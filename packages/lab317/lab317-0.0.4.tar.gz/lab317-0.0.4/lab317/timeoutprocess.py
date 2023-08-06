import multiprocessing


def func(item, return_val):
    return_val[item] = 'timeout'
    sleep(item)
    return_val[item] = 'Done'
    return 

def timeout_process(item, func, TIMEOUT):
    manager = multiprocessing.Manager()
    return_val = manager.dict()
    proc = multiprocessing.Process(target=func, args=(item,return_val,))
    proc.start()
    
    sec = 0
    
    while sec <= TIMEOUT:
        sleep(1)
        sec+=1
        if not proc.is_alive():
            break


    if proc.is_alive():
        proc.terminate()

    proc.join()

    results = dict(return_val)

    return results
