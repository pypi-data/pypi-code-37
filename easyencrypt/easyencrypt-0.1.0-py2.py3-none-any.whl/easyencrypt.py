from cryptography.fernet import Fernet
import rsa
import hashlib
import binascii
import base64
import os

def newSalt(size=16):
    '''Generate a new salt.'''
    salt = os.urandom(size)
    return salt

def hashText(text, algorithm="sha512", salt=b""):
    '''Hash some text. It is highly recommended that a salt be used.'''
    thehash = hashlib.new(algorithm, salt + text)
    thehash = thehash.digest()
    return thehash

def newKey():
    '''Generate a new symmetric key.'''
    key = Fernet.generate_key()
    return key

def passwordToKey(password):
    '''Convert a password into a useable encryption/decryption key.'''
    key = hashlib.sha256(password).digest()
    key = base64.urlsafe_b64encode(key)
    return key

def symmetricEncrypt(plaintext, key):
    '''Encrypt text symmetrically with a key. Use passwordToKey if 
    using a password instead of a generated key.
    '''
    cipher = Fernet(key)
    ciphertext = cipher.encrypt(plaintext)
    ciphertext = base64.urlsafe_b64decode(ciphertext)
    return ciphertext

def symmetricDecrypt(ciphertext, key):
    '''Decrypt text symmetrically with a key. Use passwordToKey if 
    using a password instead of a generated key.'''
    cipher = Fernet(key)
    ciphertext = base64.urlsafe_b64encode(ciphertext)
    plaintext = cipher.decrypt(ciphertext)
    return plaintext

def newKeyPair(keysize=512):
    '''Generate a new public/private key pair.'''
    pub, priv = rsa.newkeys(keysize)
    return pub, priv

def encrypt(plaintext, pubKey):
    '''Encrypt text with a public key.'''
    ciphertext = rsa.encrypt(plaintext, pubKey)
    return ciphertext

def decrypt(ciphertext, privKey):
    '''Decrypt text with a private key.'''
    plaintext = rsa.decrypt(ciphertext, privKey)
    return plaintext
