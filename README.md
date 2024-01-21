# Liber-Primus-Rune-Decrypting
General methods, worked examples and test scripts for solving the Liber Primus  

# I: Key Generator Functions Of Two Variables

Using given cipher-text and possible cribs of the text we can generate keys (for a given encryption method).
If we can spot an extendable pattern in one of those keys we may have found the solution. 

## Overview

Benchmarked and extendable methods to find 'all' keys for functions of two variables. For example:

( plaintext + key ) % 29 = cipher text

( plaintext XOR key ) % 29 = cipher text 

For a given text file of english cribs and a corresponding cipher-text find 'all' keys for a given encryption function of two variables f(plaintext,key).
Example functions for arithmetic and xor are given, the design pattern mean sits easy to add further functions with little effort.
'All' keys means considering: all possible interrupters, gematria rotations and defined plaintext rune transpositions.
To generate crib-lists 
'[Liber-Primus-Crib-Assist](https://github.com/mortlach/Liber-Primus-Crib-Assist)'
 can be used (for example).

## Example Scripts 

### test_functions_of_2_variables.py
For each method in 'cryption_methods_of_2_variables.py' randomly encrypt text and then test solve methods to find exact key (or fail). Also solve 2 56/jpg and 'A Koan: During' pages from the Liber Primus

### keys_for_cribs.py
Example loop generating keys for given list of input cribs. Keys are saved to file for later processing.

### keys_for_cribs_with_selection.py
Example loop generating keys for given list of input cribs. 
Keys are then passed through a sequence checker to look for the first few primes, etc. 
Keys are also scored using to flag potential Runeglish phrases.

## Other Files

### gematria.py
Basic gematria manipulations and stuff. add to it as needed

### runeglish_tests.py
Methods called during text ranking. See '[Is It Runeglish](https://github.com/mortlach/Is-It-Runeglish).'

### key_generator.py
Class that handles looping over all possible variations of the main method (gematria rotations, transposition, interrupters, etc. )
More transpositions can be added as needed.
To best follow procedure see test_solve function

### cryption_methods_of_2_variables.py
General method for encryption/decryption of 'any' function of two variables.
Includes methods like xor where 1 to 1 mapping of inputs and outputs is not certain.
Can be extended with arbitrary methods, simply follow design pattern of examples.
 










