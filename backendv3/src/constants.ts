export const systemPrompt = `My name is Bardia. I'm the founder of Olive (fromolive.com), an AI-powered internal tooling platform. Olive connects directly to a company's Postgres database and lets teams instantly generate full-featured internal tools—like dashboards, CRUD panels, and charts—just by describing what they need in natural language.

For example, a great use case is a payroll/compliance/bookkeeping company. This is an example of a service-oriented business wrapped by software. Think: they likely have people behind the scenes going into user's company accounts to add bookkeeping files, update numbers, look and mark transactions, etc. but the users use the product through a software. This is a great example where Olive would be great, because they can create and prompt for tools quickly that their teams can use.​ Obviously don't base responses around this, just want to show you the capabilities. It really depends on the actual company, this is just one example of one sector.

**IMPORTANT**: You have access to Neon MCP tools. You MUST use them to actually create a real Neon PostgreSQL database for this company. Here's your workflow:

1. First, analyze the company and understand their business
2. Design a realistic database schema that represents how their business operates  
3. Use the Neon MCP tools to create a new Neon project and database (in org id: org-summer-water-99276957)
4. Use the Neon MCP tools to create the tables with the schema you designed
5. Use the Neon MCP tools to populate the database with hundreds of rows of realistic sample data for each table
6. Get the connection string from the created database

You are responsible for:
- Predicting what a company's actual Postgres database likely contains based on their product and target customers
- Using Neon MCP to actually CREATE the database with realistic tables and columns  
- Using Neon MCP to POPULATE the database with hundreds of rows of highly varied, believable sample data
- Avoiding billing, behavior analytics, or things unlikely to be stored in the database

During generation of data, it is CRITICAL that there is a ton of data. For example, each table should have tens if not 100 etc rows. It should look like there is enough data. If there are foreign key relationships, there should NEVER be a case where one row's foreign key relationship is empty/there's no data. There should be data for EVERYTHING!!

Also, don't be stupid with data. If you're including numbers for example, don't include a total that will add up numbers from other tables, etc. Things that depend on each other easily break and should be calculated later in code, not hardcoded. For example say you're building a tool for a social media app. There should never be a field like "total comments" under a post because you can get that by just adding up the actual comment cells.

**You MUST actually create the database using Neon MCP tools during this conversation.**

After creating the database with Neon MCP, provide your final analysis in the following JSON format:

{
  "company_analysis": {
    "website": "website info",
    "business_description": "detailed description",
    "business_model": "how they make money",
    "target_customers": "who are their customers",
    "key_features": ["feature1", "feature2"],
    "likely_data_needs": ["data1", "data2"],
    "industry": "industry classification"
  },
  "connection_string": "the actual connection string from the Neon database you created",
  "database_info": {
    "project_id": "neon project id",
    "database_name": "database name",
    "schema": [
    {
      "table_name": <name of table>,
      "columns": { ... },
      "foreign_keys": { ... },
      "record_count": <count of records>
    },
    {
      "table_name": <name of table>,
      "columns": { ... },
      "foreign_keys": { ... },
      "record_count": <count of records>
    }
  ]
  }
}`;

export const userPrompt = ({ website }: { website: string }) => `Website: ${website}

Please analyze this company thoroughly and provide the comprehensive analysis as requested. 

IMPORTANT: You must use the Neon MCP tools to create a real database. If you don't have access to Neon MCP tools, please let me know immediately.'`



export const testOutputClaude = `
Perfect! I have successfully created a comprehensive Neon PostgreSQL database for WorkWeave with realistic data. Here's the final analysis:

{
          '{\n' +
          '  "company_analysis": {\n' +
          '    "website": "workweave.dev",\n' +
          '    "business_description": "WorkWeave (Weave) is an AI-powered engineering analytics platform that provides X-ray vision for engineering teams. They use AI and machine learning to analyze pull requests, measure engineering work output and quality, and provide actionable insights to optimize team productivity. The platform scans every PR, understands complexity and quality, and gives engineering leaders data-driven insights for team optimization.",\n' +
          '    "business_model": "B2B SaaS subscription platform targeting engineering leaders and teams. Revenue generated through tiered subscription plans (starter, professional, enterprise) based on team size and feature access.",\n' +
          '    "target_customers": "Engineering leaders, engineering managers, tech leads, and development teams of all sizes - from small 5-person startups to mid-market and enterprise organizations. Early adopters include Y Combinator companies and teams wanting to measure productivity impact of development tools.",\n' +
          '    "key_features": ["AI-powered pull request analysis", "Engineering work complexity scoring", "Code quality measurement", "Team productivity metrics and dashboards", "Integration with development tools (Cursor, Copilot, GitHub)", "Real-time insights for engineering stand-ups", "Performance impact measurement of development tools"],\n' +
          '    "likely_data_needs": ["Pull request metadata and code changes", "User and team information", "Repository and organization data", "Code review data and feedback", "AI analysis results and scoring", "Team and individual performance metrics", "Tool integration logs and impact measurements"],\n' +
          '    "industry": "Developer Tools & Engineering Productivity"\n' +
          '  },\n' +
          '  "connection_string": "postgresql://neondb_owner:npg_mqbC7fKN4WuV@ep-broad-darkness-ad17uuvj-pooler.c-2.us-east-1.aws.neon.tech/neondb?channel_binding=require&sslmode=require",\n' +
          '  "database_info": {\n' +
          '    "project_id": "sweet-bread-99231589",\n' +
          '    "database_name": "neondb",\n' +
          '    "schema": [\n' +
          '      {\n' +
          '        "table_name": "organizations",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "name": "VARCHAR(255) NOT NULL",\n' +
          '          "slug": "VARCHAR(100) UNIQUE NOT NULL",\n' +
          '          "github_organization": "VARCHAR(255)",\n' +
          
          "subscription_plan": "VARCHAR(50) DEFAULT 'starter'" +
          '          "team_size": "INTEGER",\n' +
          '          "industry": "VARCHAR(100)",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()",\n' +
          '          "updated_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {},\n' +
          '        "record_count": 10\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "users",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "organization_id": "UUID REFERENCES organizations(id)",\n' +
          '          "email": "VARCHAR(255) UNIQUE NOT NULL",\n' +
          '          "name": "VARCHAR(255) NOT NULL",\n' +
          '          "github_username": "VARCHAR(100)",\n' +
          '          "role": "VARCHAR(50) DEFAULT 'engineer'",\n' +
          '          "seniority_level": "VARCHAR(20) DEFAULT 'mid'",\n' +
          '          "team": "VARCHAR(100)",\n' +
          '          "timezone": "VARCHAR(50) DEFAULT 'UTC'",\n' +
          '          "is_active": "BOOLEAN DEFAULT true",\n' +
          '          "last_login_at": "TIMESTAMP WITH TIME ZONE",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()",\n' +
          '          "updated_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "organization_id": "organizations(id)"\n' +
          '        },\n' +
          '        "record_count": 45\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "repositories",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "organization_id": "UUID REFERENCES organizations(id)",\n' +
          '          "name": "VARCHAR(255) NOT NULL",\n' +
          '          "full_name": "VARCHAR(500) NOT NULL",\n' +
          '          "github_id": "BIGINT UNIQUE",\n' +
          '          "primary_language": "VARCHAR(50)",\n' +
          '          "is_private": "BOOLEAN DEFAULT true",\n' +
          '          "default_branch": "VARCHAR(100) DEFAULT 'main'",\n' +
          '          "description": "TEXT",\n' +
          '          "is_active": "BOOLEAN DEFAULT true",\n' +
          '          "last_analyzed_at": "TIMESTAMP WITH TIME ZONE",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()",\n' +
          '          "updated_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "organization_id": "organizations(id)"\n' +
          '        },\n' +
          '        "record_count": 52\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "pull_requests",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "repository_id": "UUID REFERENCES repositories(id)",\n' +
          '          "author_id": "UUID REFERENCES users(id)",\n' +
          '          "github_pr_number": "INTEGER NOT NULL",\n' +
          '          "github_pr_id": "BIGINT UNIQUE NOT NULL",\n' +
          '          "title": "TEXT NOT NULL",\n' +
          '          "description": "TEXT",\n' +
          '          "base_branch": "VARCHAR(100) DEFAULT 'main'",\n' +
          '          "head_branch": "VARCHAR(100) NOT NULL",\n' +
          '          "state": "VARCHAR(20) DEFAULT 'open'",\n' +
          '          "draft": "BOOLEAN DEFAULT false",\n' +
          '          "lines_added": "INTEGER DEFAULT 0",\n' +
          '          "lines_deleted": "INTEGER DEFAULT 0",\n' +
          '          "files_changed": "INTEGER DEFAULT 0",\n' +
          '          "commits_count": "INTEGER DEFAULT 1",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE NOT NULL",\n' +
          '          "updated_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()",\n' +
          '          "closed_at": "TIMESTAMP WITH TIME ZONE",\n' +
          '          "merged_at": "TIMESTAMP WITH TIME ZONE"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "repository_id": "repositories(id)",\n' +
          '          "author_id": "users(id)"\n' +
          '        },\n' +
          '        "record_count": 500\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "code_reviews",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "pull_request_id": "UUID REFERENCES pull_requests(id)",\n' +
          '          "reviewer_id": "UUID REFERENCES users(id)",\n' +
          '          "github_review_id": "BIGINT UNIQUE",\n' +
          '          "state": "VARCHAR(20) NOT NULL",\n' +
          '          "body": "TEXT",\n' +
          '          "comments_count": "INTEGER DEFAULT 0",\n' +
          '          "submitted_at": "TIMESTAMP WITH TIME ZONE NOT NULL",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "pull_request_id": "pull_requests(id)",\n' +
          '          "reviewer_id": "users(id)"\n' +
          '        },\n' +
          '        "record_count": 800\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "ai_analysis_results",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "pull_request_id": "UUID REFERENCES pull_requests(id)",\n' +
          '          "analysis_version": "VARCHAR(10) DEFAULT 'v1.0'",\n' +
          '          "work_complexity_score": "DECIMAL(4,2)",\n' +
          '          "work_type": "VARCHAR(50)",\n' +
          '          "estimated_hours": "DECIMAL(5,2)",\n' +
          '          "code_quality_score": "DECIMAL(4,2)",\n' +
          '          "test_coverage_impact": "VARCHAR(20)",\n' +
          '          "technical_debt_impact": "VARCHAR(20)",\n' +
          '          "risk_level": "VARCHAR(20) DEFAULT 'low'",\n' +
          '          "ai_confidence_score": "DECIMAL(4,2)",\n' +
          '          "analysis_notes": "TEXT",\n' +
          '          "processed_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "pull_request_id": "pull_requests(id)"\n' +
          '        },\n' +
          '        "record_count": 445\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "team_metrics",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "organization_id": "UUID REFERENCES organizations(id)",\n' +
          '          "team_name": "VARCHAR(100)",\n' +
          '          "metric_date": "DATE NOT NULL",\n' +
          '          "total_prs": "INTEGER DEFAULT 0",\n' +
          '          "merged_prs": "INTEGER DEFAULT 0",\n' +
          '          "avg_review_time_hours": "DECIMAL(6,2)",\n' +
          '          "avg_complexity_score": "DECIMAL(4,2)",\n' +
          '          "avg_quality_score": "DECIMAL(4,2)",\n' +
          '          "total_lines_added": "INTEGER DEFAULT 0",\n' +
          '          "total_lines_deleted": "INTEGER DEFAULT 0",\n' +
          '          "bug_fix_ratio": "DECIMAL(4,2)",\n' +
          '          "feature_development_ratio": "DECIMAL(4,2)",\n' +
          '          "team_velocity_score": "DECIMAL(6,2)",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "organization_id": "organizations(id)"\n' +
          '        },\n' +
          '        "record_count": 1200\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "user_daily_metrics",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "user_id": "UUID REFERENCES users(id)",\n' +
          '          "metric_date": "DATE NOT NULL",\n' +
          '          "prs_created": "INTEGER DEFAULT 0",\n' +
          '          "prs_merged": "INTEGER DEFAULT 0",\n' +
          '          "reviews_completed": "INTEGER DEFAULT 0",\n' +
          '          "lines_of_code_added": "INTEGER DEFAULT 0",\n' +
          '          "lines_of_code_deleted": "INTEGER DEFAULT 0",\n' +
          '          "avg_pr_complexity": "DECIMAL(4,2)",\n' +
          '          "avg_code_quality": "DECIMAL(4,2)",\n' +
          '          "time_spent_reviewing_hours": "DECIMAL(5,2)",\n' +
          '          "productivity_score": "DECIMAL(6,2)",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "user_id": "users(id)"\n' +
          '        },\n' +
          '        "record_count": 2000\n' +
          '      },\n' +
          '      {\n' +
          '        "table_name": "integration_logs",\n' +
          '        "columns": {\n' +
          '          "id": "UUID PRIMARY KEY",\n' +
          '          "organization_id": "UUID REFERENCES organizations(id)",\n' +
          '          "user_id": "UUID REFERENCES users(id)",\n' +
          '          "integration_type": "VARCHAR(50) NOT NULL",\n' +
          '          "event_type": "VARCHAR(50) NOT NULL",\n' +
          '          "pull_request_id": "UUID REFERENCES pull_requests(id)",\n' +
          '          "impact_score": "DECIMAL(4,2)",\n' +
          '          "metadata": "JSONB",\n' +
          '          "event_timestamp": "TIMESTAMP WITH TIME ZONE NOT NULL",\n' +
          '          "created_at": "TIMESTAMP WITH TIME ZONE DEFAULT NOW()"\n' +
          '        },\n' +
          '        "foreign_keys": {\n' +
          '          "organization_id": "organizations(id)",\n' +
          '          "user_id": "users(id)",\n' +
          '          "pull_request_id": "pull_requests(id)"\n' +
          '        },\n' +
          '        "record_count": 206\n' +
          '      }\n' +
          '    ]\n' +
          '  }\n' +
          '}\n' +
          '`