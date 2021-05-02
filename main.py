import threading
import utils
import btclog
import time

def BinarySearch(lys, val):
    first = 0
    last = len(lys)-1
    index = -1
    while (first <= last) and (index == -1):
        mid = (first+last)//2
        if lys[mid] == val:
            index = mid
        else:
            if val<lys[mid]:
                last = mid -1
            else:
                first = mid +1
    return index

def run(name):
    print("{} started!".format(name))

    while True:

        private_keys = utils.generate_private_keys_from_file(100)
        addresses = utils.private_key_to_public_address(private_keys)

        for i, address in enumerate(addresses):
            message = "private:{},address:{}".format(
                private_keys[i], address)
            log_message = "{},{}".format(name, message)

            btclog.log(log_message)

            if BinarySearch(mylist, address) > 0:
                print("BTC FOUND!", private_keys[i], address)
                f = open("btc_found.txt", "a")
                f.write(message + "\n")
                f.close()

if __name__ == '__main__':
    num_threads = 12

    btclog = btclog.BtcLog()

    time0 = time.perf_counter()

    with open('btc_latest_cleaned.txt') as f:
        mylist = [line.rstrip('\n') for line in f]

    time1 = time.perf_counter()
    print(f"Converted file to list in {time1 - time0:0.4f} seconds")
    mylist.sort()
    time2 = time.perf_counter()
    print(f"Sorted list in {time2 - time1:0.4f} seconds")

    for x in range(num_threads):
        thread_name = "Thread-{}".format(x + 1)
        mythread = threading.Thread(target=run, args=(thread_name,))
        mythread.start()
