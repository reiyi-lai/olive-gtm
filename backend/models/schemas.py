from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum

class CompanyStatus(str, Enum):
    PENDING = "pending"
    SCRAPING = "scraping"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

class Company(BaseModel):
    id: str
    name: str
    website: str
    industry: Optional[str] = None
    status: CompanyStatus = CompanyStatus.PENDING

class CompanyRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    website: str = Field(..., pattern=r'^https?://.+')

class ScrapedData(BaseModel):
    company: Company
    website_content: str
    business_type: str
    key_features: List[str]
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)

class DatabaseColumn(BaseModel):
    name: str
    type: str = Field(..., pattern=r'^(string|number|boolean|date|json)$')
    nullable: bool
    description: str

class DatabaseTable(BaseModel):
    name: str
    columns: List[DatabaseColumn]
    primary_key: str
    description: str
    
    @validator('columns')
    def validate_columns(cls, v):
        if not v:
            raise ValueError('At least one column required')
        return v
    
    @validator('primary_key')
    def validate_primary_key(cls, v, values):
        if 'columns' in values:
            column_names = [col.name for col in values['columns']]
            if v not in column_names:
                raise ValueError(f'Primary key {v} must be one of the columns')
        return v

class DatabaseRelationship(BaseModel):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    type: str = Field(..., pattern=r'^(one-to-one|one-to-many|many-to-many|many-to-one)$')

class DatabaseSchema(BaseModel):
    tables: List[DatabaseTable]
    relationships: List[DatabaseRelationship]
    description: str
    
    @validator('tables')
    def validate_tables(cls, v):
        if len(v) < 2:
            raise ValueError('At least 2 tables required for a meaningful schema')
        return v

class GeneratedPrompt(BaseModel):
    prompt: str = Field(..., min_length=50, max_length=1000)
    expectedDashboard: str = Field(..., alias="expected_dashboard")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
    
    class Config:
        populate_by_name = True

class GTMResult(BaseModel):
    company: Company
    scrapedData: Dict[str, Any] = Field(..., alias="scraped_data")  # Changed to Dict for frontend compatibility
    schema: DatabaseSchema = Field(..., alias="database_schema")
    sampleData: Dict[str, List[Dict[str, Any]]] = Field(..., alias="sample_data")
    generatedPrompt: GeneratedPrompt = Field(..., alias="generated_prompt")
    
    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

class ProcessingStatus(BaseModel):
    company_id: str
    current_step: str
    progress: int = Field(..., ge=0, le=100)
    error: Optional[str] = None

class ProcessingResponse(BaseModel):
    company_id: str
    message: str
    company: Company