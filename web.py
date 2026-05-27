import subprocess
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from core.system_status import get_system_status
from core.orchestrator import process_task
from core.settings_store import public_settings, save_settings
from core.chat_memory import recent_messages, append_chat, clear_chat

app=FastAPI()
class Task(BaseModel): task:str
class Settings(BaseModel): data:dict
@app.get('/')
def root(): return FileResponse('dashboard/index.html')
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/status')
def status(): return get_system_status()
@app.get('/history')
def history(): return recent_messages()
@app.post('/history/clear')
def clear_history(): return clear_chat()
@app.get('/settings')
def settings(): return public_settings()
@app.post('/settings')
def update_settings(s:Settings): return save_settings(s.data)
@app.post('/run')
def run(task:Task):
    append_chat('user', task.task, agent='USER')
    result = process_task(task.task)
    if isinstance(result, dict):
        for agent, text in result.items():
            append_chat('assistant', text, agent=agent)
    else:
        append_chat('assistant', str(result), agent='RM-CEO')
    return result
@app.post('/update')
def update_from_github():
    try:
        result=subprocess.run(['/bin/bash','scripts/update_from_github.sh'],capture_output=True,text=True,timeout=180)
        return {'ok':result.returncode==0,'stdout':result.stdout,'stderr':result.stderr,'returncode':result.returncode}
    except Exception as e:
        return {'ok':False,'error':str(e)}