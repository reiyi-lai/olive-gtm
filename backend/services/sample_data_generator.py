import os
import json
from typing import Dict, Any
from openai import OpenAI
from models.schemas import DatabaseSchemaDict, ScrapedDataDict
from utils.logger import logger

class SampleDataGenerator:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_sample_data(self, schema: DatabaseSchemaDict, scraped_data: ScrapedDataDict) -> Dict[str, Any]:
        try:
            logger.info(f"Generating sample data for: {scraped_data['company']['name']}")
            
            prompt = self._build_sample_data_prompt(schema, scraped_data)
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=3000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI for sample data generation")
            
            logger.info(f"OpenAI sample data response: '{content}'")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            sample_data = json.loads(content)
            
            # Validate that all tables from schema are present
            self._validate_sample_data(sample_data, schema)
            
            logger.info(f"Successfully generated sample data for: {scraped_data['company']['name']}")
            return sample_data
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error for {scraped_data['company']['name']}: {e}")
            logger.error(f"Raw OpenAI content: '{content}'")
            raise Exception(f"Invalid JSON response from AI: {e}")
        except Exception as e:
            logger.error(f"Error generating sample data for {scraped_data['company']['name']}", e)
            raise

    def _validate_sample_data(self, sample_data: Dict[str, Any], schema: DatabaseSchemaDict) -> None:
        """Validate that sample data contains all required tables."""
        schema_tables = {table['name'] for table in schema['tables']}
        sample_tables = set(sample_data.keys())
        
        missing_tables = schema_tables - sample_tables
        if missing_tables:
            raise Exception(f"Missing sample data for tables: {missing_tables}")
        
        # Validate that each table has at least one record
        for table_name, records in sample_data.items():
            if not records or not isinstance(records, list):
                raise Exception(f"Table {table_name} must have at least one record")
    
    def _build_sample_data_prompt(self, schema: DatabaseSchemaDict, scraped_data: ScrapedDataDict) -> str:
        return f"""
        Generate realistic sample data for the following database schema. The data should be representative of what {scraped_data['company']['name']} ({scraped_data['business_type']}) would actually store.

        Company Context:
        - Name: {scraped_data['company']['name']}
        - Business Type: {scraped_data['business_type']}
        - Key Features: {', '.join(scraped_data['key_features'])}
        - Description: {scraped_data['description']}

        Database Schema:
        {json.dumps(schema, indent=2)}

        Guidelines for sample data:
        - Generate 5-10 realistic records per table
        - Use company-appropriate data (e.g., for SaaS: realistic user emails, subscription tiers)
        - Maintain referential integrity between tables
        - Use realistic dates, names, amounts, etc.
        - For IDs, use simple incrementing numbers (1, 2, 3, etc.)
        - For foreign keys, ensure they reference valid primary keys
        - For dates, use recent dates in ISO format (YYYY-MM-DD)

        IMPORTANT: Respond with a JSON object where each key is a table name and the value is an array of records:
        {{
            "table_name": [
                {{
                    "column1": "value1",
                    "column2": "value2"
                }}
            ]
        }}

        Make the data realistic and business-relevant. For example:
        - If it's an e-commerce company, include real product categories and reasonable prices
        - If it's a SaaS company, include realistic subscription plans and usage metrics
        - If it's a healthcare company, include appropriate medical terminology and procedures
        """