# Olive Outbound Engine

A workflow to research Olive's potential customers, generate their sample database schema, and create optimized dashboard prompts for Olive's platform.

![Olive GTM Engine Workflow](./README-img.png)

## Steps

1. **Lead Info Input**: Enter company name and website URL
2. **Web Scraping**: Firecrawl API extracts clean website content
3. **Business Analysis**: OpenAI API analyzes business context and industry
4. **Data Schema Generation**: Creates realistic database schema
5. **Sample Data Generation**: Generates business-relevant sample data
6. **Database Creation**: Creates PostgreSQL database with schema and populates with sample data
7. **Prompt Creation**: Builds Olive dashboard prompt

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, PostgreSQL
- **AI Services**: OpenAI API, Firecrawl API
- **Storage**: Local JSON files, PostgreSQL databases (for now)

## Installation

1. Clone the repository

2. Install and setup PostgreSQL:
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   ```

3. Set up environment variables in `backend/.env`:
    ```env
   # OpenAI API Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Firecrawl API Configuration  
   FIRECRAWL_API_KEY=your_firecrawl_api_key_here
   
   # PostgreSQL Database Configuration
   POSTGRES_HOST=
   POSTGRES_PORT=
   POSTGRES_USER=
   POSTGRES_PASSWORD=
   POSTGRES_ADMIN_DB=
   ```

4. Install backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

5. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

### Run the Application

1. Start the FastAPI backend server:
   ```bash
   cd backend
   python run.py
   ```

2. Start the React frontend development server:
   ```bash
   cd frontend
   npm start
   ```

3. Open http://localhost:3000

## API Endpoints

- `POST /api/gtm/process-company` - Start processing a company
- `GET /api/gtm/status/:companyId` - Get processing status
- `GET /api/gtm/result/:companyId` - Get complete results

## Data Storage

Results are stored in multiple locations:

### Local JSON Files
- `data/companies/{company-id}/scraped-data.json` - Website content and business analysis
- `data/companies/{company-id}/inferred-schema.json` - Generated database schema
- `data/companies/{company-id}/sample-data.json` - Generated sample data
- `data/companies/{company-id}/database-info.json` - PostgreSQL connection details
- `data/companies/{company-id}/generated-prompt.json` - Olive dashboard prompt

### PostgreSQL Databases
- Each company gets its own PostgreSQL database: `olive_gtm_{company_name}`

## Architecture

```
Frontend (React) → Backend API (FastAPI) → AI Services → Local Storage + PostgreSQL
                                        ↓
                                   Firecrawl → OpenAI
```
