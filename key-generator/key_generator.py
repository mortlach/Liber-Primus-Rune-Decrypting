'''

This class generates keys for a given plaintext / ciphertext
Text transpositions can be defined,

'''

from itertools import product
import random


class KeyGenerator:
    all_gematria_directions = ['atbash','normal']

    def __init__(self, decryption_function=None, ct=None, pt=None, decrypt_variables_count=2, **kwargs):
        self.data = {}

    def setup(self, decryption_function, ct, pt, decrypt_variables_count = 2, **kwargs):
        '''
        init some things
        :param decryption_function:
        :param ct:
        :param pt:
        :param decrypt_variables_count:
        :param kwargs:
        :return:
        '''
        self.data["decryption_function"] = decryption_function
        self.data["raw_ct"] = ct
        self.data["raw_pt"] = pt
        self.data["transpositions"] = ['L2R', 'R2L']
        self.data['gematria_directions'] = list(product(KeyGenerator.all_gematria_directions, repeat=2))
        self.data['decrypt_variables_count'] = decrypt_variables_count
        self.data['variable_gematria_rotations'] = [list(x) for x in list(
            product(list(range(28)), repeat=self.data['decrypt_variables_count']))]
        # extra keys
        for k, v in kwargs:
            self.data[k] = v
        # can now calculate these, which are unambiguous and defined
        self.data["interrupted_data"] = self.getInterrupterData(ct, pt)

    def getInterrupterData(self,ct,pt):
        '''
        for passed ct return all combinations with all possible interrupters
        following interrupter rules
        '''
        r = [[[-1,[]], ct, pt]]
        interrupter_position = self.getInterrupterPositions(ct, pt)
        for i_pos in interrupter_position:
            r.append([i_pos,
                      [i for j, i in enumerate(ct) if j not in i_pos[1]],
                      [i for j, i in enumerate(pt) if j not in i_pos[1]]
                      ])
        return r

    def getInterrupterPositions(self, ct, pt):
        '''
        return positions of possible interrupters
        interrupter must be :
            all occurrences of a rune in PT have to match CT
            rune at same position
        '''
        unique_pt_runes = set(pt)
        r = []
        for pt_rune in unique_pt_runes:
            pt_pos = [i for i, p in enumerate(pt) if p == pt_rune]
            ct_pos = [i for i, c in enumerate(ct) if c == pt_rune]
            if set(pt_pos).issubset(ct_pos):
                r.append([pt_rune, pt_pos])
        return r

    def getTransposesText(self, text, transposition_key):
        '''
        define possible transpositions here, 2 obvious ones to start,
        but they can be basically arbitrary
        :param text: runes
        :param transposition_key: which transposition to use, must be defined in body
        :return:
        '''
        if transposition_key == 'L2R':
            transposition = list(range(len(text[0])))
        elif transposition_key == 'R2L':
            transposition = list(range(len(text[0])))
            transposition.reverse()
        else:
            print(f'transposition_key {transposition_key} not found, using default order')
            transposition = list(range(len(text[0])))
        r = [[item[i] for i in transposition] for item in text]
        return r

    def getKeys(self):
        '''
        loop over all possible 'stuff' and generate a key for this crib and cipher_text
        :return: all the keys
        '''
        r = []
        for interrupter_data, ct, pt in self.data["interrupted_data"]:
            temp = {}
            temp['interrupter'] = interrupter_data[0]
            temp['interrupter_pos'] = interrupter_data[1]
            for transposition in self.data["transpositions"]:
                temp['transposition'] = transposition
                ct_t, pt_t = self.getTransposesText([ct, pt], transposition)
                # todo do all direciton combos
                for direction in self.data['gematria_directions']:
                    temp['direction_c'] = direction[0]
                    temp['direction_p'] = direction[1]
                    for rotation in self.data['variable_gematria_rotations']:
                        temp['rotation_ct'] = rotation[0]
                        temp['rotation_pt'] = rotation[1]
                        ct_tr = self.getGematriaRotation(ct_t, rotation[0], temp['direction_c'])
                        pt_tr = self.getGematriaRotation(pt_t, rotation[1], temp['direction_p'])
                        keys = self.data["decryption_function"](ct_tr,pt_tr)
                        temp['pt_tr'] = pt_tr
                        temp['ct_tr'] = ct_tr
                        temp['keys'] = keys
                        r.append(temp.copy())
                        # for k, v in temp.items():
                        #     print(f'{k} {v}')
        #print(f'found {len(r)} combinations')
        return r

    def getGematriaRotation(self, data, shift, direction=None):
        '''
        add a shift or atbash then shift
        :param data:
        :param shift:
        :param direction:
        :return:
        '''
        if direction == 'atbash':
            return [(28 - d + shift) % 29 if type(d) == int else d for d in data]
        return [(d + shift) % 29 if type(d) == int else d for d in data]

    def getAllGematriaRations(self, data):
        '''
        if you know, you know
        :param data:
        :return:
        '''
        r = []
        for direction in ['atbash','normal']:
            for shift in range(29):
                r.append(self.getGematriaRotation(data,shift,direction))
        return r

    def getTransRots(self,p):
        '''
        choose some random stuff
        :param p:
        :return:
        '''
        return {
            "interrupter": random.choice([-1] + list(set(p))),
            "transposition": random.choice(['L2R', 'R2L']),
            "p_gematria_direction": random.choice(['normal', 'atbash']),
            "k_gematria_direction": random.choice(['normal', 'atbash']),
            #"transposition": random.choice(['L2R']),
            #"p_gematria_direction": random.choice(['atbash']),
            #"k_gematria_direction": random.choice(['atbash']),
            "k_gematria_shift": random.choice(range(29)),
            "p_gematria_shift": random.choice(range(29))
        }

    def shiftToZero(self, data):
        d0 = [d for d in data if type(d) == int ][0]
        return [ (d-d0) % 29 if type(d) == int else d for d in data]

    def random_encrypt(self,p_raw, k_raw, enc_function):
        '''
        encrypt passed data choosing random interrupter, transpositions, shifts
        :param p_raw:
        :param k_raw:
        :param enc_function:
        :return: dict of all variables
        '''
        #
        data = self.getTransRots(p_raw)
        data['p_raw'] = p_raw
        data['k_raw'] = k_raw
        data['enc_function'] = enc_function
        # first get the interrupted data
        data['interrupter_pos'] = [i for i, p in enumerate(data['p_raw']) if p == data['interrupter']]
        data['interrupter_p_raw'] = [p for i,p in enumerate(data['p_raw']) if i not in data['interrupter_pos']]
        data['interrupter_k_raw'] = data['k_raw'][:len(data['interrupter_p_raw'])]
        # next apply tranposition to plaintext
        data['transpose_interrupter_p_raw'] = \
        self.getTransposesText([data['interrupter_p_raw']], data['transposition'])[0]

        # rotate the plaintext / key
        data['p_to_encrypt'] = self.getGematriaRotation(data['transpose_interrupter_p_raw'],
                                                        data['p_gematria_shift'], data['p_gematria_direction'])
        data['k_to_encrypt'] = self.getGematriaRotation(data['k_raw'], data['k_gematria_shift'],
                                                        data['k_gematria_direction'])
        # apply encryption function
        data['c_raw'] = enc_function(data['p_to_encrypt'], data['k_to_encrypt'])
        # un - tranpoose (atm Assumes this inverse function is correct!) TODO better inverse transpose
        data['c_raw_untransposed'] = self.getTransposesText([data['c_raw']], data['transposition'])[0]
        # re-insert interrupter
        data['cipher_text'] = data['c_raw_untransposed']
        for i in data['interrupter_pos']:
            data['cipher_text'].insert(i, data['interrupter'])
        # data['cipher_text'] = [data['p_raw'][i] if data['p_raw'][i] == data['interrupter'] else c for i, c in enumerate(data['c_raw_untransposed'])]
        #
        # for k,v in data.items():
        #     print(f'{k} {v}')
        return data

    def test_solve(self, encrypt_function,decrypt_function, p_in = None, k_in= None, skip_key_errors = True , max_key_error_frac = 0.25 ):
        '''
            MUST PASS THIS TEST
            pass in plaintext and key and encrypt it with ran interrupters, transpose shift etc.
            then see if we can decrypt it and find exactly same key
            to count as a "true" solve require getting correct interrupter and key,
            gematria rotations are often degenerate, no need for exact match
        :param encrypt_function:
        :param decrypt_function:
        :param p_in: plaintext
        :param k_in: key
        :return:
        '''
        if p_in:
            p_raw = p_in
        else:
            ''' test "for everything that lives is holy" and prime keys'''
            p_raw = [0, 3, 4, 18, 1, 18, 4, 26, 2, 21, 2, 24, 16, 20, 10, 1, 18, 15, 10, 15, 8, 3, 20, 26]
            ''' or do something random  '''
            p_raw = random.choices(list(range(29)), k=20)
        if k_in:
            k_raw = k_in
        else:
            ''' prtime key  '''
            k_raw = [x % 29 for x in
                     [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89]]
            ''' or do something random  '''
            k_raw = random.choices(list(range(29)), k=len(p_raw))
        # generate encrypted data
        test_enc = self.random_encrypt(p_raw, k_raw, enc_function=encrypt_function)
        # set_up decrypter
        self.setup(decryption_function=decrypt_function, ct=test_enc['cipher_text'], pt=test_enc['p_raw'])
        # get all keys
        all_keys = self.getKeys()
        # set flags
        not_solved = True
        # iterate over generated keys to find known answer
        for this_k in all_keys:
            if this_k['interrupter'] == test_enc['interrupter']:
                for k_i in this_k['keys']:
                    # can arbitrarily rotate a key so ... check each one
                    rotated_keys = self.getAllGematriaRations(list(k_i))
                    for rotated_k_i in rotated_keys:
                        key_error_count = rotated_k_i.count('e')
                        if key_error_count > 0:
                            key_error_frac = float(rotated_k_i.count('e')) / float(len(rotated_k_i))
                        else:
                            key_error_frac = 0
                        if max_key_error_frac > key_error_frac:
                            hit = True
                            for k1, k2 in zip(list(rotated_k_i), k_raw):
                                if skip_key_errors and (k1 == 'e'):
                                    pass
                                elif skip_key_errors and (k2 == 'e'):
                                    pass
                                elif k1 != k2:
                                    hit = False
                                else:
                                    pass
                            if hit:
                                print(f'solved\nk_raw={k_raw}\nk_ans={rotated_k_i}')
                                int_raw = test_enc['interrupter']
                                int_found=this_k['interrupter']
                                # in some sense we don't care about transposition, as we have a working method regardless
                                transposition_raw=test_enc['transposition']
                                transposition_found=this_k['transposition']
                                print(f'interrupter_raw {int_raw} = {int_found} interrupter_ans')
                                print(f'transposition_raw {transposition_raw} = {transposition_found} transposition_ans')
                                return
        if not_solved:
            print(f'\nPRINT FAILED RESULTS')
            for k,v in test_enc.items():
                print(f'{k} = {v}')
            with open('out.txt', 'w') as f:
                [f.write(f'{v}\t') for v in all_keys[0].keys()]
                f.write('\n')
                for item in all_keys:
                    for k, v in item.items():
                        f.write(f'{v}\t')
                    f.write('\n')
            input("ERRR NO HIT")


    def getKeysForDecryptionFunctions(self, decryption_function_dict, ct, pt):
        '''
        Get the keys for a given ct/pt pair and a dict containing decryption_functions
        '''
        # data out here
        data_dict = {}
        data_dict['pt_raw'] = pt
        data_dict['ct_raw'] = ct
        data_dict['keys'] = {}
        # loop over each method adn add keys
        for method_text, method_function in decryption_function_dict.items():
            self.setup(decryption_function=method_function, ct=ct, pt=pt)
            #  get keys for this CT/PT pair
            these_keys = self.getKeys()
            # shift keys to zero and concatenate repetitions this_data
            for next_keylist in these_keys:
                for key in next_keylist['keys']:
                    key_shift2zero = tuple(self.shiftToZero(key))
                    key_meta_data = {'interrupter': next_keylist['interrupter'],
                                     'interrupter_pos': next_keylist['interrupter'],
                                     'transposition': next_keylist['interrupter'],
                                     'direction_c': next_keylist['direction_c'],
                                     'direction_p': next_keylist['direction_p'],
                                     'rotation_ct': next_keylist['rotation_ct'],
                                     'rotation_pt': next_keylist['rotation_pt'],
                                     'decryption_method':  method_function.__name__}
                    if key_shift2zero in data_dict:
                        data_dict['keys'] [key_shift2zero].append(key_meta_data)
                    else:
                        data_dict['keys'] [key_shift2zero] = [key_meta_data]
        return data_dict

