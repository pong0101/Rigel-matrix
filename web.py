import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.system_status import get_system_status
from core.orchestrator import process_task
from core.memory_store import recent_history
from core.settings_store import public_settings, save_settings

app=FastAPI()
class Task(BaseModel): task:str
class Settings(BaseModel): data:dict
@app.get('/')
def root(): return FileResponse('dashboard/index.html')
@app.get('/status')
def status(): return get_system_status()
@app.get('/history')
def history(): return recent_history()
@app.get('/settings')
def settings(): return public_settings()
@app.post('/settings')
def update_settings(s:Settings): return save_settings(s.data)
@app.post('/run')
def run(task:Task): return process_task(task.task)
@app.post('/update')
def update_from_github():
    try:
        result=subprocess.run(['git','pull'],capture_output=True,text=True,timeout=60)
        return {'ok':result.returncode==0,'stdout':result.stdout,'stderr':result.stderr,'returncode':result.returncode,'note':'Restart Rigel Matrix if Python files changed.'}
    except Exception as e:
        return {'ok':False,'error':str(e)}