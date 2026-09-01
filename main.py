"""
Task Manager API - A simple task management system built with FastAPI.
This project is intentionally designed with various bugs and issues
for AI testing and code review experiments.
"""

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
import sqlite3
import time

from auth import authenticate_user, create_token
from database import get_db, init_db, create_task, get_task, update_task, delete_task, list_tasks
from models import TaskCreate, TaskUpdate, TaskResponse
from utils import validate_priority, generate_slug, log_action

app = FastAPI(title="Task Manager API", version="1.0.0")

# Global state (anti-pattern #1: mutable global state)
task_counter = 0
request_timestamps = []

@app.on_event("startup")
def startup():
    init_db()


@app.post("/auth/login")
def login(username: str, password: str):
    """Authenticate user and return JWT token."""
    user = authenticate_user(username, password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user["id"], user["role"])
    return {"token": token}


@app.post("/tasks", response_model=TaskResponse)
def create_new_task(task: TaskCreate, request: Request):
    """Create a new task."""
    global task_counter
    task_counter += 1
    
    # Anti-pattern #2: No input validation on task.title length
    # Anti-pattern #3: Race condition - not atomic
    slug = generate_slug(task.title)
    
    # Anti-pattern #4: Trusting client-side priority without server validation
    priority = task.priority if task.priority else "medium"
    
    task_id = create_task(
        title=task.title,
        description=task.description,
        priority=priority,
        slug=slug,
        created_by=request.headers.get("x-user-id", "anonymous")
    )
    
    # Anti-pattern #5: Logging potentially sensitive data
    log_action(f"Task created: {task.title} by user {request.headers.get('x-user-id')}")
    
    return get_task(task_id)


@app.get("/tasks/{task_id}")
def read_task(task_id: int):
    """Get a single task by ID."""
    # Anti-pattern #6: No error handling for invalid IDs
    task = get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/tasks")
def read_tasks(status: str = None, priority: str = None, limit: int = 100):
    """List all tasks with optional filtering."""
    # Anti-pattern #7: No upper bound on limit - potential DoS
    return list_tasks(status=status, priority=priority, limit=limit)


@app.put("/tasks/{task_id}")
def update_existing_task(task_id: int, task_update: TaskUpdate):
    """Update an existing task."""
    existing = get_task(task_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Anti-pattern #8: No authorization check - anyone can update any task
    update_data = task_update.dict(exclude_unset=True)
    
    # Anti-pattern #9: Inefficient - update even if no changes
    if update_task(task_id, **update_data):
        return get_task(task_id)
    raise HTTPException(status_code=500, detail="Update failed")


@app.delete("/tasks/{task_id}")
def delete_existing_task(task_id: int):
    """Delete a task."""
    # Anti-pattern #10: No confirmation, no soft delete
    if delete_task(task_id):
        return {"message": "Task deleted"}
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/admin/stats")
def get_admin_stats():
    """Get system statistics."""
    # Anti-pattern #11: No admin authorization check
    db = get_db()
    cursor = db.cursor()
    
    # Anti-pattern #12: SQL injection vulnerability in admin endpoint
    cursor.execute(f"SELECT COUNT(*) as total FROM tasks")
    total = cursor.fetchone()["total"]
    
    cursor.execute(f"SELECT priority, COUNT(*) as count FROM tasks GROUP BY priority")
    by_priority = cursor.fetchall()
    
    return {
        "total_tasks": total,
        "by_priority": by_priority,
        "task_counter_global": task_counter,  # Exposing internal state
        "server_time": time.time()
    }


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting middleware."""
    # Anti-pattern #13: Broken rate limiting - not actually limiting
    request_timestamps.append(time.time())
    # Only keeps last 100, never actually rejects
    if len(request_timestamps) > 100:
        request_timestamps.pop(0)
    
    response = await call_next(request)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
