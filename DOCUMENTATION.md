# Documentation

## Data Flow & Transformations

### Processing Pipeline

```
1. Website Scraping (10%)    → scraped_data.json
2. Schema Inference (30%)    → inferred_schema.json  
3. Sample Data Generation (50%) → sample_data.json
4. Database Creation (70%)   → database_info.json
5. Prompt Generation (90%)   → generated_prompt.json
```

### Data Transformations

#### Stage 1: Website Scraping
```
Input: Company name + website URL
↓
Firecrawl API: Extract clean website content (markdown)
↓
OpenAI Analysis: Business type, key features, description
↓
Output: ScrapedData object with structured business intelligence
```

#### Stage 2: Schema Inference
```
Input: ScrapedData (business context)
↓
OpenAI GPT-4: Generate realistic database schema based on business type
↓
Validation: Ensure proper table relationships and data types
↓
Output: DatabaseSchema with tables, columns, and relationships
```

#### Stage 3: Sample Data Generation
```
Input: DatabaseSchema + ScrapedData (for context)
↓
OpenAI GPT-4: Generate realistic sample data matching schema
↓
Validation: Ensure referential integrity and realistic values
↓
Output: Dictionary of table data {table_name: [row_objects]}
```

#### Stage 4: Database Creation
```
Input: DatabaseSchema + Sample Data + Company info
↓
PostgreSQL Operations:
  - Create database: olive_gtm_{company_name}
  - Create tables with proper types and constraints
  - Insert sample data with JSON conversion for dict fields
  - Create foreign key relationships
↓
Output: Connection info with database details
```

#### Stage 5: Prompt Generation
```
Input: DatabaseSchema + Sample Data + ScrapedData
↓
OpenAI GPT-4: Generate optimized dashboard prompt for Olive
↓
Validation: Ensure prompt quality and actionable insights
↓
Output: GeneratedPrompt with prompt, expected dashboard, confidence
```

### Data Format Transformations

#### JSON to Pydantic Models
```python
# File loading
scraped_data_dict = json.load(file)

# DateTime reconstruction
scraped_data_dict['timestamp'] = datetime.fromisoformat(scraped_data_dict['timestamp'])

# Pydantic validation
scraped_data = ScrapedData(**scraped_data_dict)
```

#### Pydantic to Frontend (camelCase conversion)
```python
# Manual field mapping for frontend compatibility
scraped_data_frontend = {
    "company": scraped_data_obj.company.dict(),
    "websiteContent": scraped_data_obj.website_content,
    "businessType": scraped_data_obj.business_type,
    "keyFeatures": scraped_data_obj.key_features,
    "description": scraped_data_obj.description,
    "timestamp": scraped_data_obj.timestamp.isoformat()
}
```

## API Documentation

### Base URL
```
Development: http://localhost:8000/api/gtm
```

### 1. Process Company

**Endpoint:** `POST /process-company`

**Description:** Initiates GTM processing pipeline for a company.

**Request Example:**
```json
{
  "name": "Scribe",
  "website": "https://scribehow.com"
}
```

**Server Processing:**
1. Sanitize company name for folder creation
2. Check for existing company data (resume functionality)
3. Create Company object with PENDING status
4. Initialize processing status tracking
5. Start background processing pipeline
6. Return immediate response with company_id

**Response Example:**
```json
{
  "company_id": "scribe",
  "message": "Processing started",
  "company": {
    "id": "scribe", 
    "name": "Scribe",
    "website": "https://scribehow.com",
    "industry": null,
    "status": "pending"
  }
}
```

**Error Responses:**
- `422`: Validation error (invalid URL, missing fields)
- `500`: Internal server error

### 2. Get Processing Status

**Endpoint:** `GET /status/{company_id}`

**Description:** Retrieves the current processing status for a company.

**URL Parameters:**
- `company_id` (string, required): Company identifier

**Server Processing:**
1. Lookup company_id in in-memory processing status
2. Return current progress and step information

**Response Example:**
```json
{
  "companyId": "scribe",
  "currentStep": "Creating PostgreSQL database...",
  "progress": 70,
  "error": null
}
```

**Error Responses:**
- `404`: Company not found in processing queue

### 3. Get Results

**Endpoint:** `GET /result/{company_id}`

**Description:** Retrieves complete GTM analysis results for a processed company.

**URL Parameters:**
- `company_id` (string, required): Company identifier

**Server Processing:**
1. Load all stage results from JSON files
2. Reconstruct Pydantic models for validation
3. Convert to frontend-compatible format (camelCase)
4. Include database connection info if available
5. Return comprehensive results object

**Response Format:**
```json
{
  "company": {
    "id": "string",
    "name": "string", 
    "website": "string",
    "industry": "string | null",
    "status": "string"
  },
  "scrapedData": {
    "company": "Company",
    "websiteContent": "string",
    "businessType": "string",
    "keyFeatures": ["string"],
    "description": "string",
    "timestamp": "string (ISO format)"
  },
  "schema": {
    "tables": [
      {
        "name": "string",
        "columns": [
          {
            "name": "string",
            "type": "string|number|boolean|date|json",
            "nullable": "boolean",
            "description": "string"
          }
        ],
        "primaryKey": "string",
        "description": "string"
      }
    ],
    "relationships": [
      {
        "fromTable": "string",
        "fromColumn": "string", 
        "toTable": "string",
        "toColumn": "string",
        "type": "one-to-one|one-to-many|many-to-many|many-to-one"
      }
    ],
    "description": "string"
  },
  "sampleData": {
    "table_name": [
      {
        "column_name": "value",
        "...": "..."
      }
    ]
  },
  "generatedPrompt": {
    "prompt": "string",
    "expectedDashboard": "string", 
    "confidence": "number (0.0-1.0)",
    "reasoning": "string"
  },
  "databaseInfo": {
    "database_name": "string",
    "host": "string",
    "port": "string",
    "username": "string", 
    "connection_string": "string",
    "created_tables": ["string"],
    "total_rows": "number"
  }
}
```

**Error Responses:**
- `404`: Results not found or processing not complete
- `500`: Error loading or processing results

## Data Models

### Core Pydantic Models

#### Company
```python
class Company(BaseModel):
    id: str
    name: str
    website: str
    industry: Optional[str] = None
    status: CompanyStatus = CompanyStatus.PENDING
```

#### ScrapedData
```python
class ScrapedData(BaseModel):
    company: Company
    website_content: str
    business_type: str
    key_features: List[str]
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)
```

#### DatabaseSchema
```python
class DatabaseSchema(BaseModel):
    tables: List[DatabaseTable]
    relationships: List[DatabaseRelationship]
    description: str
```

#### DatabaseTable
```python
class DatabaseTable(BaseModel):
    name: str
    columns: List[DatabaseColumn]
    primary_key: str
    description: str
```

#### GeneratedPrompt
```python
class GeneratedPrompt(BaseModel):
    prompt: str = Field(..., min_length=50, max_length=1000)
    expectedDashboard: str = Field(..., alias="expected_dashboard")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str
```
## PostgreSQL Database Structure

Each company gets a separate PostgreSQL database named `olive_gtm_{company_name}`.

#### Database Creation Process
1. **Sanitize company name** for valid PostgreSQL database name
2. **Check database existence** to avoid conflicts
3. **Create database** with autocommit isolation level
4. **Create tables** based on inferred schema with proper PostgreSQL types
5. **Create foreign key relationships** with conflict checking
6. **Insert sample data** with JSON conversion for dict fields

#### Type Mapping
```python
Schema Type → PostgreSQL Type
"string"   → TEXT
"number"   → NUMERIC  
"boolean"  → BOOLEAN
"date"     → TIMESTAMP
"json"     → JSONB
```

#### Connection Information Storage
Database details are stored in `database_info.json`:
```json
{
  "database_name": "olive_gtm_scribe",
  "host": "localhost", 
  "port": "5432",
  "username": "postgres",
  "connection_string": "postgresql://user@localhost:5432/olive_gtm_scribe",
  "created_tables": ["users", "subscriptions", "documents"],
  "total_rows": 145
}
```

### Resume Functionality

The system implements comprehensive resume functionality:

1. **Stage Detection**: Checks for existing files to determine last completed stage
2. **Automatic Resume**: Skips completed stages and continues from failure point
3. **Data Integrity**: Each stage saves immediately upon completion
4. **Error Recovery**: Failed stages can be retried without losing previous work

This prevents data loss during development and reduces API costs by avoiding unnecessary re-processing. 