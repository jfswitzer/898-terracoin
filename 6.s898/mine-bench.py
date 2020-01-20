#!/usr/bin/python
from __future__ import absolute_import, division, print_function, unicode_literals
import tensorflow as tf
import sys
import bitstring as bs
import random
import utils as tu
from time import sleep
def mine():
    while (not sleep(5)):
        check_mine()
def check_mine():
    """mines the current boy"""
    (x_train, y_train), (x_test, y_test) = tu.fetch_active_problem()
    threshold = tu.get_threshold()
    hexy, transactions = tu.generate_input_hash()
    #train the model until the threshold is met
    i = 0
    c = 64
    a = 0
    while(a < threshold):
        if i > 5:
            print("Failed")
            return
        model = tu.generate_model(hexy, c)    
        model.compile(optimizer='adam',
                      loss='sparse_categorical_crossentropy',
                      metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=5)
        results = model.evaluate(x_test,  y_test, verbose=2)
        a = results[1]
        i += 1
        c = c*2

    #save the model
    fname = 'my_result'+str(random.randint(0,10000))+'.h5'
    model.save('unvalidated/'+fname)
    print("WROTE TO unvalidated/"+fname)
    tu.write_unvalidated_problem('unvalidated/'+fname, transactions, hexy)
