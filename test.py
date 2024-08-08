import hashlib
import re


hash_obj = hashlib.md5('10589110buy3discord80rub05082024115745'.encode())
line = str(hash_obj.hexdigest())
only_digits = ''.join(re.findall(r'\d', line))
print(only_digits)
