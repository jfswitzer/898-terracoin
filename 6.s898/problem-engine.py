#!/usr/bin/python
from time import sleep

def active_solved():
    #todo - implement
    return False
def main():
    #check if the active problem has been solved
    if not active_solved():
        print("not solved yet")
        return
    #if not, select a problem from the pool and make it the active problem
    #todo

if __name__ == '__main__':
    while (not sleep(5)):
        main()
