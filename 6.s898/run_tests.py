import miner
import validator
import teng as eng
import threading

if __name__ == '__main__':
    #spawn all threads
    tasks = [eng.transaction_generator,eng.check_validated, miner.mine, validator.validate]
    for task in tasks:
        t = threading.Thread(target=task)
        t.start()
