import base58
import hashlib
import binascii
import os
import ecdsa

class KeyGen:

    @staticmethod
    def generate_private_key(amount):
        list_of_pkeys = []
        for i in range(amount):
            list_of_pkeys.append(binascii.hexlify(os.urandom(32)).decode())
        return list_of_pkeys

    @staticmethod
    def private2wif(private_keys):

        list_of_wifs = []

        for private_key in private_keys:
            # Step 1: here we have the private key
            private_key_static = private_key
            # Step 2: let's add 80 in front of it
            extended_key = "80"+private_key_static
            # Step 3: first SHA-256
            first_sha256 = hashlib.sha256(
                binascii.unhexlify(extended_key)).hexdigest()
            # Step 4: second SHA-256
            second_sha256 = hashlib.sha256(
                binascii.unhexlify(first_sha256)).hexdigest()
            # Step 5-6: add checksum to end of extended key
            final_key = extended_key+second_sha256[:8]
            # Step 7: finally the Wallet Import Format is the base 58 encode of final_key
            WIF = base58.b58encode(binascii.unhexlify(final_key)).decode()\

            list_of_wifs.append(WIF)

        return list_of_wifs

    @staticmethod
    def __ripemd160(x):
        d = hashlib.new('ripemd160')
        d.update(x)
        return d

    @staticmethod
    def private2address(private_keys):

        list_of_addresses = []

        for private_key in private_keys:

            private_key = binascii.unhexlify(private_key)
            sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
            vk = sk.get_verifying_key()
            publ_key = '04' + binascii.hexlify(vk.to_string()).decode()
            hash160 = KeyGen.__ripemd160(hashlib.sha256(
                binascii.unhexlify(publ_key)).digest()).digest()
            publ_addr_a = b"\x00" + hash160
            checksum = hashlib.sha256(hashlib.sha256(
                publ_addr_a).digest()).digest()[:4]
            publ_addr_b = base58.b58encode(publ_addr_a + checksum)

            list_of_addresses.append(publ_addr_b.decode())

        return list_of_addresses
