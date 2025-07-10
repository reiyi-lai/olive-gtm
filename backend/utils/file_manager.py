import os
import json
import asyncio
import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from models.schemas import Company, ScrapedData, DatabaseSchema, GeneratedPrompt

class FileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.companies_dir = self.data_dir / "companies"
    
    def _sanitize_company_name(self, company_name: str) -> str:
        """Sanitize company name for safe use as folder name."""
        # Remove special characters and replace spaces with underscores
        sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', company_name)
        sanitized = re.sub(r'\s+', '_', sanitized).strip('_')
        return sanitized.lower()
    
    async def find_existing_company_dir(self, company_name: str) -> Optional[Path]:
        """Find existing company directory by name."""
        sanitized_name = self._sanitize_company_name(company_name)
        company_dir = self.companies_dir / sanitized_name
        return company_dir if company_dir.exists() else None
    
    async def ensure_company_dir(self, company_name: str) -> Tuple[Path, str]:
        """Ensure company directory exists and return both path and company_id."""
        sanitized_name = self._sanitize_company_name(company_name)
        company_dir = self.companies_dir / sanitized_name
        company_dir.mkdir(parents=True, exist_ok=True)
        return company_dir, sanitized_name
    
    async def save_scraped_data(self, company_name: str, data: ScrapedData) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "scraped_data.json"
        
        # Convert Pydantic model to dict for JSON serialization
        data_dict = data.dict()
        data_dict['timestamp'] = data_dict['timestamp'].isoformat()
        
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(data_dict, f, indent=2)
        return company_id
    
    async def save_schema(self, company_name: str, schema: DatabaseSchema) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "inferred_schema.json"
        
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(schema.dict(), f, indent=2)
        return company_id
    
    async def save_sample_data(self, company_name: str, sample_data: Dict[str, Any]) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "sample_data.json"
        
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(sample_data, f, indent=2)
        return company_id
    
    async def save_generated_prompt(self, company_name: str, prompt: GeneratedPrompt) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "generated_prompt.json"
        
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(prompt.dict(), f, indent=2)
        return company_id
    
    async def load_scraped_data(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        """Load scraped data by company_id or company_name."""
        try:
            # Try as company_id first (for backward compatibility)
            file_path = self.companies_dir / company_identifier / "scraped_data.json"
            if not file_path.exists():
                # Try as company name
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "scraped_data.json"
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_schema(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        """Load schema by company_id or company_name."""
        try:
            # Try as company_id first (for backward compatibility)
            file_path = self.companies_dir / company_identifier / "inferred_schema.json"
            if not file_path.exists():
                # Try as company name
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "inferred_schema.json"
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_sample_data(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        """Load sample data by company_id or company_name."""
        try:
            # Try as company_id first (for backward compatibility)
            file_path = self.companies_dir / company_identifier / "sample_data.json"
            if not file_path.exists():
                # Try as company name
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "sample_data.json"
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_generated_prompt(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        """Load generated prompt by company_id or company_name."""
        try:
            # Try as company_id first (for backward compatibility)
            file_path = self.companies_dir / company_identifier / "generated_prompt.json"
            if not file_path.exists():
                # Try as company name
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "generated_prompt.json"
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def save_database_info(self, company_name: str, database_info: Dict[str, Any]) -> str:
        """Save database connection information."""
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "database_info.json"
        
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(database_info, f, indent=2)
        return company_id
    
    async def load_database_info(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        """Load database connection information by company_id or company_name."""
        try:
            # Try as company_id first (for backward compatibility)
            file_path = self.companies_dir / company_identifier / "database_info.json"
            if not file_path.exists():
                # Try as company name
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "database_info.json"
            
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None