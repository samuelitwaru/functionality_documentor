from background_task import background


@background(schedule=1)
def run_task(name):
    print('starting...', name)
    with open('2.txt', 'w') as fh:
        fh.write('text')
    import time
    time.sleep(5)
    print('completed')


@background(schedule=1)
def update_app_files(name):
    
    print('starting...', name)
    with open('2.txt', 'w') as fh:
        fh.write('text')
    import time
    time.sleep(5)
    print('completed')