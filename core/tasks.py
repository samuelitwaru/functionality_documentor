from background_task import background


@background(schedule=2)
def run_task(name):
    print('starting...', name)
    with open('2.txt', 'w') as fh:
        fh.write('text')
    import time
    time.sleep(5)
    print('completed')