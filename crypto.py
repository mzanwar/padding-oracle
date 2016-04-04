from Crypto import Random
from Crypto.Cipher import AES

KEY = "1234567890ABCDEF"


def encrypt(data):
    iv = Random.get_random_bytes(AES.block_size)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return iv + cipher.encrypt(pad(data))


def decrypt(data):
    if len(data) < AES.block_size*2 or len(data) % AES.block_size != 0:
        raise ValueError("Invalid message format")
    iv, ciphertext = data[:AES.block_size], data[AES.block_size:]
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext))


def _pad_str(length):
    # return chr(length) * length  # RFC 2040
    # return "".join(chr(i) for i in xrange(1, length + 1))  # IP ESP
    # return "\x00" * (length - 1) + chr(length)  # Schneier
    return "\x01" + (length - 1) * "\x00"  # NIST


def pad(data):
    pad_len = AES.block_size - (len(data) % AES.block_size)
    return data + _pad_str(pad_len)


def unpad(data):
    # pad_len = ord(data[-1])  # RFC 2040, IP ESP, Schneier
    pad_len = len(data) - data.rfind("\x01", -AES.block_size)  # NIST
    if pad_len < 1 or pad_len > AES.block_size:
        raise ValueError("Invalid message padding")
    message, padding = data[:-pad_len], data[-pad_len:]
    if padding != _pad_str(pad_len):
        raise ValueError("Invalid message padding")
    return message


if __name__ == "__main__":
    data = "Attack at dawn!"
    ciphertext = encrypt(data)
    decrypted = decrypt(ciphertext)
    print "plaintext: ", repr(data)
    print "ciphertext: ", repr(ciphertext)
    print "decrypted: ", repr(decrypted)
