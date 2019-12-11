from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import sys
import bitstring as bs
import random
from random import randint
import json
import hashlib
import time

def generate_model(spec, complexity):
    b = bs.BitArray(spec)
    n_layers = b[0:3]
    sequences = [tf.keras.layers.Flatten(input_shape=(28, 28))]
    for i in n_layers:
        e = 17+i*14
        sequences.append(generate_layer(b[3:e].bin, complexity))
    return tf.keras.models.Sequential(sequences+[tf.keras.layers.Dropout(0.2),tf.keras.layers.Dense(10, activation='softmax')])

def generate_layer(spec, complexity):
    activation_fxns = ['relu']*7+['elu','exponential','hard_sigmoid','selu','linear','softmax','sigmoid', 'softsign','tanh']
    initializers = ['constant', 'glorot_normal']+['glorot_uniform']*7+['identity', 'ones', 'orthogonal', 'random_normal', 'random_uniform', 'zeros', 'truncated_normal']
    #todo - pad spec if needed
    b = bs.BitArray(bin=spec)
    use_bias = b[1]
    activation = activation_fxns[b[2:6].uint]
    kinitlize = initializers[b[6:10].uint]
    binitlize = initializers[b[10:14].uint]
    #print("Running model with bias "+str(use_bias)+", activation "+activation+", kernel init "+kinitlize+", bias init "+binitlize)
    return tf.keras.layers.Dense(128, activation=activation, use_bias=use_bias, kernel_initializer=kinitlize, bias_initializer=binitlize)

def generate_input_hash():
    """generates the input hash to the next block, based on the hash of the previous block and the transactions to be encoded"""
    #get the hash of the previous block
    bchain = {}
    with open('blockchain.json') as f:
        bchain = json.load(f)
    most_recent = max(bchain['blocks'], key=lambda x: x["timestamp"])
    hashy = most_recent['hash']
    #TODO - enforce that transactions should only contain the unconfirmed boys
    transactions = []
    with open('transactions.json') as f:
        transactions = json.load(f)
    stringy = str(transactions)+str(hashy)
    m = hashlib.md5()
    m.update(stringy)
    return '0x'+str(m.hexdigest()), str(transactions)

def write_unvalidated_problem(file_name, transactions, hashy):
    #writes an unvalidated problem so that it can be picked up by validators
    #todo - reconsider ID system
    solved_obj = {
        'timestamp': time.time(),
        'transactions': transactions,
        'problem_location': file_name,
        'output_hash': hashy,
        'pid': randint(0, 1000)
    }
    append_json('unvalidated-ledger.json', solved_obj, 'solved')
def fetch_unvalidated_problem():
    """fetches the location of the earliest unvalidated problem"""
    #todo - make sure to delete the problem from the unvalidated before moving to validated
    ledger = {}
    with open('unvalidated-ledger.json','r') as f:
        ledger = json.load(f)
        if (len(ledger['solved']) < 1):
               return False
        least_recent = min(ledger['solved'], key=lambda x: x["timestamp"])
        return least_recent['problem_location'], least_recent['pid'], least_recent['problem_location']
    
def write_solved_problem(file_location):
    #writes a solved problem to the problem ledger
    #TODO - add metadata
    solved_obj = {
        'timestamp': time.time(),
        'problem_location': file_location,
    }
    append_json('problem-ledger.json', solved_obj, 'solved')

def append_json(file_loc, obj, key):
    current = []
    pl = {}
    with open(file_loc, 'r+') as f:
        pl = json.load(f)
        current = pl[key]
        current.append(obj)
        f.seek(0)
        json.dump({key: current}, f)
        f.truncate()
def fetch_active_problem():
    meta = {}
    with open('active-problem/meta.json', 'r') as f:
        meta = json.load(f)
    if meta['test_file'] == "standin":
        print("Using stand in data")
        mnist = tf.keras.datasets.mnist
        (x_train, y_train), (x_test, y_test) = mnist.load_data()
        x_train, x_test = x_train / 255.0, x_test / 255.0
        return (x_train, y_train), (x_test, y_test)
    else:
        #TODO
        print("Whoooops")
        return
def get_threshold():
    """gets the performance threshold for the current problem"""
    meta = {}
    with open('active-problem/meta.json', 'r') as f:
        meta = json.load(f)
    return meta["threshold"]

def report_good_model(metadata):
    """reports that a model has been validated"""
    """Metadata includes problem ID, validator ID, timestamp"""
    append_json('confirmed-problems.json', metadata, 'confirmed')
    print("Good model reported!, looks like: "+metadata['location'])
