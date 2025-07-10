from typing import Dict
from fastapi import APIRouter, HTTPException, BackgroundTasks

from models.schemas import (
    CompanyDict, CompanyRequest, CompanyStatus, ProcessingStatusDict
)
from services.company_scraper import CompanyScraper
from services.schema_service import SchemaService
from services.sample_data_generator import SampleDataGenerator
from services.prompt_generator import PromptGenerator
from services.database_service import DatabaseService
from utils.file_manager import FileManager
from utils.logger import logger

router = APIRouter(prefix="/api/gtm", tags=["gtm"])

# In-memory storage for processing status
processing_status: Dict[str, ProcessingStatusDict] = {}

# Initialize services
company_scraper = CompanyScraper()
schema_service = SchemaService()
sample_data_generator = SampleDataGenerator()
prompt_generator = PromptGenerator()
database_service = DatabaseService()
file_manager = FileManager()

@router.post("/process-company")
async def process_company(request: CompanyRequest, background_tasks: BackgroundTasks):
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
        
        # Start background processing
        background_tasks.add_task(process_company_async, company)
        
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
        # Load all data from files
        scraped_data_dict = await file_manager.load_scraped_data(company_id)
        schema_dict = await file_manager.load_schema(company_id)
        sample_data = await file_manager.load_sample_data(company_id)
        prompt_dict = await file_manager.load_generated_prompt(company_id)
        database_info = await file_manager.load_database_info(company_id)
        
        if not all([scraped_data_dict, schema_dict, sample_data, prompt_dict]):
            raise HTTPException(
                status_code=404, 
                detail="Results not found or processing not complete"
            )
        
        # Convert scraped data to camelCase for frontend
        scraped_data_frontend = {
            "company": scraped_data_dict['company'],
            "websiteContent": scraped_data_dict['website_content'],
            "businessType": scraped_data_dict['business_type'], 
            "keyFeatures": scraped_data_dict['key_features'],
            "description": scraped_data_dict['description'],
            "timestamp": scraped_data_dict['timestamp']
        }
        
        # Return data directly with correct camelCase field names for frontend
        result = {
            "company": scraped_data_dict['company'],
            "scrapedData": scraped_data_frontend,
            "schema": schema_dict,
            "sampleData": sample_data,
            "generatedPrompt": prompt_dict
        }
        
        # Include database info if available
        if database_info:
            result["databaseInfo"] = database_info
            
        return result
        
    except Exception as e:
        logger.error("Error fetching results", e)
        raise HTTPException(status_code=500, detail="Internal server error")

async def process_company_async(company: CompanyDict):
    """Background task to process a company through the entire GTM pipeline."""
    try:
        # Check existing data and resume from last successful stage
        scraped_data = None
        schema = None
        sample_data = None
        generated_prompt = None
        
        # Step 1: Check/Scrape website
        scraped_data_dict = await file_manager.load_scraped_data(company["name"])
        if scraped_data_dict:
            try:
                logger.info(f"Found existing scraped data for {company['name']}, skipping scraping")
                scraped_data = scraped_data_dict
                update_status(company["id"], "Loaded existing scraped data", 10)
            except Exception as e:
                logger.warn(f"Failed to load existing scraped data for {company['name']}: {e}")
                scraped_data_dict = None
        
        if not scraped_data_dict:
            update_status(company["id"], "Scraping website...", 10)
            scraped_data = await company_scraper.scrape_company(company)
            await file_manager.save_scraped_data(company["name"], scraped_data)
            logger.info(f"Scraped and saved data for {company['name']}")
        
        # Step 2: Check/Infer schema
        schema_dict = await file_manager.load_schema(company["name"])
        if schema_dict:
            try:
                logger.info(f"Found existing schema for {company['name']}, skipping schema inference")
                schema = schema_dict
                update_status(company["id"], "Loaded existing schema", 30)
            except Exception as e:
                logger.warn(f"Failed to load existing schema for {company['name']}: {e}")
                schema_dict = None
        
        if not schema_dict:
            update_status(company["id"], "Inferring database schema...", 30)
            schema = await schema_service.infer_schema(scraped_data)
            await file_manager.save_schema(company["name"], schema)
            logger.info(f"Generated and saved schema for {company['name']}")
        
        # Step 3: Check/Generate sample data
        sample_data = await file_manager.load_sample_data(company["name"])
        if sample_data:
            logger.info(f"Found existing sample data for {company['name']}, skipping sample data generation")
            update_status(company["id"], "Loaded existing sample data", 50)
        else:
            update_status(company["id"], "Generating sample data...", 50)
            sample_data = await sample_data_generator.generate_sample_data(schema, scraped_data)
            await file_manager.save_sample_data(company["name"], sample_data)
            logger.info(f"Generated and saved sample data for {company['name']}")
        
        # Step 4: Check/Create PostgreSQL database
        database_info = await file_manager.load_database_info(company["name"])
        if database_info:
            logger.info(f"Found existing database info for {company['name']}, skipping database creation")
            update_status(company["id"], "Loaded existing database", 70)
        else:
            update_status(company["id"], "Creating PostgreSQL database...", 70)
            database_info = await database_service.create_company_database(
                company["name"], schema, sample_data, scraped_data
            )
            if database_info:
                await file_manager.save_database_info(company["name"], database_info)
                logger.info(f"Created and saved database for {company['name']}")
            else:
                logger.warn(f"Failed to create database for {company['name']}, continuing without database")
        
        # Step 5: Check/Generate prompt
        prompt_dict = await file_manager.load_generated_prompt(company["name"])
        if prompt_dict:
            try:
                logger.info(f"Found existing generated prompt for {company['name']}, skipping prompt generation")
                generated_prompt = prompt_dict
                update_status(company["id"], "Loaded existing prompt", 90)
            except Exception as e:
                logger.warn(f"Failed to load existing prompt for {company['name']}: {e}")
                prompt_dict = None
        
        if not prompt_dict:
            update_status(company["id"], "Creating Olive prompt...", 90)
            generated_prompt = await prompt_generator.generate_prompt(schema, sample_data, scraped_data)
            await file_manager.save_generated_prompt(company["name"], generated_prompt)
            logger.info(f"Generated and saved prompt for {company['name']}")
        
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