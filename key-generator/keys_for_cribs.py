'''
A simple script to show key-generation from a list of cribs
shifts, transpositions, interrupters depend on configuration of KeyGenerator
Decryption functions are in arithmetic_cryption_methods
Cribs are simple text file in standard english plaintext
In this example Keys are written to text file
This (mainly) for example purposes only, if you really want to save all key data
For large crib-lists suggestion is to use a better file format (HDF5, etc.)
'''
import key_generator as gd
import cryption_methods_of_2_variables as cry
import gematria as gem
import time

t0 = time.time()
# key generator object
key_generator = gd.KeyGenerator()

# 54.jpg first two words
ct_raw = [24, 19, 21, 23, 27, 2, 14, 10, 19]
# cribs for this CT
cribs_text = []
cribs_rune_pos = []
with open("./data/test_cribs.txt", 'r') as f:
    for line in f.readlines():
        cribs_text.append(line)
        line_runes = gem.translate_to_gematria(line.rstrip(), return_string=False)
        cribs_rune_pos.append(gem.rune_to_position(line_runes, keep_space=False))

# maybe just keys
generated_keys = open("./data/generated_keys.txt", 'w')
# meta data used top generate key (not used)
generated_key_data = open("./data/generated_keys_data.txt", 'w')

final_data = []
for counter, pt_raw in enumerate(cribs_rune_pos):
    # data out here
    this_crib_key_dict = {}
    this_crib_key_dict['pt_raw'] = pt_raw
    this_crib_key_dict['ct_raw'] = ct_raw
    these_keys = []
    for method_function in cry.all_decrypt_methods_of_2_variables:
        key_generator.setup(decryption_function=method_function, ct=ct_raw, pt=cribs_rune_pos[0])
        #  get keys for this CT/PT pair
        these_keys = key_generator.getKeys()
        # shift keys to zero at first element and concatenate repetitions
        for next_keylist in these_keys:
            for key in next_keylist['keys']:
                key_shift2zero = tuple(key_generator.shiftToZero(key))
                key_meta_data = {'interrupter': next_keylist['interrupter'],
                                 'interrupter_pos': next_keylist['interrupter'],
                                 'transposition': next_keylist['interrupter'],
                                 'direction_c': next_keylist['direction_c'],
                                 'direction_p': next_keylist['direction_p'],
                                 'rotation_ct': next_keylist['rotation_ct'],
                                 'rotation_pt': next_keylist['rotation_pt'],
                                 'decryption_method': method_function.__name__
                                 }
                if key_shift2zero in this_crib_key_dict:
                    this_crib_key_dict[key_shift2zero].append(key_meta_data)
                else:
                    generated_keys.write(','.join([str(x) for x in key_shift2zero]) + ':')
                    this_crib_key_dict[key_shift2zero] = [key_meta_data]
        generated_keys.flush()
    generated_keys.write('\n')
    print(
        f'{time.time() - t0} {counter}/{len(cribs_rune_pos)}. {cribs_text[counter].rstrip()} {len(this_crib_key_dict)}')
    # if you want a big list of all data
    # final_data.append(this_crib_key_dict)

print(len(this_crib_key_dict))


