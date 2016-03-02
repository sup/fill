import hashlib
import string
import random

#For hashing/security (naive)
def hash_str(s):
    return hashlib.md5(s).hexdigest()

def make_secure_val(s):
    return "%s|%s" % (s, hash_str(s))

def check_secure_val(h):
    val = h.split("|")[0]
    if h == make_secure_val(val):
        return val

def make_salt(size = 5, char = string.letters):
    return ''.join(random.choice(char) for x in xrange(size))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    return hashlib.sha256(name + pw + salt).hexdigest() + "," + salt

def valid_pw(name, pw, h):
    salt = h.split(",")[1]
    return h == hashlib.sha256(name + pw + salt).hexdigest() + "," + salt