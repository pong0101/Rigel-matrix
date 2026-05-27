import json, os
CHAT_PATH=os.path.expanduser('~/.rigel/chat_memory.json')

def _ensure():
 os.makedirs(os.path.dirname(CHAT_PATH),exist_ok=True)
 if not os.path.exists(CHAT_PATH):
  with open(CHAT_PATH,'w') as f: json.dump({'messages':[]},f)

def load_chat():
 _ensure()
 with open(CHAT_PATH) as f:return json.load(f)

def append_chat(role,msg):
 d=load_chat();d['messages'].append({'role':role,'content':msg});d['messages']=d['messages'][-200:]
 with open(CHAT_PATH,'w') as f: json.dump(d,f)
 return d['messages']
