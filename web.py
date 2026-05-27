from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app=FastAPI()

class Task(BaseModel):
    task:str

@app.get('/')
def root():
    return FileResponse('dashboard/index.html')

@app.post('/run')
def run(task:Task):
    return {'result':f'Rigel Matrix processed: {task.task}'}
