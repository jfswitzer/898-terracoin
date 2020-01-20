#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import sys
import bitstring as bs
import random
from random import randint
import utils as tu
import time
from time import sleep

def validate():
    vid = randint(100, 10000) #generate a validator id
    while( not sleep(4)):
        check_validate(vid)

def check_validate(vid):
    print("VALIDATING")
    unvalidated = tu.fetch_unvalidated_problem()
    if not unvalidated:
        return
    trained_model, model_id, problem_location = unvalidated
    saved_model = tf.keras.models.load_model(trained_model)

    (x_train, y_train), (x_test, y_test) = tu.fetch_active_problem()

    threshold = tu.get_threshold()
    hashy, transactions = tu.generate_input_hash()
    s = time.time()
    #check that the parameterization is what it should be
    if not check_params(saved_model, hashy):
        return False
    #check that the performance is what it should be
    if not check_performance(saved_model, threshold,x_test,y_test):
        return False
    e = time.time()
    #if both check out, the model is good
    metadata = {
        'pid': model_id,
        'vid': vid,
        'timestamp': time.time(),
        'location': problem_location,
        'hashy': hashy,
        'transactions': transactions,
    }
    print("REPORTING GOOD AT: "+problem_location)
    tu.report_good_model(metadata)
    return e - s
def check_params(model, hashy):
    #mb - decouple from actual model creation/complexity
    generated_model = tu.generate_model(hashy,64)
    #mb - is this the best check?
    og = ""
    ng = ""
    sys.stdout = open('tmp1', 'w')
    retval = model.summary()
    with open('tmp1','r') as f:
        og = f.read()
    sys.stdout = open('tmp2', 'w')
    generated_model.summary()
    with open('tmp2', 'r') as f:
        ng = f.read()
    sys.stdout = sys.__stdout__
    open('tmp1', 'w').close()
    open('tmp2', 'w').close()
    if og == ng:
        print("Parameterization test passed")
        return True
    print("Parameterization test failed")
    return False

def check_performance(model, threshold,x_test,y_test):
    results = model.evaluate(x_test,y_test,verbose=0)
    perf = results[1]
    if perf >= threshold:
        print("Performance test passed")
        return True
    print("Performance test failed")
    return False

