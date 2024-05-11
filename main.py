from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId
from models.models import Project, Task

app = FastAPI()


from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://<username>:<password>@project-management.iejuwsk.mongodb.net/?retryWrites=true&w=majority&appName=project-management"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["task_manager"]
projects_col = db["projects"]
tasks_col = db["tasks"]

@app.post("/projects/")
async def create_project(project: Project):
    result = projects_col.insert_one(project.dict())
    return {"id": str(result.inserted_id)}

@app.get("/projects/")
async def get_projects():
    projects = []
    for project in projects_col.find():
        projects.append(Project(**project))
    return projects

@app.get("/projects/{project_id}")
async def get_project(project_id: str):
    project = projects_col.find_one({"_id": ObjectId(project_id)})
    if project:
        return Project(**project)
    raise HTTPException(status_code=404, detail="Project is not found")

@app.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    # Попытка удалить проект из базы данных
    result = projects_col.delete_one({"_id": ObjectId(project_id)})
    
    # Если проект не найден, возбуждаем исключение HTTP 404
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Возвращаем сообщение об успешном удалении
    return {"message": "Project deleted successfully"}

@app.post("/tasks/")
async def create_task(task: Task):
    result = tasks_col.insert_one(task.dict())
    return {"id": str(result.inserted_id)}

@app.get("/tasks/")
async def get_tasks():
    tasks = []
    for task in tasks_col.find():
        tasks.append(Task(**task))
    return tasks


@app.get("/tasks/{task_id}")
async def get_task(task_id: str):
    task = tasks_col.find_one({"_id": ObjectId(task_id)})
    if task:
        return Task(**task)
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    # Попытка удалить задачу из базы данных
    result = tasks_col.delete_one({"_id": ObjectId(task_id)})
    
    # Если задача не найдена, возбуждаем исключение HTTP 404
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Возвращаем сообщение об успешном удалении
    return {"message": "Task deleted successfully"}
