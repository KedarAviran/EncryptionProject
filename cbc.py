BLOCK_SIZE = 10
PADCHAR = 0
forward = {}
backwards = {}

"""
def formatWords():
    mystring = ''
    with open("words.txt", 'r+') as cipherText_file:
        words = cipherText_file.read()
        cipherText_file.close()
    for word in words.split('\n'):
       mystring = mystring + '" ' + word + ' ",\n'
    with open("words.txt", 'r+') as cipherText_file:
        cipherText_file.write(mystring)
"""


def pad(data):
    pad_size = BLOCK_SIZE - len(data) % BLOCK_SIZE
    if pad_size == BLOCK_SIZE:
        pad_size = 0
    return data + bytes([PADCHAR] * pad_size)


def unpad(data):
    i = len(data) - 1
    while i > 0:
        if data[i] != PADCHAR:
            return data[:i + 1]
        i -= 1
    return data


def loadkey(data):
    i = 0
    while i + 2 < len(data):
        if data[i] != 13 and data[i] != 10:
            forward[data[i]] = data[i + 2]
            backwards[data[i + 2]] = data[i]
            i += 3
        else:
            i += 1


def usekey(data):
    result = []
    for i in range(len(data)):
        if data[i] in forward:
            result.append(forward[data[i]])
        else:
            result.append(data[i])
    return bytes(result)


def unusekey(data):
    result = []
    for i in range(len(data)):
        if data[i] in backwards:
            result.append(backwards[data[i]])
        else:
            result.append(data[i])
    return bytes(result)


def encrypt_cbc(iv, plaintext):
    ciphertext = b''
    previous_block = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        block = bytes(x ^ y for x, y in zip(block, previous_block))
        block = usekey(block)
        ciphertext += block
        previous_block = block
    return ciphertext


def decrypt_cbc(iv, ciphertext):
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i + BLOCK_SIZE]
        block = unusekey(block)
        block = bytes(x ^ y for x, y in zip(block, previous_block))
        plaintext += block
        previous_block = ciphertext[i:i + BLOCK_SIZE]
    return unpad(plaintext)


def Encryption(plainTextPath, keyPath, iVPath, outputPath):
    with open(keyPath, 'rb') as key_file:
        loadkey(key_file.read())
    with open(iVPath, 'rb') as iv_file:
        ivtext = iv_file.read()
    with open(plainTextPath, 'rb') as plaintext_file:
        plaintext = plaintext_file.read()
    plaintext = pad(plaintext)
    ciphertext = encrypt_cbc(ivtext, plaintext)
    with open(outputPath, 'wb') as ciphertext_file:
        ciphertext_file.write(ciphertext)


def Decryption(cipherTextPath, keyPath, iVPath):
    with open(keyPath, 'rb') as key_file:
        loadkey(key_file.read())
    with open(iVPath, 'rb') as iv_file:
        ivtext = iv_file.read()
    with open(cipherTextPath, 'rb') as cipherText_file:
        cipherText = cipherText_file.read()
    cipherText = unpad(cipherText)
    plaintext = decrypt_cbc(ivtext, cipherText)
    with open('msg.txt', 'wb') as plaintext_file:
        plaintext_file.write(plaintext)


Encryption("firstmsg.txt", "key.txt", "iv.txt", "firstcipher.txt")
Encryption("secmsg.txt", "key.txt", "iv.txt", "seccipher.txt")
Decryption("firstcipher.txt", "key.txt", "iv.txt")

