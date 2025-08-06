# weave

## Company Summary
Research failed - unable to analyze company

**Industry**: Unknown  
**Business Model**: Unknown  
**Target Customers**: Unknown

## Database Schema
This schema represents a project management system with users, projects, tasks, comments, and user activities.

### Tables Created:
- **users**: stores information about users (2 rows)
- **projects**: stores information about projects (2 rows)
- **tasks**: stores information about tasks within projects (2 rows)
- **comments**: stores comments made on tasks (2 rows)
- **user_activity**: stores records of user activities (2 rows)

### Table Relationships:
The database maintains proper referential integrity with the following key relationships:
- tasks.project_id → projects.project_id (many-to-one)
- tasks.assigned_user_id → users.user_id (many-to-one)
- comments.task_id → tasks.task_id (many-to-one)
- comments.user_id → users.user_id (many-to-one)
- user_activity.user_id → users.user_id (many-to-one)

## Recommended Internal Tools

1. **Project Overview Dashboard**: Provides a comprehensive view of all projects, their status, and associated tasks. Allows managers to track project progress and identify bottlenecks.
2. **User Activity Monitor**: Tracks and displays user activities across the platform, helping to identify active users and monitor engagement levels.

## Database Connection
**Connection String**: `postgresql://neondb_owner:npg_Chcqbn5LS9wF@ep-small-unit-adp3y5yr.c-2.us-east-1.aws.neon.tech/olive_demo_weave?channel_binding=require&sslmode=require`

**Total Sample Data**: 10 rows across 5 tables


## 🚫 Olive Integration
**Status**: Failed to connect to Olive platform
**Note**: Ensure Olive is running locally on http://localhost:3000

To start Olive locally, run:
```bash
# In your Olive repository
npm install
npm run dev
```


---
*Generated with Olive GTM Engine - 2025-08-05 20:33:22*
