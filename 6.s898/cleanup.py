import json
import os
import glob

files = glob.glob('unvalidated/*')
for f in files:
    os.remove(f)
files = glob.glob('solved-problems/*')
for f in files:
    os.remove(f)

with open('problem-ledger.json','w') as f:
    json.dump({'solved': []}, f)
with open('confirmed-problems.json','w') as f:
    json.dump({'confirmed': []}, f)
with open('unvalidated-ledger.json','w') as f:
    json.dump({'solved': []}, f)

with open('transactions.json','w') as f:
    json.dump({'transactions': []}, f)

with open('blockchain.json', 'w') as f:
    gen = {"blocks": [{"timestamp": 1575237938.423886, "hash": "0xbeefdead", "transactions": ""}]}
    json.dump(gen, f)
