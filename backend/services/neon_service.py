import os
import re
import json
import psycopg2
import asyncio
import time
from typing import Dict, Any, List
from neon_api import NeonAPI
from utils.logger import logger

class NeonService:
    """
    Service for managing Neon databases using the official Neon API.
    """
    
    def __init__(self):
        self.api_key = os.getenv("NEON_API_KEY")
        if not self.api_key:
            raise ValueError("NEON_API_KEY environment variable is required")
        
        self.neon_client = NeonAPI(api_key=self.api_key)
        self.org_id = os.getenv("NEON_ORG_ID")
        
    def _sanitize_db_name(self, company_name: str) -> str:
        """Sanitize company name to create a valid database name."""
        sanitized = re.sub(r'[^a-z0-9_]', '_', company_name.lower())
        if sanitized and sanitized[0].isdigit():
            sanitized = f"company_{sanitized}"
        return f"olive_demo_{sanitized}"
    
    def _get_postgres_type(self, schema_type: str) -> str:
        """Convert schema type to PostgreSQL type."""
        type_mapping = {
            "string": "TEXT",
            "number": "NUMERIC",
            "boolean": "BOOLEAN", 
            "date": "TIMESTAMP",
            "json": "JSONB"
        }
        return type_mapping.get(schema_type, "TEXT")
    
    async def create_database_project(self, company_name: str) -> Dict[str, Any]:
        """
        Create a new Neon project for the company using the real Neon API.
        """
        try:
            db_name = self._sanitize_db_name(company_name)
            logger.info(f"Creating Neon project for company {company_name}: {db_name}")
            
            # Create a new Neon project using correct API method and format
            project_response = self.neon_client.project_create(
                project={
                    "name": f"Olive Demo - {company_name}",
                    "pg_version": 15,
                    "region_id": "aws-us-east-1"
                }
            )
            
            # Extract project info from response object
            project = project_response.project
            project_id = project.id
            
            logger.info(f"Created Neon project: {project_id}")
            
            # Get the default branch (main branch)
            branches_response = self.neon_client.branches(project_id)
            main_branch = None
            for branch in branches_response.branches:
                if branch.default:  # Find the default branch
                    main_branch = branch
                    break
            
            if not main_branch:
                raise Exception("No default branch found in the project")
            
            default_branch_id = main_branch.id
            logger.info(f"Using default branch: {default_branch_id}")
            
            # Get the default role for the database owner
            roles_response = self.neon_client.roles(project_id, default_branch_id)
            default_role = roles_response.roles[0]  # Use the first/default role
            owner_name = default_role.name
            logger.info(f"Using default role as owner: {owner_name}")
            
            # Create a new database within the project (with retry for initialization)
            max_retries = 3
            retry_delay = 10  # seconds
            
            for attempt in range(max_retries):
                try:
                    logger.info(f"Creating database (attempt {attempt + 1}/{max_retries})...")
                    database_response = self.neon_client.database_create(
                        project_id=project_id,
                        branch_id=default_branch_id,
                        database={
                            "name": db_name,
                            "owner_name": owner_name
                        }
                    )
                    logger.info(f"Database created successfully on attempt {attempt + 1}")
                    break
                except Exception as e:
                    if "conflicting operations" in str(e) and attempt < max_retries - 1:
                        logger.info(f"Project still initializing, waiting {retry_delay} seconds before retry...")
                        time.sleep(retry_delay)
                        continue
                    else:
                        raise e
            
            # Get connection URI using the API method
            connection_response = self.neon_client.connection_uri(
                project_id=project_id,
                database_name=db_name,
                role_name=owner_name
            )
            
            connection_string = connection_response.uri if hasattr(connection_response, 'uri') else connection_response["uri"]
            
            project_info = {
                "project_id": project_id,
                "database_name": db_name,
                "connection_string": connection_string,
                "status": "active"
            }
            
            logger.info(f"Created Neon project and database: {project_id}/{db_name}")
            return project_info
            
        except Exception as e:
            logger.error(f"Error creating Neon project for {company_name}", e)
            raise
    
    async def create_schema_and_data(
        self, 
        connection_string: str, 
        schema: Dict[str, Any], 
        sample_data: Dict[str, Any]
    ) -> bool:
        """
        Create tables and insert sample data into the Neon database.
        Optimized for Neon's PostgreSQL features.
        """
        try:
            logger.info("Creating schema and inserting sample data into Neon database")
            
            # Connect to Neon database
            conn = psycopg2.connect(connection_string)
            conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
            
            with conn.cursor() as cursor:
                # Create tables
                for table in schema["tables"]:
                    columns = []
                    for column in table["columns"]:
                        postgres_type = self._get_postgres_type(column["type"])
                        nullable = "" if column["nullable"] else "NOT NULL"
                        columns.append(f"{column['name']} {postgres_type} {nullable}")
                    
                    # Add primary key constraint
                    columns.append(f"PRIMARY KEY ({table['primary_key']})")
                    
                    create_sql = f"""
                    CREATE TABLE IF NOT EXISTS {table["name"]} (
                        {', '.join(columns)}
                    )
                    """
                    cursor.execute(create_sql)
                    logger.info(f"Created table: {table['name']}")
                
                # Create relationships (foreign keys)
                for relationship in schema["relationships"]:
                    if relationship["type"] in ["one-to-many", "many-to-one"]:
                        constraint_name = f"fk_{relationship['from_table']}_{relationship['from_column']}"
                        
                        # Check if constraint already exists
                        cursor.execute("""
                            SELECT 1 FROM information_schema.table_constraints 
                            WHERE constraint_name = %s AND table_name = %s
                        """, (constraint_name, relationship["from_table"]))
                        
                        if cursor.fetchone() is None:
                            alter_sql = f"""
                            ALTER TABLE {relationship["from_table"]}
                            ADD CONSTRAINT {constraint_name}
                            FOREIGN KEY ({relationship["from_column"]})
                            REFERENCES {relationship["to_table"]}({relationship["to_column"]})
                            """
                            try:
                                cursor.execute(alter_sql)
                                logger.info(f"Added foreign key: {relationship['from_table']}.{relationship['from_column']} -> {relationship['to_table']}.{relationship['to_column']}")
                            except psycopg2.Error as e:
                                logger.warn(f"Could not add foreign key: {e}")
                
                # Insert sample data with batch optimization
                for table_name, rows in sample_data.items():
                    if not rows:
                        continue
                    
                    # Get column names from first row
                    columns = list(rows[0].keys())
                    placeholders = ", ".join(["%s"] * len(columns))
                    
                    insert_sql = f"""
                    INSERT INTO {table_name} ({', '.join(columns)})
                    VALUES ({placeholders})
                    ON CONFLICT DO NOTHING
                    """
                    
                    # Prepare batch data for faster insertion
                    batch_data = []
                    for row in rows:
                        values = []
                        for col in columns:
                            value = row[col]
                            # Convert dict objects to JSON strings for PostgreSQL
                            if isinstance(value, dict):
                                value = json.dumps(value)
                            values.append(value)
                        batch_data.append(values)
                    
                    # Insert in batches for better performance
                    try:
                        cursor.executemany(insert_sql, batch_data)
                        logger.info(f"Inserted {len(rows)} rows into {table_name}")
                    except psycopg2.Error as e:
                        logger.warn(f"Batch insert failed for {table_name}, falling back to individual inserts: {e}")
                        # Fallback to individual inserts if batch fails
                        for values in batch_data:
                            try:
                                cursor.execute(insert_sql, values)
                            except psycopg2.Error as insert_error:
                                logger.warn(f"Failed to insert row in {table_name}: {insert_error}")
                        logger.info(f"Completed individual inserts for {table_name}")
            
            conn.close()
            logger.info("Successfully created schema and inserted sample data")
            return True
            
        except Exception as e:
            logger.error("Error creating schema and data in Neon database", e)
            raise
    
    async def create_company_database(
        self, 
        company_name: str, 
        schema: Dict[str, Any], 
        sample_data: Dict[str, Any]
    ) -> str:
        """
        Complete workflow: create Neon project and populate with schema and data.
        Returns the connection string.
        """
        try:
            # Step 1: Create Neon project
            project_info = await self.create_database_project(company_name)
            
            # Step 2: Create schema and insert data
            await self.create_schema_and_data(
                project_info["connection_string"], 
                schema, 
                sample_data
            )
            
            logger.info(f"Successfully created complete Neon database for {company_name}")
            return project_info["connection_string"]
            
        except Exception as e:
            logger.error(f"Error creating complete Neon database for {company_name}", e)
            raise