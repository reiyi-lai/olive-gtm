import os
import json
from typing import Dict, Any
from openai import OpenAI
from models.schemas import DatabaseSchemaDict, ScrapedDataDict, GeneratedPromptDict
from utils.logger import logger

class PromptGenerator:
    def __init__(self):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def generate_prompt(
        self, 
        schema: DatabaseSchemaDict, 
        sample_data: Dict[str, Any], 
        scraped_data: ScrapedDataDict
    ) -> GeneratedPromptDict:
        try:
            logger.info(f"Generating Olive prompt for: {scraped_data['company']['name']}")
            
            prompt = self._build_prompt_generation_prompt(schema, sample_data, scraped_data)
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI for prompt generation")
            
            logger.info(f"OpenAI prompt response: '{content}'")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            prompt_dict = json.loads(content)
            # No Pydantic validation, just return dict
            logger.info(f"Successfully generated prompt for: {scraped_data['company']['name']}")
            return prompt_dict
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error for {scraped_data['company']['name']}: {e}")
            logger.error(f"Raw OpenAI content: '{content}'")
            raise Exception(f"Invalid JSON response from AI: {e}")
        except Exception as e:
            logger.error(f"Error generating prompt for {scraped_data['company']['name']}", e)
            raise

    def _build_prompt_generation_prompt(
        self, 
        schema: DatabaseSchemaDict, 
        sample_data: Dict[str, Any], 
        scraped_data: ScrapedDataDict
    ) -> str:
        return f"""
        You are an expert at creating dashboard prompts for Olive, a tool that turns natural language prompts into live dashboards from company databases.

        Company Context:
        - Name: {scraped_data['company']['name']}
        - Business Type: {scraped_data['business_type']}
        - Key Features: {', '.join(scraped_data['key_features'])}
        - Description: {scraped_data['description']}

        Database Schema:
        {json.dumps(schema, indent=2)}

        Sample Data Preview:
        {json.dumps(sample_data, indent=2)[:1000]}...

        Your task is to create the optimal natural language prompt that a {scraped_data['business_type']} company would use to create a comprehensive executive dashboard in Olive.

        The prompt should:
        1. Request the most important KPIs for this business type
        2. Include relevant metrics, charts, and visualizations
        3. Focus on actionable insights executives would need
        4. Be specific about data sources and table relationships
        5. Use natural language that Olive can understand

        Examples of good prompts:
        - "Create a SaaS executive dashboard showing monthly recurring revenue, user growth, churn rate, and top features by usage"
        - "Build an e-commerce dashboard with sales trends, top products, customer lifetime value, and inventory alerts"
        - "Generate a fintech dashboard displaying transaction volume, user acquisition, revenue by product, and fraud detection metrics"

        IMPORTANT: Respond with a JSON object in this EXACT format:
        {{
            "prompt": "The natural language prompt for Olive (150-250 words)",
            "expectedDashboard": "Description of what the dashboard should show (3-4 key sections)",
            "confidence": 0.85,
            "reasoning": "Brief explanation of why this prompt would be effective for this company"
        }}
        """