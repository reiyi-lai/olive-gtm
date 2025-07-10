# Olive GTM Engine

A workflow to research Olive's potential customers, generate their sample database schema, and create optimized dashboard prompts for Olive's platform.

## How It Works

1. **Input**: Enter company name and website URL
2. **Scraping**: Firecrawl API extracts clean website content
3. **Analysis**: OpenAI API analyzes business context and industry
4. **Schema Generation**: Creates realistic database schema
5. **Sample Data**: Generates business-relevant sample data
6. **Database Creation**: Creates PostgreSQL database with schema and populates with sample data
7. **Prompt Creation**: Builds Olive dashboard prompt

## Tech Stack

- **Frontend**: React, TypeScript, Tailwind CSS
- **Backend**: FastAPI, Python, Pydantic, PostgreSQL
- **AI Services**: OpenAI GPT-4, Firecrawl API
- **Storage**: Local JSON files, PostgreSQL databases (for now)

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (v16 or higher)
- npm or yarn
- PostgreSQL (v12 or higher)

### Installation

1. Clone the repository

2. Install and setup PostgreSQL:
   ```bash
   # macOS
   brew install postgresql
   brew services start postgresql
   ```

3. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with your API keys and database credentials
   ```
   
   Required environment variables:
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

### Running the Application

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

3. Open http://localhost:3000 in your browser

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
- Contains all tables from the inferred schema populated with sample data
- Enables live database queries and realistic demo experiences

## Architecture

```
Frontend (React) → Backend API (FastAPI) → AI Services → Local Storage + PostgreSQL
                                        ↓
                                   Firecrawl → OpenAI
```
