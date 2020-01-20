import minerb as m
import validatorb as v
import time
from random import randint
import matplotlib.pyplot as plt
import seaborn as sns

def benchmarking():
    print("Mining...")
    mining_times = []
    v_times = []
    for i in range(0,30):
        mining_times.append(m.check_mine())
        vid = randint(100, 10000) #generate a validator id
        v_times.append(v.check_validate(vid))
    print mining_times
    print v_times
    plt.figure("Mining latency")
    sns.distplot(mining_times, hist=False, kde=True,
                 bins=8, color = 'darkred',label="Mining latency (s)",
                 hist_kws={'edgecolor':'black'},
                 kde_kws={'linewidth': 2})
    plt.title("Mining latency")
    plt.ylabel("Probability density function", fontsize=16)
    plt.xlabel("Latency (in seconds)", fontsize=14)    
    #plt.legend()
    plt.show()

    plt.figure("Validation latency")
    sns.distplot(v_times, hist=False, kde=True,
                 bins=8, color = 'darkblue',label="Validation latency (s)",
                 hist_kws={'edgecolor':'black'},
                 kde_kws={'linewidth': 2})
    plt.title("Validation latency")
    plt.ylabel("Probability density function", fontsize=16)
    plt.xlabel("Latency (in seconds)", fontsize=14)    
    #plt.legend()
    plt.show()

benchmarking()
