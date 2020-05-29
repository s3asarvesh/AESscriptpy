# -*- coding: utf-8 -*-
"""
@author: Sarvesh
"""

from Crypto import Random
from Crypto.Cipher import AES
import os
import sys

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def encrypt(message, key, key_size=128):
    message = pad(message)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(message)

def decrypt(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0")

def encrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        plaintext = fo.read()
    enc = encrypt(plaintext, key)
    with open(file_name + ".enc", 'wb') as fo:
        fo.write(enc)
    os.remove(file_name)    

def decrypt_file(file_name, key):
    with open(file_name, 'rb') as fo:
        ciphertext = fo.read()
    dec = decrypt(ciphertext, key)
    with open(file_name[:-4], 'wb') as fo:
        fo.write(dec)
    os.remove(file_name)    


if len(sys.argv)<2:
    print("Error Input file to encrypt")
    print("Usage:enc_128 'file to be encrypted'")
else:
    print("Enter 1 to encrypt file\nEnter 2 to decrypt file")
    c=int(input("Enter choice\t"))
    if c == 1:
    	ckey = input("Enter key for encryption: ")
    	key = ckey.encode('utf-8')+b"\0" * (AES.block_size - len(ckey.encode('utf-8')) % AES.block_size)
    	encrypt_file(sys.argv[1], key)
    elif c == 2:
    	ckey = input("Enter key for decryption: ")
    	key = ckey.encode('utf-8')+b"\0" * (AES.block_size - len(ckey.encode('utf-8')) % AES.block_size)
    	decrypt_file(sys.argv[1], key)
        
        