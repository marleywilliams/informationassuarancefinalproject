''' code inspired by Svetlin Nakov at cryptobook.nakov.com '''

from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii, time


def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)


def decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext


def ecc_point_to_256_bit_key(point):
    sha = hashlib.sha256(int.to_bytes(point.x, 32, 'big'))
    sha.update(int.to_bytes(point.y, 32, 'big'))
    return sha.digest()


curve = registry.get_curve('brainpoolP256r1')


def encrypt_ECC(msg, pubKey):
    ciphertextPrivKey = secrets.randbelow(curve.field.n)
    sharedECCKey = ciphertextPrivKey * pubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    ciphertext, nonce, authTag = encrypt_AES_GCM(msg, secretKey)
    ciphertextPubKey = ciphertextPrivKey * curve.g
    return (ciphertext, nonce, authTag, ciphertextPubKey)


def decrypt_ECC(encryptedMsg, privKey):
    (ciphertext, nonce, authTag, ciphertextPubKey) = encryptedMsg
    sharedECCKey = privKey * ciphertextPubKey
    secretKey = ecc_point_to_256_bit_key(sharedECCKey)
    plaintext = decrypt_AES_GCM(ciphertext, nonce, authTag, secretKey)
    return plaintext

def main():
    print('Enter the value to encrypt: ')
    x = input()

    print("How many times would you like to run: ")
    num_run = input()

    msg = bytes(str(x), 'utf8')
    print("original msg:", msg)


    for i in range(int(num_run)):
        start = time.time()

        privKey = secrets.randbelow(curve.field.n) # pick random private key on curve
        pubKey = privKey * curve.g

        encryptedMsg = encrypt_ECC(msg, pubKey)

        print("encrypted:", binascii.hexlify(encryptedMsg[0]))

        decryptedMsg = decrypt_ECC(encryptedMsg, privKey)
        print("decrypted:", decryptedMsg)
    end = time.time()
    print("Total time: ", end-start)


if __name__ == '__main__':
    main()