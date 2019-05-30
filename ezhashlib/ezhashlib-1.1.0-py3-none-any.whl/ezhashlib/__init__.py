import hashlib

methods = ['sha3_224', 'sha224', 'shake_256', 'sha512', 'sha384', 'sha3_384', 'sha1', 'sha3_512', 'sha256', 'blake2b', 'blake2s', 'md5', 'sha3_256']

for i in methods:
    exec("""def {}(phrase):
        hash_object = hashlib.{}(phrase.encode("utf-8"))
        hex_dig = hash_object.hexdigest()
        return str(hex_dig)""".format(i, i))
    
