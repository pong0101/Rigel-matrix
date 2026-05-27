print('Rigel Matrix booting...')
print('RM-CEO online')
print('RM-ENG online')
print('RM-ANL online')
print('RM-DSN online')
print('RM-MEM online')

while True:
    task = input('\nTask> ')
    if task.lower() == 'exit':
        break
    print(f'Processing: {task}')
