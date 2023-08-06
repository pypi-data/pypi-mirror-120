from .crypto import RSA, SHA256, PKCS1_v1_5
from .util import tobytes
from base64 import b64encode, urlsafe_b64encode, b64decode, urlsafe_b64decode

def sign(message, key="sign.key", passphrase=None, no_urlsafe=False, raw=False):
    with open(key, 'rb') as f:
        private_key = RSA.importKey(f.read(), passphrase=passphrase)
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new()
    digest.update(tobytes(message, raw))
    sig = signer.sign(digest)
    sig64 = (urlsafe_b64encode if not no_urlsafe else b64encode)(sig).decode('utf8')
    return sig64

def verify(message, signature, *, key="sign.crt", passphrase=None, no_urlsafe=False, raw=False):
    with open(key, 'rb') as f:
        public_key = RSA.importKey(f.read(), passphrase=passphrase)
    verifier = PKCS1_v1_5.new(public_key)
    digest = SHA256.new()
    digest.update(tobytes(message, raw))
    sig64 = (urlsafe_b64decode if not no_urlsafe else b64decode)(tobytes(signature))
    ok = verifier.verify(digest, sig64)
    return ok
