'''

*** TEST OVERVIEW ***

Encrypt text with a key using some arithmetic function with random:
    interrupter, transposition, gematria shift, ... anything else?
For a given crib generate keys for:
    all possible interrupter,
    defined transpositions
    gematria shifts
    ... anything else?

Generated keys can be further inspected to look for 'patterns'
(sequences, words, etc.)

In these tests we compare key to the known key
to 'prove' we have generated a solution to  this encryption.

Also solve 56.jpg and a koan by cribbing then
finding the known key and interrupter in generated data

See 'keys_for_cribs.py' for how to generate keys lists from a criblist

'''
import key_generator as gd
import cryption_methods_of_2_variables as cry

key_generator = gd.KeyGenerator()

for dec, enc in zip(cry.all_decrypt_methods_of_2_variables,cry.all_encrypt_methods_of_2_variables):
    print(enc.__name__,dec.__name__)
    key_generator.test_solve(enc, dec)


''' test LOSS OF DIVINITY.jpg '''
print('\nTEST WE CAN SOLVE: "A KOAN DURING", key repeating FIRFUMFERENCE')

ct_koan = [24, 15, 7, 24, 10, 13, 1, 22, 25, 13, 0, 18, 4, 15, 13, 13, 2, 19, 9, \
           24, 4, 20, 7, 13, 18, 3, 13, 1, 28, 10, 10, 8, 23, 20, 22, 28, 11, \
           18, 28, 10, 25, 6, 18, 2, 22, 10, 23, 22, 21, 0, 11, 18, 23, 10, 14, \
           9, 1, 20, 0, 8, 4, 7, 13, 23, 27, 8, 7, 15, 5, 14, 23, 8, 27, 18, 27, \
           28, 4, 14, 18, 12, 17, 7, 28, 15, 17, 20, 23, 7, 13, 5, 25, 3, 7, 14, \
           23, 24, 24, 11, 28, 7, 26, 28, 5, 11, 24, 5, 19, 9, 13, 16, 3, 8, 19, \
           13, 19, 5, 27, 4, 4, 24, 20, 27, 10, 17, 0, 15, 13, 5, 21, 19, 5, 7, \
           10, 19, 19, 10, 24, 8, 26, 21, 5, 22, 17, 28, 12, 10, 4, 7, 9, 17, \
           27, 24, 19, 22, 13, 10, 3, 28, 5, 28, 14, 9, 20, 16, 8, 17, 27, 20, \
           12, 1, 24, 8, 26, 6, 18, 16, 6, 1, 12, 22, 27, 25, 24, 27, 23, 18, \
           22, 4, 25, 0, 15, 7, 27, 26, 19, 15, 26, 24, 19, 27, 16, 4, 6, 18, 9, \
           24, 20, 27, 19, 13, 15, 26, 22, 4, 3, 8, 19, 13, 19, 5, 27, 4, 4, 16, \
           13, 17, 13, 19, 13, 2, 7, 19, 5, 10, 23, 7, 9, 26, 28, 9, 24, 5, 24, \
           28, 27, 20, 27, 1, 21, 10, 15, 22, 2, 25, 6, 11, 19, 19, 5, 24, 24, \
           28, 23, 7, 7, 1, 9, 14, 1, 7, 13, 21, 10, 3, 28, 5, 28, 14, 9, 27, \
           22, 1, 22, 12, 17, 3, 10, 4, 2, 28, 14, 24, 10, 13, 2, 7, 19, 5, 10, \
           23, 7, 9, 26, 19, 7, 19, 23, 18, 7, 13, 9, 19, 6, 26, 16, 28, 13, 18,
           24]

pt_koan = [24, 5, 3, 24, 9, 23, 1, 4, 21, 24, 20, 18, 15, 15, 3, 9, 2, 18, 19, \
           24, 15, 16, 18, 4, 18, 14, 13, 20, 24, 10, 9, 18, 23, 2, 18, 10, 2, \
           18, 10, 10, 15, 2, 18, 1, 3, 10, 5, 18, 3, 0, 2, 18, 5, 10, 4, 5, 1, \
           19, 0, 18, 4, 18, 9, 5, 18, 8, 18, 15, 24, 10, 23, 7, 8, 18, 9, 24, \
           15, 5, 18, 23, 17, 26, 24, 15, 16, 1, 23, 18, 9, 16, 16, 3, 18, 14, \
           13, 20, 24, 10, 9, 7, 8, 24, 16, 2, 24, 16, 19, 28, 9, 16, 2, 18, 19, \
           24, 15, 16, 18, 4, 15, 24, 10, 23, 10, 16, 10, 15, 24, 1, 3, 10, 5, \
           18, 10, 9, 15, 10, 23, 18, 26, 3, 1, 4, 8, 28, 23, 10, 23, 3, 9, 16, \
           8, 24, 1, 18, 24, 1, 3, 10, 5, 18, 10, 9, 19, 26, 8, 28, 23, 2, 3, 1, \
           6, 8, 16, 2, 18, 15, 16, 1, 23, 18, 9, 16, 24, 9, 23, 8, 18, 4, 24, \
           10, 15, 18, 23, 8, 10, 15, 8, 24, 9, 23, 16, 3, 16, 18, 20, 20, 2, \
           18, 19, 24, 15, 16, 18, 4, 2, 18, 19, 24, 15, 16, 18, 4, 15, 16, 3, \
           13, 13, 18, 23, 2, 18, 15, 16, 1, 23, 18, 9, 16, 24, 9, 23, 15, 24, \
           10, 23, 2, 18, 1, 3, 10, 5, 18, 2, 24, 16, 11, 1, 15, 16, 15, 24, 10, \
           23, 26, 3, 1, 8, 24, 1, 18, 9, 3, 1, 3, 10, 5, 18, 10, 9, 26, 3, 1, \
           4, 8, 28, 23, 10, 15, 2, 18, 10, 24, 9, 23, 2, 18, 15, 16, 1, 23, 18, \
           9, 16, 15, 7, 18, 4, 18, 18, 9, 20, 10, 6, 8, 16, 18, 9, 18, 23]

key_koan = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18, 0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

key_generator.setup(decryption_function=cry.decrypt_p_plus_k, ct=ct_koan, pt=pt_koan)
keys_koan = key_generator.getKeys()
solved = False
for item in keys_koan:
    if solved: break
    # we know
    if item['interrupter'] == 0:
        for k_i in item['keys']:
            if solved: break
            # can arbitrarily rotate a key so ... check each one
            rotated_keys = key_generator.getAllGematriaRations(list(k_i))
            for rotated_k_i in rotated_keys:
                hit = True
                for k1, k2 in zip(list(rotated_k_i)[:len(key_koan)], key_koan):
                    if k1 != k2:
                        hit = False
                if hit:
                    print(f'solved\nk_raw={key_koan}\nk_ans={rotated_k_i}')
                    int_found = item['interrupter']
                    # in some sense we don't care about transposition, as we have a working method regardless
                    transposition_found = item['transposition']
                    print(f'interrupter_raw {0} = {int_found} interrupter_ans')
                    print(f'transposition_raw L2R = {transposition_found} transposition_ans')
                    solved = True

if not solved:
    print(f'\nPRINT FAILED RESULTS')
    with open('out.txt', 'w') as f:
        [f.write(f'{v}\t') for v in keys_koan[0].keys()]
        f.write('\n')
        for item in keys_koan:
            for k, v in item.items():
                f.write(f'{v}\t')
            f.write('\n')
    input("ERRR NO HIT")

''' test 56.jpg '''
print('\nTEST WE CAN SOLVE 56.jpg')

ct_56_jpg = [25, 11, 22, 15, 4, 19, 26, 20, 3, 8, 3, 25, 5, 2, 6, 7, 7, 20, 25, \
             14, 3, 24, 13, 19, 23, 23, 1, 6, 7, 20, 23, 9, 26, 11, 5, 0, 27, 25, \
             16, 13, 12, 24, 2, 5, 25, 5, 23, 0, 9, 27, 18, 0, 9, 5, 21, 4, 0, 25, \
             10, 4, 23, 18, 15, 26, 11, 28, 1, 21, 7, 14, 3, 19, 28, 7, 0, 4, 6, \
             27, 21, 4, 17, 25, 9, 1, 15]

pt_56_jpg = [24, 9, 18, 9, 23, 7, 10, 2, 10, 9, 2, 18, 23, 18, 18, 13, 7, 18, 17, \
             2, 18, 4, 18, 18, 14, 10, 15, 16, 15, 24, 13, 24, 6, 18, 2, 24, 16, \
             8, 24, 15, 8, 18, 15, 16, 3, 10, 16, 10, 15, 2, 18, 23, 1, 16, 26, 3, \
             0, 18, 1, 18, 4, 26, 13, 10, 20, 6, 4, 10, 19, 16, 3, 15, 18, 18, 5, \
             3, 1, 16, 2, 10, 15, 13, 24, 6, 18]

key_56_jpg = [2, 3, 5, 7, 11, 13, 17, 19, 23, 0, 2, 8, 12, 14, 18, 24, 1, 3, 9, 13, \
              15, 21, 25, 2, 10, 14, 16, 20, 22, 26, 11, 15, 21, 23, 4, 6, 12, 18, \
              22, 28, 5, 7, 17, 19, 23, 25, 8, 20, 24, 26, 1, 7, 9, 19, 25, 2, 8, \
              10, 16, 20, 22, 3, 17, 21, 23, 27, 12, 18, 28, 1, 5, 11, 19, 25, 2, \
              6, 12, 20, 24, 3, 13, 15, 25, 27, 4]

key_generator.setup(decryption_function=cry.decrypt_p_plus_k, ct=ct_56_jpg, pt=pt_56_jpg)
keys_56_jpg = key_generator.getKeys()
solved = False
for item in keys_56_jpg:
    if solved: break
    # we know
    if item['interrupter'] == 0:
        for k_i in item['keys']:
            if solved: break
            # can arbitrarily rotate a key so ... check each one
            rotated_keys = key_generator.getAllGematriaRations(list(k_i))
            for rotated_k_i in rotated_keys:
                hit = True
                for k1, k2 in zip(list(rotated_k_i), key_56_jpg):
                    if k1 != k2:
                        hit = False
                if hit:
                    print(f'solved\nk_raw={key_56_jpg}\nk_ans={rotated_k_i}')
                    int_found = item['interrupter']
                    # in some sense we don't care about transposition, as we have a working method regardless
                    transposition_found = item['transposition']
                    print(f'interrupter_raw {0} = {int_found} interrupter_ans')
                    print(f'transposition_raw L2R = {transposition_found} transposition_ans')
                    solved = True
                    break

# If script does not get here it's broke
input("\n**********************\nTEST FIN: ALL TESTS PASSED")
input()
