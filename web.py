from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.system_status import get_system_status

app=FastAPI()
class Task(BaseModel):
    task:str
@app.get('/')
def root(): return FileResponse('dashboard/index.html')
@app.get('/status')
def status(): return get_system_status()
@app.post('/run')
def run(task:Task): return {'result':f'Rigel Matrix processed: {task.task}'}