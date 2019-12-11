#!/usr/bin/python
from time import sleep
from random import randint
import json
import threading
import shutil
import time
import utils as tu
import hashlib
TRANSACTIONS = {}
TID = 0
TRANSACTIONS['transactions'] = []
SOLVED = []
def publish_transaction():
    global TID
    global TRANSACTIONS
    #mimics a real system by publishing a fake transaction every timestep
    #transactions don't persist when you run this multiple times
    source = randint(0, 1000)
    dest = randint(0, 1000)
    amt = randint(1, 10)
    TID += 1
    TRANSACTIONS['transactions'].append({
        'transaction_id': TID,
        'destination': dest,
        'source': source,
        'amount': amt
    })
    with open('transactions.json', 'w') as f:
        json.dump(TRANSACTIONS, f)
def check_confirmed():
    print("Checking for confirmed")
    confirmation_threshold = 1 #todo - this needs to be based on number of nodes in the network
    with open('confirmed-problems.json', 'r') as f:
        confirmed = json.load(f)['confirmed']
        print("Confirmed looks like: "+str(confirmed))
        counts = {}
        meta = {}
        for m in confirmed:
            id = m['pid']
            validators = counts.get(id, set())
            validators.add(m['vid'])
            counts[id] = validators
            meta[id] = m
        for key, value in counts.items():
            if len(value) >= confirmation_threshold:
                return meta[key]
    return False
        
def generate_block_hash(model):
    #todo - hash includes the previous hash, the solved model
    #todo - definitely not cryptographically secure
    m = hashlib.md5()
    model_text = ""
    with open(model['location'], 'r') as f:
        model_text = f.read()
    instring = model_text+str(tu.generate_input_hash()[0])
    print("INSTRING LOOKS LIKE: "+instring)
    m.update(instring)
    return str(m.hexdigest())
def write_validated(model):
    global SOLVED
    if model['pid'] in SOLVED:
        return
    SOLVED.append(model['pid'])
    block = {
        'timestamp': time.time(),
        'hash': model['hashy'],
        'transactions': model['transactions'],
        'pid': model['pid'],
    }
    #move the problem to the correct location
    old_loc = model['location']
    new_loc = "solved-problems/"+old_loc.split("/")[-1]
    shutil.copy(old_loc, new_loc)
    
    #update the blockchain
    tu.write_solved_problem(new_loc)
    tu.append_json('blockchain.json', block, 'blocks')
    clean_up()

def clean_up():
    #clear everything that should be cleared after a block is mined
    #todo - clear the unvalidated folder
    with open('confirmed-problems.json', 'w') as f:
        reset = {'confirmed': []}
        json.dump(reset, f)
    with open('unvalidated-ledger.json', 'w') as f:
        reset = {'solved': []}
        json.dump(reset, f)
    print("CLEANED UP")
    #todo (eventually) - clear the active problem and fetch a new one
    
def transaction_generator():
    while (not sleep(20)):
        publish_transaction()
        
def check_validated():
    while (not sleep(12)):
        confirmed = check_confirmed()
        if confirmed:
            write_validated(confirmed)
            

