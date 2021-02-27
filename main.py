import requests
import urllib
import json
import threading

#!/usr/bin/python3

import threading
import time

from utils import get_address

def run(name):
    print("{} started!".format(name))

    while True:

        private_key = bitlib.BitGen.generate_private_key()
        wif = bitlib.BitGen.private2wif(private_key)
        address = bitlib.BitGen.private2address(private_key)
        balance = bitnet.get_balance(address)

        url = "https://api.smartbit.com.au/v1/blockchain/address/1BvvRfz4XnxSWJ524TusetYKrtZnAbgV3r,1LdRcdxfbSnmCYYNdeYpUnztiYzVfBEQeC"

        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        values = json.loads(data)

        if not values['success']:
            return 0

        for address in values['addresses']:
            if address['confirmed']['balance'] != "0.00000000":
                print("test1")


def main():
    url = "https://api.smartbit.com.au/v1/blockchain/address/1BvvRfz4XnxSWJ524TusetYKrtZnAbgV3r,1LdRcdxfbSnmCYYNdeYpUnztiYzVfBEQeC"

    req = urllib.request.Request(url)
    response = urllib.request.urlopen(req)
    data = response.read()
    values = json.loads(data)

    if not values['success']:
        return 0

    for address in values['addresses']:
        if address['confirmed']['balance'] != "0.00000000":
            print("test1")

    #if values['addresses'][0]['confirmed']['balance'] != "0.00003600":
    #print(values['addresses'][0]['confirmed']['balance'])

if __name__ == '__main__':
    for x in range(2):
        thread_name = "Thread-{}".format(x + 1)
        mythread = threading.Thread(target=run, args=(thread_name,))
        mythread.start()

#curl "https://api.smartbit.com.au/v1/blockchain/address/1BvvRfz4XnxSWJ524TusetYKrtZnAbgV3r37XuVSEpWW4trkfmvWzegTHQt7BdktSKUs,5Jx8yk7EAAYB5g9CYm1aFpG4ckRCFm13Q76eE1TpPGzanh39Lfp"
