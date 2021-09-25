# Nashwan Sulaiman


from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

# tables for key generation
key_shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

PC1 = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18, 10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36, 63,
       55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22, 14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]

PC2 = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10, 23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2, 41, 52, 31, 37, 47, 55,
       30, 40, 51, 45, 33, 48, 44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]

# tables for encryption

IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]
IP_inverse = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# Tables for function f

E = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9, 8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17, 16, 17, 18, 19, 20, 21, 20, 21,
     22, 23, 24, 25, 24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]

S = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
    ]
]

P = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25]


# In[ ]:


# In[2]:


def bytes2binary(hex_input,case=0):
    int_input = int.from_bytes(hex_input, byteorder='big')
    target_length = len(bin(int_input)[2:]) + (8 - len(bin(int_input)[2:]) % 8) % 8
    if case == 0:
        return bin(int_input)[2:].zfill(target_length)
    else:
        return bin(int_input)[2:].zfill(64)
        #i=0
        #while b[i] == 0:
        #target_length = target_length + 8
        #i++
        


# In[ ]:


# In[3]:


def binary2bytes(bin_input):
    scr_length = len(bin_input) + (8 - len(bin_input) % 8) % 8
    bin_input = bin_input.zfill(scr_length)
    bin_input_to_int = (int(bin_input[bin_byte: bin_byte + 8], 2) for bin_byte in range(0, len(bin_input), 8))
    return bytes(bin_input_to_int)


# In[ ]:


# In[4]:


def bin_xor(bin1, bin2):
    length = max(len(bin1), len(bin2))
    bin1 = int('0b' + bin1, 2)
    bin2 = int('0b' + bin2, 2)
    return (bin(bin1 ^ bin2)[2:]).zfill(length)


# In[ ]:


# In[5]:


def create_DES_subkeys(key):
    # Generate 56bit key
    k_plus = [key[ind - 1] for ind in PC1]

    # Split Key to left and right
    C0 = k_plus[:28]
    D0 = k_plus[28:]

    Cn = [''.join(C0)]
    Dn = [''.join(D0)]

    # Generates Ci,Di i=1,..,15
    def shift_key(key, shift):
        key = key[shift:] + key[:shift]
        return key

    for i in range(0, 16):
        Cn.append(''.join(shift_key(Cn[i], key_shifts[i])))
        Dn.append(''.join(shift_key(Dn[i], key_shifts[i])))

    # Generate Final sub-keys
    Sub_keys_concatenated = [Cn[key + 1] + Dn[key + 1] for key in range(0, 16)]

    Sub_keys = [''.join([Sub_keys_concatenated[numkey][value - 1] for value in PC2]) for numkey in range(0, 16)]

    return Sub_keys


# In[ ]:


# In[ ]:


# In[ ]:


# In[6]:


def S_box_P(E_R_data_Gr):
    S_E_R_data = []
    S_E_R_data_P = []
    for i in range(0, 8):
        row = int(E_R_data_Gr[i][0] + E_R_data_Gr[i][-1], 2)
        # print(row)
        col = int(E_R_data_Gr[i][1:-1], 2)
        # print(col)
        # print(E_R_data_Gr[i][1:-1])
        S_E_R_data.append((bin(S[i][row][col])[2:]).zfill(4))

    S_E_R_data = list(''.join(S_E_R_data))
    # print(S_E_R_data)

    S_E_R_data_P = [S_E_R_data[n - 1] for n in P]

    return ''.join(S_E_R_data_P)


def f(R_data, key):
    # Apply E permutaion
    E_R_data = ''.join([R_data[new_pos - 1] for new_pos in E])

    # XOR Previous result of permutation with the key
    E_R_data_X_Key = bin_xor(E_R_data, key)

    # Divide to six bit group
    E_R_data_X_Key_6b_group = [E_R_data_X_Key[i:i + 6] for i in range(0, len(E_R_data_X_Key), 6)]
    return S_box_P(E_R_data_X_Key_6b_group)


# In[ ]:


# In[7]:


def encrypt_DES(Message, key):
    Message = bytes2binary(Message,64)
    # Prepare Message
    Message = list(Message)

    # print('Mes')
    # print(Message)

    # print()

    Message_IP = [Message[i - 1] for i in IP]

    # print('Message_IP')
    # print(len(Message_IP))

    Message_IP = ''.join(Message_IP)

    L0 = Message_IP[:32]
    R0 = Message_IP[32:]

    L_previous = L0
    R_previous = R0

    # print(L_previous)
    # print(R_previous)

    # Generate Sub Keys
    key = bytes2binary(key,64)
    key = create_DES_subkeys(key)

    # print(key)

    # Implementation Rounds
    def Rounds(L_previous, R_previous):
        for ite in range(0, 16):
            L_current = R_previous
            R_current = bin_xor(L_previous, f(R_previous, key[ite]))
            R_previous = R_current
            L_previous = L_current

        return R_current + L_current

    # R16L16 =  R_current+L_current
    R16L16 = Rounds(L0, R0)
    Cipher = [R16L16[i - 1] for i in IP_inverse]

    Cipher = ''.join(Cipher)

    return binary2bytes(Cipher)


# In[ ]:


# In[ ]:


# In[ ]:


# In[8]:


# In[ ]:


# In[ ]:


# In[9]:


def are_random_tests_all_passes(testtimes):
    result = []
    for i in range(0, testtimes):
        key = get_random_bytes(8)
        plaintext = get_random_bytes(8)
        cipher = DES.new(key, DES.MODE_ECB)
        msg = cipher.encrypt(plaintext)
        result.append(encrypt_DES(plaintext, key) == msg)
    # return result
    return all([results for results in result])


# In[10]:


print(are_random_tests_all_passes(100))

# In[ ]:
#print(bytes2binary(b'\xf0\x80'))

# In[ ]:




