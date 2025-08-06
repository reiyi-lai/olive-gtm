import json
import asyncio
import re
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from models.schemas import CompanyDict, ScrapedDataDict, DatabaseSchemaDict, GeneratedPromptDict

class FileManager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.companies_dir = self.data_dir / "companies"
    
    def _sanitize_company_name(self, company_name: str) -> str:
        """Sanitize company name for safe use as folder name."""
        sanitized = re.sub(r'[^a-zA-Z0-9\s-]', '', company_name)
        sanitized = re.sub(r'\s+', '_', sanitized).strip('_')
        return sanitized.lower()
    
    async def find_existing_company_dir(self, company_name: str) -> Optional[Path]:
        sanitized_name = self._sanitize_company_name(company_name)
        company_dir = self.companies_dir / sanitized_name
        return company_dir if company_dir.exists() else None
    
    async def ensure_company_dir(self, company_name: str) -> Tuple[Path, str]:
        sanitized_name = self._sanitize_company_name(company_name)
        company_dir = self.companies_dir / sanitized_name
        company_dir.mkdir(parents=True, exist_ok=True)
        return company_dir, sanitized_name
    
    async def save_scraped_data(self, company_name: str, data: ScrapedDataDict) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "scraped_data.json"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        return company_id
    
    async def save_schema(self, company_name: str, schema: DatabaseSchemaDict) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "inferred_schema.json"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(schema, f, indent=2)
        return company_id
    
    async def save_sample_data(self, company_name: str, sample_data: Dict[str, Any]) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "sample_data.json"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(sample_data, f, indent=2)
        return company_id
    
    async def save_generated_prompt(self, company_name: str, prompt: GeneratedPromptDict) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "generated_prompt.json"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(prompt, f, indent=2)
        return company_id
    
    async def load_scraped_data(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self.companies_dir / company_identifier / "scraped_data.json"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "scraped_data.json"
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_schema(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self.companies_dir / company_identifier / "inferred_schema.json"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "inferred_schema.json"
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_sample_data(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self.companies_dir / company_identifier / "sample_data.json"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "sample_data.json"
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def load_generated_prompt(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self.companies_dir / company_identifier / "generated_prompt.json"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "generated_prompt.json"
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def save_database_info(self, company_name: str, database_info: Dict[str, Any]) -> str:
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "database_info.json"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(database_info, f, indent=2)
        return company_id
    
    async def load_database_info(self, company_identifier: str) -> Optional[Dict[str, Any]]:
        try:
            file_path = self.companies_dir / company_identifier / "database_info.json"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "database_info.json"
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None
    
    async def save_markdown_output(self, company_name: str, markdown_content: str) -> str:
        """Save the final markdown output for a company."""
        company_dir, company_id = await self.ensure_company_dir(company_name)
        sanitized_name = self._sanitize_company_name(company_name)
        file_path = company_dir / f"{sanitized_name}.md"
        async with asyncio.Lock():
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
        return company_id
    
    async def load_markdown_output(self, company_identifier: str) -> Optional[str]:
        """Load the markdown output for a company."""
        try:
            sanitized_name = self._sanitize_company_name(company_identifier)
            file_path = self.companies_dir / company_identifier / f"{sanitized_name}.md"
            if not file_path.exists():
                file_path = self.companies_dir / sanitized_name / f"{sanitized_name}.md"
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    async def save_connection_string(self, company_name: str, connection_string: str) -> str:
        """Save the Neon database connection string."""
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / "connection_string.txt"
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                f.write(connection_string)
        return company_id
    
    async def load_connection_string(self, company_identifier: str) -> Optional[str]:
        """Load the connection string for a company."""
        try:
            file_path = self.companies_dir / company_identifier / "connection_string.txt"
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / "connection_string.txt"
            with open(file_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            return None
    
    async def save_json_file(self, company_name: str, filename: str, data: dict) -> str:
        """Save any JSON data for a company."""
        company_dir, company_id = await self.ensure_company_dir(company_name)
        file_path = company_dir / filename
        async with asyncio.Lock():
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
        return company_id
    
    async def load_json_file(self, company_identifier: str, filename: str) -> Optional[dict]:
        """Load any JSON file for a company."""
        try:
            file_path = self.companies_dir / company_identifier / filename
            if not file_path.exists():
                sanitized_name = self._sanitize_company_name(company_identifier)
                file_path = self.companies_dir / sanitized_name / filename
            with open(file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return None