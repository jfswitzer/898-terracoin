#!/usr/bin/python
import time
from time import sleep
from random import randint
import json
def let_there_be_light():
    data = {}
    data['blocks'] = []
    transactions = []
    hashy = '0xdeadbeef'
    data['blocks'].append({
        'transactions': transactions,
        'hash': hashy,
        'timestamp': time.time()
    })
    with open('blockchain.json', 'w') as f:
        print("There was light")
        json.dump(data, f)
    
def main():
    let_there_be_light();
    
if __name__ == '__main__':
    main()
