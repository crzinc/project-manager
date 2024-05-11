from pydantic import BaseModel
from typing import List,Optional

class Project(BaseModel):
    name: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class Task(BaseModel):
    name: str
    description: Optional[str]
    status: str
    priority: str
    project_id: str

