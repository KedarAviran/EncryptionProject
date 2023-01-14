BLOCK_SIZE = 10
forward = {}
backwards = {}


def pad(data):
    pad_size = BLOCK_SIZE - len(data) % BLOCK_SIZE
    return data + bytes([pad_size] * pad_size)


def unpad(data):
    pad_size = data[-1]
    return data[:-pad_size]


def loadkey(data):
    for block in data.split("\n"):
        value = block.split(" ")
        forward[value[0]] = value[1]
        backwards[value[1]] = value[0]


def usekey(data):
    result = data
    for i in range(len(data)):
        result[i] = forward[data[i]]
    return result


def unusekey(data):
    result = data
    for i in range(len(data)):
        result[i] = backwards[data[i]]
    return result


def encrypt_cbc(iv, plaintext):
    ciphertext = b''
    previous_block = iv
    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        block = bytes(x ^ y for x, y in zip(block, previous_block))
        block = usekey(block)
        block = bytes(block)
        ciphertext += block
        previous_block = block
    return ciphertext


def decrypt_cbc(iv, ciphertext):
    plaintext = b''
    previous_block = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        block = unusekey(block)
        block = bytes(block)
        block = bytes(x ^ y for x, y in zip(block, previous_block))
        plaintext += block
        previous_block = ciphertext[i:i+BLOCK_SIZE]
    return unpad(plaintext)


def Encryption(plainTextPath, keyPath, iVPath):
    with open(keyPath, 'rb') as key_file:
        loadkey(key_file.read())
    with open(iVPath, 'rb') as iv_file:
        ivtext = iv_file.read()
    with open(plainTextPath, 'rb') as plaintext_file:
        plaintext = plaintext_file.read()
    plaintext = pad(plaintext)
    ciphertext = encrypt_cbc(ivtext, plaintext)
    with open('cipherText.txt', 'wb') as ciphertext_file:
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
    with open('cipherText.txt', 'wb') as plaintext_file:
        plaintext_file.write(plaintext)