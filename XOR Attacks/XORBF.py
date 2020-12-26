from itertools import product
import codecs

 
enc_str ="34020703460a03470709024701021247120f034715021002084716080f091214"


# GENERATING THE KEYS FUNCTION
def allposibilewords(characters, length):
    
    '''
    
    Generate All Possible Keys using itertools
    
    >>allposibilewords("ab", 2)
    aa
    ab
    ba
    bb
    
    '''
    
    for let in product(characters, repeat=length):
        yield ''.join(let)

# CALCULATE CIPHERTEXT LENGTH
def lengthkey(key):
    
    keylength = len(enc_str) / len(key)
    return int(keylength)
 
# BRUTE FORCE ATTACK FUNCTION
def generater(ciphertext):
    
    # LOWERCASE ENGLISH LETTERS DICTIONARY, YOU CAN ADD HERE YOUR DICTIONARY
    letters = "abcdefghijklmnopqrstuvxyz"
    
    for wordlen in range(2, 4):
        for key in allposibilewords(letters, wordlen):
            key = key.encode("utf-8").hex()
            newkey = key*lengthkey(key)
            decrypted = hex(int(newkey, 16) ^ int(enc_str, 16))
            plain = codecs.decode(decrypted[2:], "hex").decode('utf-8')
            
            # PRINT THE OUTPUT IF THE DECRYPTED ONE CONTAINS PRINTABLE ENGLISH LETTERS,
            # AND ONLY FROM THE DICTIONARY WE HAVE CREATED BEFORE
            if plain.isprintable() and not any(letter.lower() not in letters for letter in (''.join(plain.strip().split()))):
                print("The Key : " +  codecs.decode(key, "hex").decode('utf-8') + '\n' + "The Plaintext : " + plain)