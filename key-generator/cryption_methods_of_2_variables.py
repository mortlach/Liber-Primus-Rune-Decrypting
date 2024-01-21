'''
cryption methods for simple arithmetic functions
explicit is better than implicit ;)
this is about as simple as it need be
used in other files to encrypt / decrypt user data
see test_functions_of_2_variables.py
'''

from itertools import combinations, product
''' encrypt arithmetic '''
def encrypt_p_plus_k(pt, key):
    if type(pt) == list:
        return [(p + k) % 29 for p, k in zip(pt, key)]
    return (pt + key) % 29
def encrypt_p_minus_k(pt, key):
    if type(pt) == list:
        return [(p - k) % 29 for p, k in zip(pt, key)]
    return (pt - key) % 29
def encrypt_k_minus_p(pt, key):
    if type(pt) == list:
        return [(k - p) % 29 for p, k in zip(pt, key)]
    return (key - pt) % 29
def encrypt_p_multiply_k(pt, key):
    if type(pt) == list:
        return [(p * k) % 29 for p, k in zip(pt, key)]
    return (pt * key) % 29
def encrypt_k_divide_p(pt, key):
    if type(pt) == list:
        return [(k * pow(p, -1, 29)) % 29 if p > 0 else "e" for p, k in zip(pt, key)]
    if pt > 0:
        return (key * pow(pt, -1, 29)) % 29
    else:
        return "e"
def encrypt_p_divide_k(pt, key):
    if type(pt) == list:
        return [(p * pow(k, -1, 29)) % 29 if k > 0 else "e" for p, k in zip(pt, key)]
    if key > 0:
        return (pt * pow(key, -1, 29)) % 29
    else:
        return "e"

def encrypt_p_xor_k(pt, key):
    if type(pt) == list:
        return  [(p ^ k) % 29 for p, k in zip(pt, key)]
    return (pt ^ key) % 29

def encrypt_k_xor_p(pt, key):
    if type(pt) == list:
        return [(k ^ p )% 29 for p, k in zip(pt, key)]
    return (key ^ pt) % 29

def get_decrypt_data(encryption_function_of_p_and_k):
    '''
    returns map of (c,p)->k for function p+k=c
    '''
    raw_data =  [(p, k1, encryption_function_of_p_and_k(p,k1)) for p, k1 in list(product(list(range(29)), repeat=2))]
    r = {}
    p, k, c = 0,1,2
    for data in raw_data:
        next_key = tuple([data[c], data[p]])
        if next_key in r:
            r[next_key].append(data[k])
        else:
            r[next_key] = [data[k]]
    return r

''' generating raw data for decryption maps  '''
print('''Generating raw data for decryption maps''')
__decrypt_p_plus_k_data = get_decrypt_data(encrypt_p_plus_k)
__decrypt_p_minus_k_data = get_decrypt_data(encrypt_p_minus_k)
__decrypt_k_minus_p_data = get_decrypt_data(encrypt_k_minus_p)
__decrypt_p_multiply_k_data = get_decrypt_data(encrypt_p_multiply_k)
__decrypt_p_divide_k_data = get_decrypt_data(encrypt_p_divide_k)
__decrypt_k_divide_p_data = get_decrypt_data(encrypt_k_divide_p)
__decrypt_k_xor_p_data = get_decrypt_data(encrypt_k_xor_p)
__decrypt_p_xor_k_data = get_decrypt_data(encrypt_p_xor_k)
#print(__decrypt_k_divide_p_data)

def decrypt_p_plus_k(ct, pt):
    return [v for v in product(*[__decrypt_p_plus_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_p_minus_k(ct, pt):
    return [v for v in product(*[__decrypt_p_plus_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_k_minus_p(ct, pt):
    return [v for v in product(*[__decrypt_p_plus_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_p_multiply_k(ct, pt):
    return [v for v in product(*[__decrypt_p_multiply_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_p_divide_k(ct, pt):
    return [v for v in product(*[__decrypt_p_divide_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_k_divide_p(ct, pt):
    return [v for v in product(*[__decrypt_k_divide_p_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_p_xor_k(ct, pt):
    return [v for v in product(*[__decrypt_p_xor_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
def decrypt_k_xor_p(ct, pt):
    return [v for v in product(*[__decrypt_k_xor_p_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]

all_decrypt_methods_of_2_variables = [
decrypt_p_xor_k,
decrypt_k_xor_p,
decrypt_p_plus_k,
decrypt_p_minus_k,
decrypt_k_minus_p,
decrypt_p_multiply_k,
decrypt_p_divide_k,
decrypt_k_divide_p

]

all_encrypt_methods_of_2_variables = [
encrypt_p_xor_k,
encrypt_k_xor_p,
encrypt_p_plus_k,
encrypt_p_minus_k,
encrypt_k_minus_p,
encrypt_p_multiply_k,
encrypt_p_divide_k,
encrypt_k_divide_p

]



# def get_decrypt_p_minus_k_data():
#     '''
#     returns map of (c,p)->k for function p+k=c
#     '''
#     raw_data = [(p, k1, encrypt_p_minus_k(p,k1)) for p, k1 in list(product(list(range(29)), repeat=2))]
#     r = {}
#     p, k, c = 0,1,2
#     for data in raw_data:
#         next_key = tuple([data[c], data[p]])
#         if next_key in r:
#             r[next_key].append(data[k])
#         else:
#             r[next_key] = [data[k]]
#     return r
# __decrypt_p_minus_k_data = get_decrypt_p_minus_k_data()
# def decrypt_p_minus_k(ct, pt):
#     return [v for v in product(*[__decrypt_p_minus_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
#
#
#
#
#
#
#
#





#
# def get_decrypt_p_minus_k_data():
#     '''
#     returns map of (c,p)->k for function p+k=c
#     '''
#     raw_data = [(p, k1, encrypt_k_minus_p(p,k1)) for p, k1 in list(product(list(range(29)), repeat=2))]
#     r = {}
#     p, k, c = 0,1,2
#     for data in raw_data:
#         next_key = tuple([data[c], data[p]])
#         if next_key in r:
#             r[next_key].append(data[k])
#         else:
#             r[next_key] = [data[k]]
#     return r
# __decrypt_p_minus_k_data = get_decrypt_p_minus_k_data()
# def decrypt_p_minus_k(ct, pt):
#     return [v for v in product(*[__decrypt_p_minus_k_data.get(tuple([c, p]), ["e"]) for c, p in zip(ct, pt)])]
#
#
#
# def getDecryptPlus():
#     '''
#     returns map of (c,p)->k for function p+k=c
#     '''
#     raw_data =  [(p, k1, encrypt_p_plus_k(p,k1)) for p, k1 in list(product(list(range(29)), repeat=2))]
#     r = {}
#     p, k, c = 0,1,2
#     for data in raw_data:
#         next_key = tuple([data[c], data[p]])
#         if next_key in r:
#             r[next_key].append(data[k])
#         else:
#             r[next_key] = [data[k]]
#     return r
#
#
#
# def getDecryptMultiplyPlus():
#     '''
#     returns map of (c[i],p[i],k1[i])->k[i] for function p[i]*k1[i]+k2[i]=c[i]
#     where k2[i]=c[i-1]
#     '''
#     raw_data = [(p, k1, k2, (p*k1+k2) % 29) for p, k1, k2 in list(product(list(range(29)),repeat=3))]
#     r = {}
#     p, k1, k2, c = 0,1,2,3
#     for data in raw_data:
#         next_key = tuple([data[c], data[p], data[k2]])
#         if next_key in r:
#             newv = r[next_key]
#             newv.append(data[k1])
#             r[next_key] = newv
#         else:
#             r[next_key] = [data[k1]]
#     return r