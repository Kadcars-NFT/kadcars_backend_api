import hashlib
import base64
import js2py
from temp import *

input = "{\"networkId\":\"testnet04\",\"payload\":{\"cont\":{\"proof\":null,\"data\":{\"kc\":{\"pred\":\"keys-all\",\"keys\":[\"f157854c15e9bb8fb55aafdecc1ce27a3d60973cbe6870045f4415dc06be06f5\"]},\"transformation-list\":[{\"transform\":{\"obj\":{\"uri\":{\"data\":\"view-references\",\"scheme\":\"ipfs\"},\"new-datum\":{\"hash\":\"6Te22fUzf-9ynFfzYTYnKLzVVU2JhqhimJPgYGyuAwQ\",\"uri\":{\"data\":\"view-references\",\"scheme\":\"pact:schema\"},\"datum\":{\"art-asset\":{\"data\":\"ipfs://bafybeielzyapofnglxicaith7etxczpxq3psaeq6uh7chuh6dtbbmtqyny\",\"scheme\":\"ipfs://\"}}}},\"type\":\"replace\"}},{\"transform\":{\"obj\":{\"hash\":\"6Te22fUzf-9ynFfzYTYnKLzVVU2JhqhimJPgYGyuAwQ\",\"uri\":{\"data\":\"nft-references\",\"scheme\":\"pact:schema\"},\"datum\":{\"test\":\"test\"}},\"type\":\"add\"}},{\"transform\":{\"obj\":{\"uri\":{\"data\":\"ipfs://bafybeia3obqfvgnxpm56oan2b7mempewuml4xynlcgkodks6tf44b3hnie\",\"scheme\":\"ipfs\"}},\"type\":\"uri\"}}]},\"pactId\":\"DycORcKohpEWlyC6VxX9pcT28y_bP-G52xjlGqAaUVc\",\"rollback\":false,\"step\":2}},\"signers\":[{\"pubKey\":\"b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3\"}],\"meta\":{\"creationTime\":1678004406,\"ttl\":6000,\"gasLimit\":150000,\"chainId\":\"1\",\"gasPrice\":1.0e-8,\"sender\":\"k:b9b798dd046eccd4d2c42c18445859c62c199a8d673b8c1bf7afcfca6a6a81e3\"},\"nonce\":\"\\\"2023-03-05 08:20:06.599883 UTC\\\"\"}"
hashinput = hashlib.blake2b(input.encode("utf-8"), digest_size=32)
print()
print(hashinput.digest())
print()

encodedBytes = base64.b64encode(input.encode("utf-8"))
encodedStr = str(encodedBytes, "utf-8")

js2py.translate_file("EncodingUtils.js", "temp.py")
output = temp.b64url.encode("_ÁÐ'Á7µüè¹ÀµáK¢öPÌô×~$");

print()
print(output)