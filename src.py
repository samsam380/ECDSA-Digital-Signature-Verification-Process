# make sure to run "pip install ecdsa" in your python instance first

# codes below simulate the process of digital signature creation and verification
# you will be asked to add a message, this is arbitrary, you can write anything
# in bitcoin, the message contains the transaction data, something like "Send 1 bitcoin from address A to address B"
# at the end, the code will check if the resulting x coodrinate is equal r, if they are equal then the signature is correct.
# this is how the bitcoin network verifies the correctness of the transaction without the need to revealing the sender's private key

import ecdsa
from ecdsa.curves import SECP256k1
from ecdsa.ellipticcurve import Point
import secrets
import hashlib

# Step 1: Generate a random number (for demonstration purposes)
random_number = secrets.randbelow(SECP256k1.order)
print(f"Step 1: Generated a random number for demonstration: {random_number}")

# Step 2: Generate a private key (think of this as a 'secret' key only known by the signer)
private_key = secrets.randbelow(SECP256k1.order)
print(f"Step 2: Generated a private key: {private_key} (This remains private!)")

# Step 3: Get the generator point on the elliptic curve (a fixed point everyone uses)
generator_point = SECP256k1.generator
print(f"Step 3: Generator Point on the curve (constant and public): {generator_point}")

# Step 4: Multiply the private key with the generator point to get the public key
public_key = generator_point * private_key
print(f"Step 4: Derived public key from the private key (this can be shared): {public_key}")

# Step 5: Create a message (like a transaction to sign)
message = input("\nEnter a message to sign (for example, a Bitcoin transaction): ")
print(f"\nMessage to be signed: '{message}'")

# Step 6: Hash the message (transforms the message into a fixed-size hash)
message_hash = hashlib.sha256(message.encode()).digest()
print(f"Step 6: Hash of the message (unique to this message): {message_hash.hex()}")

# Step 7: Create a signing key from the private key
signing_key = ecdsa.SigningKey.from_secret_exponent(private_key, curve=ecdsa.SECP256k1)

# Step 8: Sign the message hash (creates a digital signature)
signature = signing_key.sign_digest(message_hash, sigencode=ecdsa.util.sigencode_string)
print(f"Step 8: Digital Signature created (r, s values combined): {signature.hex()}")

# Step 9: Extract r and s values from the signature (to understand the signature structure)
r = int.from_bytes(signature[:32], byteorder='big')
s = int.from_bytes(signature[32:], byteorder='big')
print(f"\nSignature Breakdown:\nr: {r}\ns: {s}")

# Step 10: Calculate the inverse of s (used in verification)
s_inv = ecdsa.numbertheory.inverse_mod(s, SECP256k1.order)
print(f"Step 10: Calculated inverse of s: {s_inv}")

# Step 11: Calculate u and v (scalars for verification)
u = int.from_bytes(message_hash, byteorder='big') * s_inv % SECP256k1.order
v = r * s_inv % SECP256k1.order
print(f"Step 11: Calculated u: {u}\nCalculated v: {v}")

# Step 12: Calculate the resulting point using u, v, generator point, and public key
resulting_point = u * generator_point + v * public_key
print(f"Step 12: Resulting Point (derived using u, v, generator, and public key): x = {resulting_point.x()}, y = {resulting_point.y()}")

# Step 13: Verify the signature by comparing resulting_point.x() with r
if resulting_point.x() % SECP256k1.order == r:
    print("\n✅ The signature is valid! This verifies that the message came from the holder of the private key without revealing it.")
else:
    print("\n❌ The signature is not valid. There may be an error in the process or an invalid signature.")
