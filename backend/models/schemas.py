from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict
from enum import Enum
from pydantic import BaseModel

class CompanyStatus(str, Enum):
    PENDING = "pending"
    SCRAPING = "scraping"
    ANALYZING = "analyzing"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"

# Company data structure
class CompanyDict(TypedDict, total=False):
    id: str
    name: str
    website: str
    industry: Optional[str]
    status: CompanyStatus

# Company request structure (Pydantic for FastAPI)
class CompanyRequest(BaseModel):
    name: str
    website: str

# Company request structure (TypedDict for internal use)
class CompanyRequestDict(TypedDict):
    name: str
    website: str

# Scraped data structure
class ScrapedDataDict(TypedDict, total=False):
    company: CompanyDict
    website_content: str
    business_type: str
    key_features: List[str]
    description: str
    timestamp: str  # ISO format

# Database column structure
class DatabaseColumnDict(TypedDict):
    name: str
    type: str  # 'string', 'number', 'boolean', 'date', 'json'
    nullable: bool
    description: str

# Database table structure
class DatabaseTableDict(TypedDict):
    name: str
    columns: List[DatabaseColumnDict]
    primary_key: str
    description: str

# Database relationship structure
class DatabaseRelationshipDict(TypedDict):
    from_table: str
    from_column: str
    to_table: str
    to_column: str
    type: str  # 'one-to-one', 'one-to-many', etc.

# Database schema structure
class DatabaseSchemaDict(TypedDict):
    tables: List[DatabaseTableDict]
    relationships: List[DatabaseRelationshipDict]
    description: str

# Generated prompt structure
class GeneratedPromptDict(TypedDict):
    prompt: str
    expectedDashboard: str
    confidence: float
    reasoning: str


# Processing status structure
class ProcessingStatusDict(TypedDict, total=False):
    company_id: str
    current_step: str
    progress: int
    error: Optional[str]

