# Task Manager API

A simple FastAPI-based task management system.

## Features

- Create, read, update, delete tasks
- Priority-based task organization
- Simple authentication
- Admin statistics dashboard

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/login | User login |
| POST | /tasks | Create task |
| GET | /tasks | List tasks |
| GET | /tasks/{id} | Get task |
| PUT | /tasks/{id} | Update task |
| DELETE | /tasks/{id} | Delete task |
| GET | /admin/stats | Admin statistics |

## Authentication

Default users:
- `admin` / `admin123`
- `user1` / `password123`

## Project Structure

```
task-manager/
├── main.py          # FastAPI application entry
├── auth.py          # Authentication logic
├── database.py      # Database operations
├── models.py        # Pydantic models
├── utils.py         # Utility functions
├── config.py        # Configuration
├── requirements.txt # Dependencies
└── tests/           # Test files
```

## License

MIT
test

## Update
This file was modified by ChatGPT via GitHub Connector.
