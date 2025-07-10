import os
import re
import json
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from typing import Dict, Any, List
from dotenv import load_dotenv

from models.schemas import DatabaseSchema, ScrapedData
from utils.logger import logger

# Load environment variables
load_dotenv()

class DatabaseService:
    def __init__(self):
        self.host = os.getenv("POSTGRES_HOST", "localhost")
        self.port = os.getenv("POSTGRES_PORT", "5432")
        self.username = os.getenv("POSTGRES_USER")
        self.password = os.getenv("POSTGRES_PASSWORD", "")
        self.admin_db = os.getenv("POSTGRES_ADMIN_DB", "postgres")
        
        # Validate required environment variables
        if not self.username:
            raise ValueError("POSTGRES_USER environment variable is required")
    
    def _sanitize_db_name(self, company_name: str) -> str:
        """Sanitize company name to create a valid PostgreSQL database name."""
        # Convert to lowercase and replace invalid characters with underscores
        sanitized = re.sub(r'[^a-z0-9_]', '_', company_name.lower())
        # Ensure it starts with a letter or underscore
        if sanitized and sanitized[0].isdigit():
            sanitized = f"company_{sanitized}"
        # Prefix with olive_gtm for clarity
        return f"olive_gtm_{sanitized}"
    
    def _get_connection(self, database: str = None):
        """Get a database connection."""
        db_name = database or self.admin_db
        return psycopg2.connect(
            host=self.host,
            port=self.port,
            user=self.username,
            password=self.password,
            database=db_name
        )
    
    def _database_exists(self, db_name: str) -> bool:
        """Check if a database exists."""
        try:
            conn = self._get_connection()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT 1 FROM pg_database WHERE datname = %s",
                (db_name,)
            )
            result = cursor.fetchone() is not None
            cursor.close()
            conn.close()
            return result
        except Exception as e:
            logger.error(f"Error checking if database {db_name} exists", e)
            return False
    
    def _create_database(self, db_name: str):
        """Create a new PostgreSQL database."""
        try:
            conn = self._get_connection()
            conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE {db_name}")
            cursor.close()
            conn.close()
            logger.info(f"Created database: {db_name}")
        except Exception as e:
            logger.error(f"Error creating database {db_name}", e)
            raise
    
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
    
    def _create_tables(self, db_name: str, schema: DatabaseSchema):
        """Create tables in the database based on the schema."""
        try:
            with self._get_connection(db_name) as conn:
                with conn.cursor() as cursor:
                    # Create tables
                    for table in schema.tables:
                        columns = []
                        for column in table.columns:
                            postgres_type = self._get_postgres_type(column.type)
                            nullable = "" if column.nullable else "NOT NULL"
                            columns.append(f"{column.name} {postgres_type} {nullable}")
                        
                        # Add primary key constraint
                        columns.append(f"PRIMARY KEY ({table.primary_key})")
                        
                        create_sql = f"""
                        CREATE TABLE IF NOT EXISTS {table.name} (
                            {', '.join(columns)}
                        )
                        """
                        cursor.execute(create_sql)
                        logger.info(f"Created table: {table.name}")
                    
                    # Create relationships (foreign keys)
                    for relationship in schema.relationships:
                        if relationship.type in ["one-to-many", "many-to-one"]:
                            constraint_name = f"fk_{relationship.from_table}_{relationship.from_column}"
                            
                            # Check if constraint already exists
                            cursor.execute("""
                                SELECT 1 FROM information_schema.table_constraints 
                                WHERE constraint_name = %s AND table_name = %s
                            """, (constraint_name, relationship.from_table))
                            
                            if cursor.fetchone() is None:
                                alter_sql = f"""
                                ALTER TABLE {relationship.from_table}
                                ADD CONSTRAINT {constraint_name}
                                FOREIGN KEY ({relationship.from_column})
                                REFERENCES {relationship.to_table}({relationship.to_column})
                                """
                                try:
                                    cursor.execute(alter_sql)
                                    logger.info(f"Added foreign key: {relationship.from_table}.{relationship.from_column} -> {relationship.to_table}.{relationship.to_column}")
                                except psycopg2.Error as e:
                                    logger.warn(f"Could not add foreign key: {e}")
                            else:
                                logger.info(f"Foreign key {constraint_name} already exists, skipping")
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error creating tables in database {db_name}", e)
            raise
    
    def _insert_sample_data(self, db_name: str, sample_data: Dict[str, List[Dict[str, Any]]]):
        """Insert sample data into the database tables."""
        try:
            with self._get_connection(db_name) as conn:
                with conn.cursor() as cursor:
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
                        
                        # Insert each row
                        for row in rows:
                            values = []
                            for col in columns:
                                value = row[col]
                                # Convert dict objects to JSON strings for PostgreSQL
                                if isinstance(value, dict):
                                    import json
                                    value = json.dumps(value)
                                values.append(value)
                            cursor.execute(insert_sql, values)
                        
                        logger.info(f"Inserted {len(rows)} rows into {table_name}")
                    
                    conn.commit()
                    
        except Exception as e:
            logger.error(f"Error inserting sample data into database {db_name}", e)
            raise
    
    async def create_company_database(
        self, 
        company_name: str, 
        schema: DatabaseSchema, 
        sample_data: Dict[str, List[Dict[str, Any]]], 
        scraped_data: ScrapedData
    ) -> Dict[str, Any]:
        """
        Create a PostgreSQL database for a company with schema and sample data.
        Returns database connection information.
        """
        try:
            db_name = self._sanitize_db_name(company_name)
            logger.info(f"Creating database for company {company_name}: {db_name}")
            
            # Check if database already exists
            if self._database_exists(db_name):
                logger.info(f"Database {db_name} already exists, using existing database")
            else:
                # Create new database
                self._create_database(db_name)
            
            # Create tables and relationships
            self._create_tables(db_name, schema)
            
            # Insert sample data
            self._insert_sample_data(db_name, sample_data)
            
            # Return connection info
            connection_info = {
                "database_name": db_name,
                "host": self.host,
                "port": self.port,
                "username": self.username,
                "company_name": company_name,
                "created_tables": [table.name for table in schema.tables],
                "total_rows": sum(len(rows) for rows in sample_data.values()),
                "connection_string": f"postgresql://{self.username}@{self.host}:{self.port}/{db_name}"
            }
            
            logger.info(f"Successfully created database for {company_name}: {db_name}")
            return connection_info
            
        except Exception as e:
            logger.error(f"Failed to create database for company {company_name}", e)
            # Return None to indicate failure - pipeline will continue
            return None 