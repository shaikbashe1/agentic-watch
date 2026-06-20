# Stub for the crypt module removed in Python 3.12
# Passlib tries to import this, but it doesn't strictly need it if we're only using bcrypt.

def crypt(word, salt):
    raise NotImplementedError("crypt is not supported")
