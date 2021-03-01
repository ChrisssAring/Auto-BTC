import requests
import urllib
import json
import threading
import time
import utils
import btclog
import horsephrase

def run(name):
    print("{} started!".format(name))

    while True:

        private_keys = utils.generate_private_keys_random(100)
        #private_keys = utils.generate_private_keys_from_file(100)

        addresses = utils.private_key_to_public_address(private_keys)
        url = utils.public_address_list_to_url(addresses)
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req)
        data = response.read()
        values = json.loads(data)

        for i, address in enumerate(values['addresses']):
            message = "private:{},address:{},balance:{}".format(
                private_keys[i], addresses[i], address['final_balance'])
            log_message = "{},{}".format(name, message)
            btclog.log(log_message)

            if address['final_balance'] != 0 or address['n_tx'] != 0:
                print("BTC FOUND!")
                f = open("btc_found.txt", "a")
                f.write(message + "\n")
                f.close()

if __name__ == '__main__':

    num_threads = 12

    btclog = btclog.BtcLog()

    for x in range(num_threads):
        thread_name = "Thread-{}".format(x + 1)
        mythread = threading.Thread(target=run, args=(thread_name,))
        mythread.start()
