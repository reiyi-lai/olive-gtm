from typing import Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks

from models.schemas import (
    CompanyDict, CompanyRequest, CompanyStatus, ProcessingStatusDict
)
from typing import Optional
from services.gtm_service import GTMService
from utils.file_manager import FileManager
from utils.logger import logger

router = APIRouter(prefix="/api/gtm", tags=["gtm"])

# In-memory storage for processing status
processing_status: Dict[str, ProcessingStatusDict] = {}

# Initialize services
gtm_service = GTMService()
file_manager = FileManager()

@router.post("/process-company")
async def process_company(
    request: CompanyRequest, 
    background_tasks: BackgroundTasks,
    olive_backend_url: Optional[str] = "http://localhost:3000",
    olive_frontend_url: Optional[str] = "http://localhost:3001"
):
    """Start processing a company through the GTM pipeline."""
    try:
        # Check if company data already exists
        existing_dir = await file_manager.find_existing_company_dir(request.name)
        
        if existing_dir:
            # Use existing company data
            company_id = existing_dir.name
            logger.info(f"Found existing data for {request.name}, using existing folder: {company_id}")
        else:
            # Create new company folder using sanitized name
            sanitized_name = file_manager._sanitize_company_name(request.name)
            company_id = sanitized_name
            logger.info(f"Creating new folder for {request.name}: {company_id}")
        
        company: CompanyDict = {
            "id": company_id,
            "name": request.name,
            "website": request.website,
            "status": CompanyStatus.PENDING
        }
        
        # Initialize processing status
        processing_status[company["id"]] = {
            "company_id": company["id"],
            "current_step": "Starting...",
            "progress": 0
        }
        
        # Start background processing with Olive configuration
        background_tasks.add_task(
            process_company_async, 
            company, 
            olive_backend_url, 
            olive_frontend_url
        )
        
        return {
            "company_id": company["id"],
            "message": "Processing started",
            "company": company
        }
        
    except Exception as e:
        logger.error("Error starting company processing", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/status/{company_id}")
async def get_processing_status(company_id: str):
    """Get the current processing status for a company."""
    if company_id not in processing_status:
        raise HTTPException(status_code=404, detail="Company not found")
    
    return processing_status[company_id]

@router.get("/result/{company_id}")
async def get_result(company_id: str):
    """Get the complete GTM results for a company."""
    try:
        # Load the new markdown output and connection string
        markdown_output = await file_manager.load_markdown_output(company_id)
        connection_string = await file_manager.load_connection_string(company_id)
        
        if not markdown_output:
            raise HTTPException(
                status_code=404, 
                detail="Results not found or processing not complete"
            )
        
        result = {
            "company_id": company_id,
            "markdown_output": markdown_output,
            "connection_string": connection_string,
            "status": "completed"
        }
        
        return result
        
    except Exception as e:
        logger.error("Error fetching results", e)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/olive-info/{company_id}")
async def get_olive_info(company_id: str):
    """Get Olive integration information for a company."""
    try:
        olive_info = await file_manager.load_json_file(company_id, "olive_integration.json")
        
        if not olive_info:
            raise HTTPException(
                status_code=404, 
                detail="Olive integration data not found or not yet completed"
            )
        
        # Add quick status check if database_id is available
        if olive_info.get('success') and olive_info.get('database_id'):
            return {
                "company_id": company_id,
                "olive_integration": olive_info,
                "frontend_url": olive_info.get('frontend_url'),
                "admin_url": olive_info.get('admin_url'),
                "suggestions": olive_info.get('suggestions', []),
                "database_id": olive_info.get('database_id')
            }
        else:
            return {
                "company_id": company_id,
                "olive_integration": olive_info,
                "error": "Olive integration failed"
            }
        
    except Exception as e:
        logger.error("Error fetching Olive info", e)
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_company_async(
    company: CompanyDict, 
    olive_backend_url: str = "http://localhost:3000",
    olive_frontend_url: str = "http://localhost:3001"
):
    """Background task to process a company through the new unified GTM pipeline."""
    try:
        # Check if we already have a completed result
        existing_markdown = await file_manager.load_markdown_output(company["name"])
        if existing_markdown:
            logger.info(f"Found existing completed result for {company['name']}, skipping processing")
            update_status(company["id"], "Completed!", 100)
            return
        
        # Step 1: Company research and analysis
        update_status(company["id"], "Researching company...", 20)
        
        # Step 2: Generate schema, sample data, and recommendations
        update_status(company["id"], "Generating database schema and sample data...", 50)
        
        # Step 3: Create Neon database
        update_status(company["id"], "Creating Neon database...", 60)
        
        # Step 4: Integrate with Olive
        update_status(company["id"], "Integrating with Olive platform...", 80)
        
        # Run the unified GTM processing with Olive integration
        gtm_service_with_olive = GTMService(olive_backend_url, olive_frontend_url)
        result = await gtm_service_with_olive.process_company(company)
        
        # Save the results including Olive integration data
        await file_manager.save_markdown_output(company["name"], result['markdown_output'])
        await file_manager.save_connection_string(company["name"], result['connection_string'])
        
        # Save Olive integration info for later retrieval
        if result.get('olive_integration'):
            await file_manager.save_json_file(
                company["name"], 
                "olive_integration.json", 
                result['olive_integration']
            )
        
        # Complete
        update_status(company["id"], "Completed!", 100)
        logger.info(f"Successfully processed company: {company['name']}")
        
    except Exception as e:
        logger.error(f"Error processing company {company['name']}", e)
        update_status(company["id"], "Failed", 0, str(e))

def update_status(company_id: str, current_step: str, progress: int, error: str = None):
    """Update the processing status for a company."""
    processing_status[company_id] = {
        "company_id": company_id,
        "current_step": current_step,
        "progress": progress,
        "error": error
    }