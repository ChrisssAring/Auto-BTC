import base58
import hashlib
import binascii
import os
import ecdsa
import logging
import codecs
import horsephrase
from logging.handlers import RotatingFileHandler

def generate_private_keys_random(number_of_keys):
    private_keys = []
    for i in range(number_of_keys):
        private_keys.append(binascii.hexlify(os.urandom(32)).decode())
    return private_keys

def generate_private_keys_from_file(number_of_keys):
    private_keys = []
    for i in range(number_of_keys):
        input_password_bytes = codecs.encode(horsephrase._implementation.generate(), "utf-8")
        private_key = hashlib.sha256(input_password_bytes).hexdigest()
        private_key_bytes = codecs.decode(private_key, "hex") #Type bytes
        private_keys.append(private_key_bytes.hex())
    return private_keys

def ripemd160(hash):
    ripemd = hashlib.new('ripemd160')
    ripemd.update(hash)
    return ripemd

def private_key_to_public_address(private_keys):
    addresses = []
    for private_key in private_keys:
        private_key = binascii.unhexlify(private_key)
        signing_key = ecdsa.SigningKey.from_string(
            private_key, curve=ecdsa.SECP256k1)
        verifying_key = signing_key.get_verifying_key()
        public_key = '04' + binascii.hexlify(
            verifying_key.to_string()).decode()
        hash160 = ripemd160(hashlib.sha256(
            binascii.unhexlify(public_key)).digest()).digest()
        main_net_key = b"\x00" + hash160
        checksum = hashlib.sha256(hashlib.sha256(
            main_net_key).digest()).digest()[:4]
        public_address = base58.b58encode(main_net_key + checksum)
        addresses.append(public_address.decode())
    return addresses

def public_address_list_to_url(addresses):
    address_list_as_string = ""
    for address in addresses:
        address_list_as_string += address + "|"
    address_list_as_string = address_list_as_string[:-1]
    url = "https://blockchain.info/multiaddr?active={}".format(address_list_as_string)
    return url

def log(message):
    log_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s')

    logFile = 'logFile.txt'

    my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=1*1024*1024,
                                          backupCount=2, encoding=None, delay=0)
    my_handler.setFormatter(log_formatter)
    my_handler.setLevel(logging.INFO)

    app_log = logging.getLogger('root')
    app_log.setLevel(logging.INFO)

    app_log.addHandler(my_handler)

    app_log.info(message)
