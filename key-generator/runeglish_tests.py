'''
    basic implementation, should be easy to modify (&improve!) for your particular needs
'''
import math
import csv

# sigmoid funciton paramters fro runeglish "score"
from raw_scoring_data.reProbChar2 import reProbChar2
from raw_scoring_data.reProbChar3 import reProbChar3
from raw_scoring_data.reProbChar4 import reProbChar4
from raw_scoring_data.reProbRB2 import reProbRB2
from raw_scoring_data.reProbRB3 import reProbRB3
from raw_scoring_data.reProbGNG2 import reProbGNG2
from raw_scoring_data.reProbGNG3 import reProbGNG3



def readcsvtodict(fp):
    with open(fp, mode='r',encoding='utf-8') as file:
        return {r[0]: [float(r[1]), int(r[2])] for r in csv.reader(file)}
# Log Probabilty data for 7 different methods
log_prob = {}
log_prob["char"] = {}
log_prob["char"][2] = readcsvtodict('./raw_scoring_data/ngChar2LogProb.csv')
log_prob["char"][3] = readcsvtodict('./raw_scoring_data/ngChar3LogProb.csv')
log_prob["char"][4] = readcsvtodict('./raw_scoring_data/ngChar4LogProb.csv')
log_prob["rb"] = {}
log_prob["rb"][2] = readcsvtodict('./raw_scoring_data/ngRB2LogProb.csv')
# github does not allow files that are too large, so data has been split 
log_prob["rb"][3] = {**readcsvtodict('./raw_scoring_data/ngRB3LogProbA.csv'), **readcsvtodict('./raw_scoring_data/ngRB3LogProbB.csv')}
log_prob["gng"] = {}
log_prob["gng"][2] = readcsvtodict('./raw_scoring_data/ngGNG2LogProb.csv')
log_prob["gng"][3] = readcsvtodict('./raw_scoring_data/ngGNG3LogProb.csv')
runeglish_score= {}
runeglish_score["char"] = {}
runeglish_score["char"][2] = reProbChar2
runeglish_score["char"][3] = reProbChar3
runeglish_score["char"][4] = reProbChar4
runeglish_score["rb"] = {}
runeglish_score["rb"][2] = reProbRB2
runeglish_score["rb"][3] = reProbRB3
runeglish_score["gng"] = {}
runeglish_score["gng"][2] = reProbGNG2
runeglish_score["gng"][3] = reProbGNG3

def charLogProb(runes, nglength):
    '''
        runes: single list of runes, no spaces, "ᚠᚩᚱᚪᛚᛚᛁᛋᛋᚪᚳᚱᛖᛞ" 
        nglength: 2 to 4 
        get log prob and ng freq in data 
    '''
    if not nglength > 1 and nglength < 6 : raise Exception(f'charScore nglength = {nglength}, not 2 to 5')
    ngrams = [runes[i:i+nglength] for i in range(0,len(runes)-nglength+1)]
    scores = [log_prob["char"][nglength].get(x, [0.0,0]) for x in ngrams]
    return scores

def rbLogProb(runes_with_word_length_info, nglength):
    '''
        for list of [runes, index in word, word length]
        e.g. "ᛁᚾ  ᛒᚳ ᚦᛖ ᚣᛠᚱ  ᚷᚢᛁᚾᚾᛖᛋᛋ" would give:
        [['ᛁ', 0, 2], ['ᚾ', 1, 2], ['ᛒ', 0, 2], ['ᚳ', 1, 2], ['ᚦ', 0, 2], ['ᛖ', 1, 2], ['ᚣ', 0, 3], ['ᛠ', 1, 3], ['ᚱ', 2, 3], ['ᚷ', 0, 8], ['ᚢ', 1, 8], ['ᛁ', 2, 8], ... ]
        nglength: 2 or 3 
    '''
    if not nglength > 1 and nglength < 4 : raise Exception(f'rbScore nglength = {nglength}, not 2 or 3')
    keys = getWordInfoKey(runes_with_word_length_info, nglength)
    lp = [log_prob["rb"][nglength].get(x, [0.0,0]) for x in keys]
    return lp

def gngLogProb(runes_with_word_length_info, nglength):
    '''
        for list of [runes, index in word, word length]
        e.g. "ᛁᚾ  ᛒᚳ ᚦᛖ ᚣᛠᚱ  ᚷᚢᛁᚾᚾᛖᛋᛋ" would give:
        [['ᛁ', 0, 2], ['ᚾ', 1, 2], ['ᛒ', 0, 2], ['ᚳ', 1, 2], ['ᚦ', 0, 2], ['ᛖ', 1, 2], ['ᚣ', 0, 3], ['ᛠ', 1, 3], ['ᚱ', 2, 3], ['ᚷ', 0, 8], ['ᚢ', 1, 8], ['ᛁ', 2, 8], ... ]
        nglength: 2 or 3 
    '''
    if not nglength > 1 and nglength < 4 : raise Exception(f'rbScore nglength = {nglength}, not 2 or 3')
    keys = getWordInfoKey(runes_with_word_length_info, nglength)
    scores = [log_prob["gng"][nglength].get(x, [0.0,0]) for x in keys]
    return scores


def getWordInfoKey(data, length):
    '''
        convert rune string with word spacing to input for 'RB' adn 'GNG' log probability methods 
        for list of [runes, index in word, word length]
        e.g. "ᛁᚾ ᛒᚳ ᚦᛖ ᚣᛠᚱ  ᚷᚢᛁᚾᚾᛖᛋᛋ" would give:
        [['ᛁ', 0, 2], ['ᚾ', 1, 2], ['ᛒ', 0, 2], ['ᚳ', 1, 2], ['ᚦ', 0, 2], ['ᛖ', 1, 2], ['ᚣ', 0, 3], ['ᛠ', 1, 3], ['ᚱ', 2, 3], ['ᚷ', 0, 8], ['ᚢ', 1, 8], ['ᛁ', 2, 8], ... ]
    '''
    keys = []
    for i in range(0,len(data)-length+1):
        next_chunk = data[i:i+length]
        nk = []
        for item in next_chunk:
            nk.append(",".join([str(x) for x in item]))
        keys.append(",".join(nk))
    return keys

def getIoC(text, c = 29):
    ''' index of coinsidence for c things '''
    text_no_space = text.replace(" ", "")
    counts = [[x, text_no_space.count(x)] for x in set(text_no_space)]
    text_len = len(text_no_space)
    if text_len == 0:
        return 0
    else:
        return c * sum([x[1]*(x[1]-1) for x in counts]) / (text_len*(text_len-1))

def charRuneglishScore(total_score, ngram_length, ngram_count):
    ''' imported magic numbers define a sigmoid used to estimate runeglish "score" '''
    a, b, c, d, = runeglish_score["char"][ngram_length][ngram_count]
    return sigmoid(a, b, c, d, total_score)

def runeglishScore(d, total_score, ngram_length, ngram_count):
    ''' imported magic numbers define a sigmoid used to estimate runeglish "score" '''
    a, b, c, d, = d[ngram_length][ngram_count]
    return sigmoid(a, b, c, d, total_score)

def sigmoid(a, b, c, d, log_prob_total):
    '''
        A sigmoid function. 
        to cope with numerical stuff, return values clipped to be between 0 and 1   
    '''
    r = a / (1 + b * math.exp((-c * (log_prob_total - d))))
    return 0.0 if r < 0.0 else 1.0 if r > 1.0 else r

def logProbRunesWithNoWordLengthKey(data):
    '''
        param data: is a string of runes, e.g. "ᚠᚩᚱᚪᛚᛚᛁᛋᛋᚪᚳᚱᛖᛞ"
    '''
    r = {}
    r['char2'] = charLogProb(data, 2)
    r['char3'] = charLogProb(data, 3)
    r['char4'] = charLogProb(data, 4)
    return r

def logProbRunesWithWordLengthKey(data):
    '''
        data: e.g. [['ᛁ', 0, 2], ['ᚾ', 1, 2], ['ᛒ', 0, 2], ['ᚳ', 1, 2], ['ᚦ', 0, 2], ['ᛖ', 1, 2], ['ᚣ', 0, 3], ['ᛠ', 1, 3], ['ᚱ', 2, 3], ['ᚷ', 0, 8], ['ᚢ', 1, 8], ['ᛁ', 2, 8], ... ]
    '''
    rune_text = ''.join([x[0] for x in data])
    r = logProbRunesWithNoWordLengthKey(rune_text)
    r['gng2'] = gngLogProb(data, 2)
    r['gng3'] = gngLogProb(data, 3)
    r['rb2'] = rbLogProb(data, 2)
    r['rb3'] = rbLogProb(data, 3)
    return r

def runeglishScoreWithWordLengthKey(data):
    r = runeglishScoreWithNoWordLengthKey(data)
    r['rb2'] = runeglishScore(runeglish_score["rb"], sum([x[0] for x in data['rb2']]), 2, len(data['rb2']))
    r['rb3'] = runeglishScore(runeglish_score["rb"], sum([x[0] for x in data['rb3']]), 3, len(data['rb3']))
    r['gng2'] = runeglishScore(runeglish_score["gng"], sum([x[0] for x in data['gng2']]), 2, len(data['gng2']))
    r['gng3'] = runeglishScore(runeglish_score["gng"], sum([x[0] for x in data['gng3']]), 3, len(data['gng3']))
    return r

def runeglishScoreWithNoWordLengthKey(data):
    r = {}
    r['char2'] = runeglishScore(runeglish_score["char"], sum([x[0] for x in data['char2']]), 2, len(data['char2']))
    r['char3'] = runeglishScore(runeglish_score["char"], sum([x[0] for x in data['char3']]), 3, len(data['char3']))
    r['char4'] = runeglishScore(runeglish_score["char"], sum([x[0] for x in data['char4']]), 4, len(data['char4']))
    return r

def scoreWithWordLengthInfo(data):
    r = {}
    r['log_prob'] = logProbRunesWithWordLengthKey(data)
    r['score'] = runeglishScoreWithWordLengthKey(r['log_prob'] )
    return r

def scoreWithNoWordLengthInfo(data):
    r = {}
    r['log_prob'] = logProbRunesWithNoWordLengthKey(data)
    r['score'] = runeglishScoreWithNoWordLengthKey(r['log_prob'] )
    return r


def do_benchmark():
    # First test calculate IoC for some text in english and runeglish
    import gematria
    import statistics
    alice = "alice was beginning to get very tired of sitting by her sister on the bank  and of having nothing to do  once or twice she had peeped into the book her sister was reading  but it had no pictures or conversations in it   and what is the use of a book   thought alice  without pictures or conversations   so she was considering in her own mind  as well as she could  for the hot day made her feel very sleepy and stupid   whether the pleasure of making a daisy chain would be worth the trouble of getting up and picking the daisies  when suddenly a white rabbit with pink eyes ran close by her"
    print(f'IoC english text = {getIoC(alice,26)}')
    print(f'IoC runeglish text = {getIoC(gematria.sentence_to_gematria(alice))}')
    ##
    # second text is to calculate runeglish score for set text and compare to pre-computed version
    def readbenchmarkcsv(fp):
        l = []
        with open(fp, mode='r', encoding='utf-8') as file:
            for row in csv.reader(file,quoting = csv.QUOTE_NONNUMERIC):
                l.append(row)
        return l
    # text to score
    test_text = [[x[0],int(x[1]),int(x[2])] for x in readbenchmarkcsv('./benchmark_data/set_text_runewordswithposindex.csv')]
    # pre-computed results from different application
    test_data_benchmark = {}
    chunk_sizes = [7,12,20]
    test_data_benchmark[chunk_sizes[0]] = readbenchmarkcsv('./benchmark_data/set_text_rg_score_7.csv')
    test_data_benchmark[chunk_sizes[1]] = readbenchmarkcsv('./benchmark_data/set_text_rg_score_12.csv')
    test_data_benchmark[chunk_sizes[2]] = readbenchmarkcsv('./benchmark_data/set_text_rg_score_20.csv')
    # results will go here
    test_data_results = {}
    # d =len(data['char2'])
    keys =  ['char2','char3','char4','rb2','rb3','gng2','gng3']
    for cs in chunk_sizes:
        test_data_results[cs] = []
        chunks = [test_text[i:i+cs] for i in range(0,len(test_text)-cs+1)]
        for i, chunk in enumerate(chunks):
            # print(f'next chunk = {chunk}')
            sc = scoreWithWordLengthInfo(chunk)
            py_log_prob = [sc['log_prob'][x] for x in keys]
            py_score = [sc['score'][x] for x in keys]
            bench_score = test_data_benchmark[cs][i]
            # print(f'py_log_prob = {py_log_prob}')
            # print(f'py_score = {py_score}')
            # print(f'bench_score = {bench_score}')
            # take difference between py_score and benchmark
            sub = list()
            for item1, item2 in zip(py_score, bench_score):
                item = item1 - item2
                sub.append(item)
            # print(f'sub = {sub}')
            test_data_results[cs].append( sub  )
        # rms of the difference, if 'small' all is good !
        rms = math.sqrt(statistics.mean([math.pow(x,2) for x in [item for sublist in test_data_results[cs] for item in sublist]]))
        print(f'Chunk size = {cs} delta-rms with benchmark = {rms} (should be a small number, <10^-5)')


if __name__ == '__main__':
    print(f'************ Is it runeglish ???? *************')
    print(f'\n\tMethods to accurately estimate if a text fragment in runes is valid english')
    print(f'\n************ Running tests *************')
    print(f'Example scoring, using  "ᚠᚩᚱ ᚪᛚᛚ ᛁᛋ ᛋᚪᚳᚱᛖᛞ"')
    print(f'*** Type 1 methods ***')
    print(f'These just use the runes, With No Word Length Information')
    sample_input = "ᚠᚩᚱᚪᛚᛚᛁᛋᛋᚪᚳᚱᛖᛞ"
    print(f'sample_input = {sample_input}')
    print(f'scoreWithWordNoLengthInfo returns a dictionary with log_probability data, and score data, for 3 different methods char2, char3 and char4')
    print(f'char2, sample_text is chunked into length 2 strings and each scored: [ᚠᚩ, ᚩᚱ, ᚱᚪ, ᚪᛚ, ᛚᛚ, ᛚᛁ, ᛁᛋ, ᛋᛋ, ᛋᚪ, ᚪᚳ, ᚳᚱ, ᚱᛖ, ᛖᛞ] ')
    print(f'char3, sample_text is chunked into length 3 strings and each scored: [ᚠᚩᚱ, ᚩᚱᚪ, ᚱᚪᛚ, ᚪᛚᛚ, ᛚᛚᛁ, ᛚᛁᛋ, ᛁᛋᛋ, ᛋᛋᚪ, ᛋᚪᚳ, ᚪᚳᚱ, ᚳᚱᛖ, ᚱᛖᛞ] ')
    print(f'char4, sample_text is chunked into length 4 strings and each scored: [ᚠᚩᚱᚪ, ᚩᚱᚪᛚ, ᚱᚪᛚᛚ, ᚪᛚᛚᛁ, ᛚᛚᛁᛋ, ᛚᛁᛋᛋ, ᛁᛋᛋᚪ, ᛋᛋᚪᚳ, ᛋᚪᚳᚱ, ᚪᚳᚱᛖ, ᚳᚱᛖᛞ] ')

    print(f'*** Type 2 methods ***')
    print(f'These the runes, including Word Length Information (which is good for checking decrypted text from the Liber Primus')
    print(f'Instead of a string of runes these methods also include the length of the word, and the index of that rune in the word:')
    print("sample_input = [[ᚠ, 0, 3], [ᚩ, 1, 3], [ᚱ, 2, 3]], [[ᚪ, 0, 3], [ᛚ, 1,3], [ᛚ, 2, 3]], [[ᛁ, 0, 2], [ᛋ, 1, 2]], [[ᛋ, 0, 6], [ᚪ, 1,6], [ᚳ, 2, 6], [ᚱ, 3, 6], [ᛖ, 4, 6], [ᛞ, 5, 6]]")
    print(f'There are 4 methods of this type rb2, rb3 and gng2, gng3')
    print(f'rb2 and gng2, sample_input chunked into parts of length 2: [[[ᚠ, 0, 3], [ᚩ, 1, 3]], [[ᚩ, 1, 3], [ᚱ, 2, 3]], [[ᚱ, 2, 3], [ᚪ, 0, 3]], [[ᚪ, 0, 3], [ᛚ, 1, 3]], [[ᛚ, 1, 3], [ᛚ, 2, 3]], [[ᛚ, 2, 3], [ᛁ, 0, 2]], [[ᛁ, 0, 2], [ᛋ, 1, 2]], [[ᛋ, 1, 2], [ᛋ, 0, 6]], [[ᛋ, 0, 6], [ᚪ, 1, 6]], [[ᚪ,1, 6], [ᚳ, 2, 6]], [[ᚳ, 2, 6], [ᚱ, 3, 6]], [[ᚱ, 3, 6], [ᛖ, 4, 6]], [[ᛖ, 4, 6], [ᛞ, 5, 6]]]')
    print(f'rb3 and gng3, sample_input chunked into parts of length 3: [[[ᚠ, 0, 3], [ᚩ, 1, 3], [ᚱ, 2, 3]], [[ᚩ, 1, 3], [ᚱ, 2, 3], [ᚪ, 0, 3]], [[ᚱ, 2, 3], [ᚪ, 0, 3], [ᛚ, 1, 3]], [[ᚪ,   0, 3], [ᛚ, 1, 3], [ᛚ, 2, 3]], [[ᛚ, 1, 3], [ᛚ, 2, 3], [ᛁ,    0, 2]], [[ᛚ, 2, 3], [ᛁ, 0, 2], [ᛋ, 1, 2]], [[ᛁ, 0,2], [ᛋ, 1, 2], [ᛋ, 0, 6]], [[ᛋ, 1, 2], [ᛋ, 0, 6], [ᚪ, 1,   6]], [[ᛋ, 0, 6], [ᚪ, 1, 6], [ᚳ, 2, 6]], [[ᚪ, 1, 6], [ᚳ,    2, 6], [ᚱ, 3, 6]], [[ᚳ, 2, 6], [ᚱ, 3, 6], [ᛖ, 4, 6]], [[ᚱ, 3, 6], [ᛖ, 4, 6], [ᛞ, 5, 6]]]')
    print()
    print(f'log probability data is returned as pair of numbers,  [(positive)log probability, counts]')
    print(f'These are the log probability of those runes, and total counts from the corpus data')
    print(f'The \'score\' is a normalized weighting estimation that can be calculated for the sum of multiple log probabilities.')
    print(f'The weighting is in the range 0 to 1, 0 being low confidence of runeglish, 1 being high confidence')
    #
    text = "ᚠᚩᚱ ᚪᛚᛚ ᛁᛋ ᛋᚪᚳᚱᛖᛞ"
    score_input = []
    for word in text.split():
        [score_input.append([x,i,len(word)]) for i, x in enumerate(word) ]
    print('\n***** Example 1, real text *****\n')
    print(f'raw text = {text} ')
    print(f'scoring function input = {score_input} ')
    result = scoreWithWordLengthInfo(score_input)
    for k,v in result['log_prob'].items():
        print(f'Real text example: log prob data [log probability, counts] for test: {k} = {v}')

    for k,v in result['score'].items():
        print(f'Real text example: is it runeglish scores for test: {k} = {v}')
    import random
    ''' random rune comparison '''
    runes = "ᚠᚢᚦᚩᚱᚳᚷᚹᚻᚾᛁᛂᛇᛈᛉᛋᛏᛒᛖᛗᛚᛝᛟᛞᚪᚫᚣᛡᛠ"
    for item in score_input:
        item[0] = random.choice(runes)
    print('\n***** Example 2, real text *****\n')
    print('Compare same word lengths, but with random runes assigned')
    print(f'scoring functon input = {score_input} ')
    print(f'input = {score_input} ')
    result = scoreWithWordLengthInfo(score_input)
    for k,v in result['log_prob'].items():
        print(f'Random text example: log prob data [log probability, counts] for test: {k} = {v}')
    for k,v in result['score'].items():
        print(f'Random text example: is it runeglish scores for test: {k} = {v}')

    print(f'\n\n****** do_benchmark ********\n')
    do_benchmark()

    print(f'\n\n****** FIN ********\n')











