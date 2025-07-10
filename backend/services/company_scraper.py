import os
import json
from typing import Dict, Any
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from openai import OpenAI
from pydantic import ValidationError
from models.schemas import Company, ScrapedData
from utils.logger import logger

# Load environment variables
load_dotenv()

class CompanyScraper:
    def __init__(self):
        self.firecrawl = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def scrape_company(self, company: Company) -> ScrapedData:
        try:
            logger.info(f"Starting scrape for company: {company.name}")
            
            # Scrape website content
            logger.info(f"Attempting to scrape: {company.website}")
            scrape_result = self.firecrawl.scrape_url(
                company.website,
                params={
                    'formats': ['markdown'],
                    'onlyMainContent': True,
                    'includeTags': ['title', 'meta', 'h1', 'h2', 'h3', 'p', 'li']
                }
            )
            
            logger.info(f"Firecrawl response keys: {list(scrape_result.keys())}")
            
            # Check if we got content (Firecrawl returns data directly)
            if 'markdown' not in scrape_result and 'content' not in scrape_result:
                error_msg = scrape_result.get('error', 'No content returned')
                logger.error(f"Firecrawl failed for {company.website}: {error_msg}")
                raise Exception(f"Failed to scrape {company.website}: {error_msg}")
            
            # Get content - try markdown first, then content
            website_content = scrape_result.get('markdown', '') or scrape_result.get('content', '')
            logger.info(f"Extracted website content length: {len(website_content)}")
            
            # Analyze business context using OpenAI
            logger.info("Starting business context analysis with OpenAI...")
            business_analysis = await self._analyze_business_context(website_content, company.name)
            logger.info(f"Business analysis result: {business_analysis}")
            
            # Create and validate ScrapedData with Pydantic
            logger.info("Creating ScrapedData object...")
            scraped_data = ScrapedData(
                company=company,
                website_content=website_content,
                business_type=business_analysis['business_type'],
                key_features=business_analysis['key_features'],
                description=business_analysis['description']
            )
            logger.info("ScrapedData created successfully")
            
            logger.info(f"Successfully scraped company: {company.name}")
            return scraped_data
            
        except ValidationError as e:
            logger.error(f"Validation error for company {company.name}", e)
            raise
        except Exception as e:
            logger.error(f"Error scraping company {company.name}", e)
            raise
    
    async def _analyze_business_context(self, content: str, company_name: str) -> Dict[str, Any]:
        prompt = f"""
        Analyze the following website content for {company_name} and extract:
        1. Business type/industry (e.g., "SaaS", "E-commerce", "Fintech", "Healthcare")
        2. Key features/products they offer
        3. Brief description of what they do

        Website content:
        {content[:4000]}

        Respond with a JSON object in this exact format:
        {{
            "business_type": "specific industry/category",
            "key_features": ["feature1", "feature2", "feature3"],
            "description": "1-2 sentence description of what the company does"
        }}
        """
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI")
            
            logger.info(f"OpenAI raw response: '{content}'")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            return json.loads(content)
            
        except json.JSONDecodeError as e:
            logger.error(f"Error parsing OpenAI response: {e}")
            logger.error(f"Raw OpenAI content: '{content}'")
            return {
                "business_type": "Unknown",
                "key_features": [],
                "description": "Analysis failed"
            }
        except Exception as e:
            logger.error("Error analyzing business context", e)
            return {
                "business_type": "Unknown",
                "key_features": [],
                "description": "Analysis failed"
            }