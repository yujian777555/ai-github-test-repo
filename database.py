"""
Database operations module.
Intentionally contains SQL injection and other database issues.
"""

import sqlite3
from typing import Optional, List, Dict, Any

DATABASE_PATH = "tasks.db"


def get_db() -> sqlite3.Connection:
    """Get database connection."""
    db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db


def init_db():
    """Initialize database with tables."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #7: No schema versioning or migrations
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'medium',
            status TEXT DEFAULT 'pending',
            slug TEXT UNIQUE,
            created_by TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # No indexes on frequently queried columns
    db.commit()
    db.close()


def create_task(title: str, description: str, priority: str, slug: str, created_by: str) -> int:
    """Create a new task."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #8: SQL Injection - string formatting
    query = f"""
        INSERT INTO tasks (title, description, priority, slug, created_by)
        VALUES ('{title}', '{description}', '{priority}', '{slug}', '{created_by}')
    """
    
    cursor.execute(query)
    task_id = cursor.lastrowid
    db.commit()
    db.close()
    return task_id


def get_task(task_id: int) -> Optional[Dict[str, Any]]:
    """Get a task by ID."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #9: SQL Injection - string formatting
    cursor.execute(f"SELECT * FROM tasks WHERE id = {task_id}")
    row = cursor.fetchone()
    db.close()
    
    return dict(row) if row else None


def list_tasks(status: str = None, priority: str = None, limit: int = 100) -> List[Dict[str, Any]]:
    """List tasks with optional filtering."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #10: SQL Injection in filter building
    query = "SELECT * FROM tasks WHERE 1=1"
    if status:
        query += f" AND status = '{status}'"
    if priority:
        query += f" AND priority = '{priority}'"
    query += f" LIMIT {limit}"
    
    cursor.execute(query)
    rows = cursor.fetchall()
    db.close()
    
    return [dict(row) for row in rows]


def update_task(task_id: int, **kwargs) -> bool:
    """Update a task."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #11: SQL Injection in dynamic UPDATE
    set_clause = ", ".join([f"{k} = '{v}'" for k, v in kwargs.items()])
    query = f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = {task_id}"
    
    cursor.execute(query)
    db.commit()
    db.close()
    return True


def delete_task(task_id: int) -> bool:
    """Delete a task."""
    db = get_db()
    cursor = db.cursor()
    
    # VULNERABILITY #12: No soft delete - data permanently lost
    cursor.execute(f"DELETE FROM tasks WHERE id = {task_id}")
    db.commit()
    affected = cursor.rowcount
    db.close()
    return affected > 0
