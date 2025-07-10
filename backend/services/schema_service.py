import os
import json
from typing import Dict, Any
from openai import OpenAI
from pydantic import ValidationError
from models.schemas import ScrapedData, DatabaseSchema
from utils.logger import logger

class SchemaService:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def infer_schema(self, scraped_data: ScrapedData) -> DatabaseSchema:
        try:
            logger.info(f"Inferring schema for company: {scraped_data.company.name}")
            
            prompt = self._build_schema_prompt(scraped_data)
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=2000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI for schema inference")
            
            logger.info(f"OpenAI schema response: '{content}'")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            schema_dict = json.loads(content)
            
            # Validate and create DatabaseSchema with Pydantic
            schema = DatabaseSchema(**schema_dict)
            
            logger.info(f"Successfully inferred schema for: {scraped_data.company.name}")
            return schema
            
        except ValidationError as e:
            logger.error(f"Schema validation error for {scraped_data.company.name}", e)
            raise Exception(f"Invalid schema structure: {e}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error for {scraped_data.company.name}: {e}")
            logger.error(f"Raw OpenAI content: '{content}'")
            raise Exception(f"Invalid JSON response from AI: {e}")
        except Exception as e:
            logger.error(f"Error inferring schema for {scraped_data.company.name}", e)
            raise
    
    def _build_schema_prompt(self, scraped_data: ScrapedData) -> str:
        return f"""
        You are a database architect. Based on the following company information, design a realistic database schema that this company would likely use to store their business data.

        Company: {scraped_data.company.name}
        Business Type: {scraped_data.business_type}
        Key Features: {', '.join(scraped_data.key_features)}
        Description: {scraped_data.description}

        Consider what data entities this business would need to track based on their industry and features.

        Common patterns by business type:
        - SaaS: users, subscriptions, usage_analytics, billing, features
        - E-commerce: products, customers, orders, inventory, payments
        - Fintech: users, accounts, transactions, payments, compliance
        - Healthcare: patients, appointments, treatments, providers, billing

        Design 4-6 core tables with realistic relationships. Include:
        - Primary keys and foreign keys
        - Realistic column names and data types
        - Proper relationships between tables

        IMPORTANT: Respond with a JSON object in this EXACT format:
        {{
            "tables": [
                {{
                    "name": "table_name",
                    "columns": [
                        {{
                            "name": "column_name",
                            "type": "string|number|boolean|date|json",
                            "nullable": true|false,
                            "description": "what this column stores"
                        }}
                    ],
                    "primary_key": "column_name",
                    "description": "what this table represents"
                }}
            ],
            "relationships": [
                {{
                    "from_table": "table1",
                    "from_column": "foreign_key",
                    "to_table": "table2",
                    "to_column": "primary_key",
                    "type": "one-to-one|one-to-many|many-to-many|many-to-one"
                }}
            ],
            "description": "Brief description of the overall schema design"
        }}
        """