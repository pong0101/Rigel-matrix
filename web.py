from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.system_status import get_system_status
from core.orchestrator import process_task
from core.memory_store import recent_history

app=FastAPI()
class Task(BaseModel): task:str
@app.get('/')
def root(): return FileResponse('dashboard/index.html')
@app.get('/status')
def status(): return get_system_status()
@app.get('/history')
def history(): return recent_history()
@app.post('/run')
def run(task:Task): return process_task(task.task)