'''
A simple script to show key-generation from a list of cribs
shifts, transpositions, interrupters depend on configuration of KeyGenerator
Decryption functions are in arithmetic_cryption_methods
Cribs are simple text file in standard english plaintext
Here we score a text using log_probability of n-grams adn check to see if
prime sequence or Fibonacci sequence is in key
'''
import key_generator as gd
import cryption_methods_of_2_variables as cry
import gematria as gem
import runeglish_tests as runeglish_test
import time
import statistics

t0 = time.time()

# key generator object
key_generator = gd.KeyGenerator()

# 54.jpg first two words
ct_raw = [24, 19, 21, 23, 27, 2, 14, 10, 19, 27, 23, 13, 21, 1, 7, 24, 19]


def key_in_sequence(key, sequence):
    return any(sequence[i:i + len(key)] == key for i in range(len(sequence) - len(key) + 1))


def sequence_match(key):
    '''
    check a zero-shifted key matches a pre-defined sequence
    '''
    if key_in_sequence(key, [0, 1, 3, 5, 9, 11]):
        print('Prime key found')
        return True
    elif key_in_sequence(key, [0, 0, 1, 2, 4, 7]):
        print('Fibonacci_1 key found')
        return True
    elif key_in_sequence(key, [0, 1, 2, 4, 7]):
        print('Fibonacci_2 key found')
        return True
    elif key_in_sequence(key, [0, 1, 4, 12, 1, 0]):
        print('Fibonacci_3 key found')
        return True
    elif key_in_sequence(key, [0, 1, 6, 19, 26, 27]):
        print('Fibonacci_4 key found')
        return True
    return False


# cribs for this CT
cribs_text = []
cribs_rune_pos = []
score2 = []
with open("1 8 8 cribs.txt", 'r') as f:
    for line in f.readlines():
        cribs_text.append(line)
        line_runes = gem.translate_to_gematria(line.rstrip(), return_string=False)
        score = runeglish_test.scoreWithNoWordLengthInfo(''.join([x for x in line_runes if x != ' ']))
        score2.append([sum([x[0] for x in score['log_prob']['char2']]),
                       sum([x[0] for x in score['log_prob']['char3']]),
                       sum([x[0] for x in score['log_prob']['char4']])])
        cribs_rune_pos.append(gem.rune_to_position(line_runes, keep_space=False))
# print(score2)

# decryption functions to use
decyrption_methods = {
    'p_plus_k': cry.decrypt_p_plus_k,
    'p_minus_k': cry.decrypt_p_minus_k,
    'k_minus_p': cry.decrypt_k_minus_p,
    'decrypt_p_multiply_k': cry.decrypt_p_multiply_k,
    'decrypt_p_divide_k': cry.decrypt_p_divide_k,
    'decrypt_k_divide_p': cry.decrypt_k_divide_p,
}

key_hits = []
print('start run')
hits = []
final_data = []
for counter, pt_raw in enumerate(cribs_rune_pos):
    # data out here
    this_crib_key_dict = key_generator.getKeysForDecryptionFunctions(decryption_function_dict=decyrption_methods,
                                                                     ct=ct_raw, pt=pt_raw)
    # now loop over all keys and see if any "look like runeglish"
    llll = len(this_crib_key_dict['keys'])
    for k, v in this_crib_key_dict['keys'].items():
        # remove errors (These occur when a combination of method,ct,pt cant give a defined answer
        # could replace errors with all possible values, if number of errors is nto too high, etc.
        k_remove_errors = [x for x in k if x != 'e']
        # check for a zero-shifted sequence
        if len(k_remove_errors) > 5:
            if sequence_match(k_remove_errors[:6]):
                key_hits.append([counter, k_remove_errors, "SEQ MATCH"])
                print(f'{len(key_hits)} HIT!! SEQUENCE = {k_remove_errors} ')

        # get all gematria rotaitons of thsi key
        rotated_keys = key_generator.getAllGematriaRations(k_remove_errors)
        for rotated_key_i in rotated_keys:
            rotated_key_i_2 = [x for x in rotated_key_i if x != 'e']
            rune_string = ''.join(gem.position_to_rune(rotated_key_i_2))

            # score text and compare to some chosen threshold, user to define sensitivity
            score = runeglish_test.scoreWithNoWordLengthInfo(rune_string)
            py_log_prob_sum = [sum([x[0] for x in score['log_prob']['char2']]),
                               sum([x[0] for x in score['log_prob']['char3']]),
                               sum([x[0] for x in score['log_prob']['char4']])]
            # normalize
            d = [py_log_prob_sum[0] / 5.3, py_log_prob_sum[1] / 3.4, py_log_prob_sum[2] / 2.3]
            # if good enough keep
            if statistics.mean(d) > 1.2:
                key_runes = ' '.join(gem.position_to_latin(rotated_key_i_2, join=False))
                kept_keys = [sublist[1] for sublist in key_hits]
                if key_runes not in kept_keys:
                    key_hits.append([counter, key_runes, py_log_prob_sum])
                    print(f'{len(key_hits)} HIT!! {key_hits[-1]}')

    num_keys = len(this_crib_key_dict['keys'])
    print(f'{time.time() - t0} {counter}/{len(cribs_rune_pos)}. {cribs_text[counter].rstrip()} {num_keys}')

input()
input()
input()
