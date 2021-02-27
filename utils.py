import requests
from bs4 import BeautifulSoup

import hashlib
import ecdsa
import codecs

def get_address(input_password_bytes):

    private_key = hashlib.sha256(input_password_bytes).hexdigest()
    private_key_bytes = codecs.decode(private_key, "hex") #Type bytes
    private_key_hex = private_key_bytes.hex()

    # Get ECDSA public key
    verifying_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1).verifying_key
    public_key_bytes = verifying_key.to_string()

    public_key_full_bytes = bytes.fromhex("04") + public_key_bytes #Type bytes
    public_key_full_hex = public_key_full_bytes.hex() #Type str

    if (ord(bytearray.fromhex(public_key_full_hex[-2:])) % 2 == 0):
        appended_hex = '02'
    else:
        appended_hex = '03'
    appended_hex += public_key_full_hex[2:66] #Type str
    public_key_compressed_bytes = bytearray.fromhex(appended_hex) #Type bytearray

    public_key_compressed_hex = public_key_compressed_bytes.hex()

    sha = hashlib.sha256()
    sha.update(public_key_compressed_bytes)
    rip = hashlib.new('ripemd160')
    rip.update(sha.digest())

    encrypted_public_key_hex = rip.hexdigest() #Type str
    main_net_key_bytes = bytes.fromhex("00") + bytes.fromhex(encrypted_public_key_hex) #Type bytes
    main_net_key_hex = main_net_key_bytes.hex() #Type str
    main_net_key_byte_array = bytearray.fromhex(main_net_key_hex) #Type bytearray

    sha1 = hashlib.sha256()
    sha1.update(main_net_key_byte_array)

    sha2 = hashlib.sha256()
    sha2.update(sha1.digest())

    double_sha_hex = sha2.hexdigest() #Type str
    checksum_hex = double_sha_hex[:8] #Type str

    address_bytes = main_net_key_bytes + bytes.fromhex(checksum_hex) #Type bytes
    address_hex = address_bytes.hex() #Type str


    #Encode address with Base58

    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    address_b58 = ""
    # Get the number of leading zeros
    leading_zeros = len(address_hex) - len(address_hex.lstrip("0"))
    # Convert hex to decimal
    address_int = int(address_hex, 16)
    # Append digits to the start of string
    while address_int > 0:
        digit = address_int % 58
        digit_char = alphabet[digit]
        address_b58 = digit_char + address_b58
        address_int //= 58
    # Add '1' for each 2 leading zeros
    ones = leading_zeros // 2
    for one in range(ones):
        address_b58 = "1" + address_b58

    return(address_b58)

def has_balance(address):
    sep = " "

    URL = "https://explorer.btc.com/btc/address/{0}".format(address)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    balance_btc = soup.find(text="Balance").findNext('div').text

    balance_btc_stripped = balance_btc.split(sep, 1)[0]

    if (balance_btc_stripped != "0"):
        print("YAY!")
        return ("1", address, balance_btc_stripped)
    else:
        return ("0", address, balance_btc_stripped)
