import os
import json
import re
from typing import Dict, Any, Optional
from openai import OpenAI
from datetime import datetime
from utils.logger import logger
from models.schemas import CompanyDict
from services.neon_service import NeonService
from services.olive_service import OliveService

class GTMService:
    """
    Unified GTM service that implements Bardia's system prompt for Olive demo databases.
    Combines web research, schema inference, sample data generation, and Neon database creation.
    """
    
    def __init__(self, olive_backend_url: str = None, olive_frontend_url: str = None):
        self.openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.neon_service = NeonService()
        self.olive_service = OliveService(
            backend_url=olive_backend_url or "http://localhost:3000",
            frontend_url=olive_frontend_url or "http://localhost:3001"
        )
    
    async def process_company(self, company: CompanyDict) -> Dict[str, Any]:
        """
        Main method that processes a company through the complete GTM pipeline.
        Returns the final markdown output and Neon connection string.
        """
        try:
            logger.info(f"Starting GTM processing for company: {company['name']}")
            
            # Step 1: Research company (replaces web scraping)
            company_analysis = await self._research_company(company)
            
            # Step 2: Generate schema, sample data, and tool recommendations using boss's system prompt
            gtm_result = await self._generate_gtm_output(company_analysis)
            
            # Step 3: Create Neon database
            connection_string = await self._create_neon_database(
                company['name'], 
                gtm_result['schema'], 
                gtm_result['sample_data']
            )
            
            # Step 4: Integrate with Olive platform
            olive_result = await self._integrate_with_olive(
                connection_string, 
                company['name']
            )
            
            # Step 5: Create final markdown output (enhanced with Olive info)
            markdown_output = self._create_markdown_output(
                company['name'],
                company_analysis,
                gtm_result,
                connection_string,
                olive_result
            )
            
            logger.info(f"Successfully processed company: {company['name']}")
            return {
                'company_analysis': company_analysis,
                'markdown_output': markdown_output,
                'connection_string': connection_string,
                'schema': gtm_result['schema'],
                'sample_data': gtm_result['sample_data'],
                'tool_recommendations': gtm_result['tool_recommendations'],
                'olive_integration': olive_result
            }
            
        except Exception as e:
            logger.error(f"Error processing company {company['name']}", e)
            raise
    
    async def _research_company(self, company: CompanyDict) -> Dict[str, Any]:
        """
        Research company using OpenAI with web browsing capabilities.
        Replaces Firecrawl with more comprehensive research.
        """
        try:
            logger.info(f"Researching company: {company['name']} at {company['website']}")
            
            prompt = f"""
            Research the company {company['name']} at {company['website']}. 
            I need to understand what this company does, their business model, and what their Postgres database likely contains.

            Please provide detailed information about:
            1. What the company does (their core product/service)
            2. Who their target customers are  
            3. Their business model (SaaS, e-commerce, marketplace, etc.)
            4. Key features and capabilities they offer
            5. The type of data they would need to store to run their business

            Focus on understanding their internal operations, not just their marketing website.
            Look for clues about their database needs based on their product functionality.

            Respond with a JSON object in this exact format:
            {{
                "company_name": "{company['name']}",
                "website": "{company['website']}",
                "business_description": "detailed description of what they do",
                "business_model": "SaaS/E-commerce/Marketplace/etc",
                "target_customers": "who uses their product",
                "key_features": ["feature1", "feature2", "feature3"],
                "likely_data_needs": ["type of data they store", "another data type"],
                "industry": "specific industry category"
            }}
            """
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI for company research")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            result = json.loads(content)
            logger.info(f"Successfully researched company: {company['name']}")
            return result
            
        except Exception as e:
            logger.error(f"Error researching company {company['name']}", e)
            # Return fallback data
            return {
                "company_name": company['name'],
                "website": company['website'],
                "business_description": "Research failed - unable to analyze company",
                "business_model": "Unknown",
                "target_customers": "Unknown",
                "key_features": [],
                "likely_data_needs": [],
                "industry": "Unknown"
            }
    
    async def _generate_gtm_output(self, company_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate schema, sample data, and tool recommendations using Bardia's system prompt.
        This is the core AI processing step.
        """
        try:
            logger.info(f"Generating GTM output for: {company_analysis['company_name']}")
            
            # Use Bardia's exact system prompt
            system_prompt = """
# olive demo dbs

My name is Bardia. I'm the founder of Olive (fromolive.com), an AI-powered internal tooling platform. Olive connects directly to a company's Postgres database and lets teams instantly generate full-featured internal tools—like dashboards, CRUD panels, and charts—just by describing what they need in natural language.

For example, a great use case is a payroll/compliance/bookkeeping company. This is an example of a service-oriented business wrapped by software. Think: they likely have people behind the scenes going into user's company accounts to add bookkeeping files, update numbers, look and mark transactions, etc. but the users use the product through a software. This is a great example where Olive would be great, because they can create and prompt for tools quickly that their teams can use.​ Obviously don't base responses around this, just want to show you the capabilities. It really depends on the actual company, this is just one example of one sector.

We're using Neon MCP to spin up detailed demo databases that simulate the company's real-world Postgres schema and populate them with sample data. These are all products that have Postgres databases for their products and our job is to guess what those contain. Then, these demo DBs are used to generate internal tools we showcase in custom videos to prospects. The goal is to show each company what they could build with Olive—instantly—if they connected their production DB.

You are responsible for:

- Predicting what a company's actual Postgres database likely contains based on their product and target customers.
- Creating a schema with realistic tables and columns that represent how their business operates under the hood.
- Populating the database with hundreds of rows of highly varied, believable sample data that tells a compelling story in a demo
- Things like billing, behavior analytics, or things that are unlikely to be stored in the database, or frankly don't matter for our demo, shouldn't be included.

After, I need you to recommend two internal tools that they could build with Olive based on this schema. Understand that:

- Tools are NOT for end users of the company, but for the people running this product and overseeing the database
- Thinking like the internal team: what data would their ops, product, growth, support teams want visibility into or control over?
- Avoiding features for end users—tools should serve the company's internal team, not their customers.
- Avoid recommending tools to patch missing things in the database, check the health of things, don't design for errors or fixing broken things. design thinking things are working and u are showing even more visibility into what happens in the product/things that need to be changed on the data layer.

Examples of tools people can create on Olive:

- Show me a dashboard of all users grouped by organization, including their role and signup date.
- Show me accounts who haven't completed onboarding and what % of features they've used
- Let me see all documents within workspaces in my database
- Create a dashboard of user activity grouped by organization and flagged for churn signals.
- Create a dashboard to view and update inventory labels for products across warehouses.
- Give me a tool to view product details by product ID.
- Show me a chart of my DAU based on my users and their signup date

You'll see most of these are basically a UI CRUD layer over the database. We think the most helpful thing here will be to visualize or make dashboards to understand what happens inside your database. Instead of waiting on engineers to scope and build custom dashboards, users of Olive can generate fully functional, query-aware interfaces (with filters, CRUD, search, and charts) that map directly to their existing database schema.

Understand that you need tools NOT for their end users (e.g. for a SaaS company that helps other companies do shipping, a tool to see the your current shipments and their status is useless because its for their customer, NOT for them. A tool to see all companies and how many things they've shipped is a good tool, on the other hand).

During generation of data, it is _CRITICAL_ that there is a ton of data. For example, each table should have tens if not 100 etc rows. It should look like there is enough data. If there are foreign key relationships, there should NEVER be a case where one row's foreign key relationship is empty/there's no data. There should be data for EVERYTHING!!

Also, don't be stupid with data. If you're including numbers for example, don't include a total that will add up numbers from other tables, etc. Things that depend on each other easily break and should be calculated later in code, not hardcoded. For example say you're building a tool for a social media app. There should never be a field like "total comments" under a post because you can get that by just adding up the actual comment cells. Etc.
            """
            
            user_prompt = f"""
            Company Information:
            - Name: {company_analysis['company_name']}
            - Website: {company_analysis['website']}
            - Business Description: {company_analysis['business_description']}
            - Business Model: {company_analysis['business_model']}
            - Target Customers: {company_analysis['target_customers']}
            - Key Features: {', '.join(company_analysis['key_features'])}
            - Industry: {company_analysis['industry']}
            
            Based on this company information, please:
            1. Design a realistic PostgreSQL database schema (4-6 core tables)
            2. Generate substantial sample data (50-100 rows per table minimum)
            3. Recommend 2 internal tools for their team
            
            Respond with a JSON object in this exact format:
            {{
                "schema": {{
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
                            "type": "one-to-many|many-to-one|one-to-one"
                        }}
                    ],
                    "description": "Brief description of the overall schema design"
                }},
                "sample_data": {{
                    "table_name": [
                        {{
                            "column1": "value1",
                            "column2": "value2"
                        }}
                    ]
                }},
                "tool_recommendations": [
                    {{
                        "title": "Tool 1 Name",
                        "description": "What this internal tool does for the team",
                        "target_users": "Which internal team members would use this"
                    }},
                    {{
                        "title": "Tool 2 Name", 
                        "description": "What this internal tool does for the team",
                        "target_users": "Which internal team members would use this"
                    }}
                ]
            }}
            """
            
            response = self.openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.2,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            if not content:
                raise Exception("No response from OpenAI for GTM output generation")
            
            # Strip markdown code blocks if present
            if content.startswith('```json'):
                content = content.replace('```json', '').replace('```', '').strip()
            elif content.startswith('```'):
                content = content.replace('```', '').strip()
            
            result = json.loads(content)
            logger.info(f"Successfully generated GTM output for: {company_analysis['company_name']}")
            return result
            
        except Exception as e:
            logger.error(f"Error generating GTM output for {company_analysis['company_name']}", e)
            raise
    
    async def _create_neon_database(self, company_name: str, schema: Dict[str, Any], sample_data: Dict[str, Any]) -> str:
        """
        Create a Neon database using the Neon service.
        """
        try:
            logger.info(f"Creating Neon database for: {company_name}")
            
            connection_string = await self.neon_service.create_company_database(
                company_name, schema, sample_data
            )
            
            logger.info(f"Successfully created Neon database for: {company_name}")
            return connection_string
            
        except Exception as e:
            logger.error(f"Error creating Neon database for {company_name}", e)
            raise
    
    async def _integrate_with_olive(self, connection_string: str, company_name: str) -> Dict[str, Any]:
        """
        Integrate the Neon database with Olive platform.
        """
        try:
            logger.info(f"Integrating {company_name} database with Olive...")
            
            database_name = f"{company_name} Analytics DB"
            result = await self.olive_service.integrate_with_olive(
                connection_string=connection_string,
                database_name=database_name,
                suggestions_count=6  # Generate more suggestions for variety
            )
            
            if result['success']:
                logger.info(f"✅ Successfully integrated with Olive: {result['database_id']}")
            else:
                logger.warning(f"⚠️  Olive integration failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error integrating with Olive: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'database': None,
                'suggestions': []
            }

    def _create_markdown_output(
        self, 
        company_name: str, 
        company_analysis: Dict[str, Any], 
        gtm_result: Dict[str, Any], 
        connection_string: str,
        olive_result: Dict[str, Any] = None
    ) -> str:
        """
        Create the final markdown output as specified in the boss's system prompt.
        """
        try:
            logger.info(f"Creating markdown output for: {company_name}")
            
            # Create table descriptions
            tables_description = []
            for table in gtm_result['schema']['tables']:
                row_count = len(gtm_result['sample_data'].get(table['name'], []))
                tables_description.append(f"- **{table['name']}**: {table['description']} ({row_count} rows)")
            
            # Create tool recommendations
            tools_section = []
            for i, tool in enumerate(gtm_result['tool_recommendations'], 1):
                tools_section.append(f"{i}. **{tool['title']}**: {tool['description']}")
            
            markdown = f"""# {company_name}

## Company Summary
{company_analysis['business_description']}

**Industry**: {company_analysis['industry']}  
**Business Model**: {company_analysis['business_model']}  
**Target Customers**: {company_analysis['target_customers']}

## Database Schema
{gtm_result['schema']['description']}

### Tables Created:
{chr(10).join(tables_description)}

### Table Relationships:
The database maintains proper referential integrity with the following key relationships:
{chr(10).join([f"- {rel['from_table']}.{rel['from_column']} → {rel['to_table']}.{rel['to_column']} ({rel['type']})" for rel in gtm_result['schema']['relationships']])}

## Recommended Internal Tools

{chr(10).join(tools_section)}

## Database Connection
**Connection String**: `{connection_string}`

**Total Sample Data**: {sum(len(rows) for rows in gtm_result['sample_data'].values())} rows across {len(gtm_result['schema']['tables'])} tables

{self._generate_olive_section(olive_result)}

---
*Generated with Olive GTM Engine - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            
            logger.info(f"Successfully created markdown output for: {company_name}")
            return markdown
            
        except Exception as e:
            logger.error(f"Error creating markdown output for {company_name}", e)
            raise
    
    def _generate_olive_section(self, olive_result: Dict[str, Any]) -> str:
        """Generate the Olive integration section for markdown output."""
        if not olive_result or not olive_result.get('success'):
            return """
## 🚫 Olive Integration
**Status**: Failed to connect to Olive platform
**Note**: Ensure Olive is running locally on http://localhost:3000

To start Olive locally, run:
```bash
# In your Olive repository
npm install
npm run dev
```
"""
        
        suggestions_text = ""
        if olive_result.get('suggestions'):
            suggestions_list = []
            for i, suggestion in enumerate(olive_result['suggestions'], 1):
                title = suggestion.get('title', f'Suggestion {i}')
                prompt = suggestion.get('prompt', suggestion.get('description', 'No prompt available'))
                suggestions_list.append(f"{i}. **{title}**: {prompt}")
            suggestions_text = f"""
### 💡 AI-Generated Prompt Suggestions
{chr(10).join(suggestions_list)}
"""
        
        return f"""
## 🎯 Olive Integration
**Status**: ✅ Successfully connected to Olive
**Database ID**: `{olive_result.get('database_id', 'N/A')}`
**Frontend URL**: {olive_result.get('frontend_url', 'N/A')}
**Admin Panel**: {olive_result.get('admin_url', 'N/A')}

{suggestions_text}

### 🚀 Next Steps
1. **Open Olive Frontend**: Visit the frontend URL above to interact with your data
2. **Create Apps**: Use any of the suggested prompts to generate dashboards
3. **Customize**: Send additional messages to modify the generated apps
4. **Export**: Add export functionality or other features as needed

### 🛠️ Available Actions
- **Create App**: Use the frontend to create data applications
- **Query Data**: Run natural language queries against your database
- **Generate Insights**: Get AI-powered analytics and recommendations
"""