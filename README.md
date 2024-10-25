# ECDSA-Digital-Signature-Verification-Process
ECDSA Digital Signature Verification Process as used in Bitcoin Transactions

The digital signature is verified as valid because the x coordinate of the resulting_point matches the r value from the signature.

Here’s a breakdown of why this is the key to verification:

Signature Creation: When a message is signed, it generates a pair (r, s):
        r is derived from the x coordinate of a specific point on the elliptic curve, which involves the private key and the hashed message.
        s is another value that ties the signature to the private key and the message hash.

Signature Verification: To verify the signature without knowing the private key, we use a mathematical approach with r, s, the public key, and the message hash:
        By calculating u and v (which involve the inverse of s and the hashed message), we reconstruct the elliptic curve point used in the signature process.
        The x coordinate of this resulting_point should match r if the signature is valid.

Match of x and r: Since x from resulting_point matches r, it confirms that:
        The signature was created with the corresponding private key.
        The message wasn’t altered after signing.

This process essentially ensures that only someone with the private key could have generated the signature, while keeping that private key hidden. So, in summary, the verification hinges on this x == r equality.
