requirements
user management id name mail
task management task id date priority

endpoints
get users
get tasks

filter queries based on user limit status priority 

tables 
user 
task

1. User Management
Create users with:
id
name
email (must be validated)
Prevent duplicate emails
2. Task Management
Each task should have:
task_id
title
description
status → (pending, in_progress, completed)
priority → (low, medium, high)
assigned_to (user_id)
due_date
created_at

3. API Endpoints (FastAPI)
User APIs
get all users 
add user
delete user

 
Task APIs
get tasks
4. Filtering & Querying
Add advanced query support:
Filter by:
status
priority
assigned user
Pagination (limit, offset)
Sort by due_date

add task
delete task
