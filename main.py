from agents import build_default_agents
from hardware.adapters import get_device

print('Rigel Matrix booting...')
print(get_device())
for agent in build_default_agents():
    print(agent,'online')

while True:
    task=input('\nTask> ')
    if task=='exit':break
    for k,v in build_default_agents().items():
        print(f'[{k}] {v}: {task}')
