# Decipher

### Background

This problem was presented to me as a code challenge for a company I was applying to. This submission got me to the next round, where I promptly disqualified myself by having trouble efficiently computing Conway's Game Of Life.

The problem statement follows. My solution can be found in [christopher.py](https://github.com/zfrenchee/adventures-in-cryptanalysis/blob/master/christopher.py). My thought process and results can be found in [thought-process.md](https://github.com/zfrenchee/adventures-in-cryptanalysis/blob/master/thought-process.md)

=====

### Goal

The goal of this problem is to write a program that decrypts a set of short messages (roughly the length of Tweets) that have been encrypted with a simple substitution cipher.

### Input Data

Along with this documentation file, you have been given two data files.

"encoded-en.txt" is a set of short messages (e.g. Tweets) in English, where each has been encrypted using a simple substitution cipher. Such a cipher works by replacing all occurrences of a character with a different (randomly selected, but consistent) character. The substitution is not case sensitive.

For example:

Original message: `Hello world.`
Encrypted message: `Lkccz mzfca.`

Cipher:

encrypted | decrypted
------- | -------
d | a
e | k
h | l
l | c
o | z
r | f
w | m

For this problem white space and punctuation are not substituted.

"corpus-en.txt" is a corpus of English text consisting of the contents of a number of books.


### Your Program

Your program should be runnable from the command line and output at least two things:

(1) The decryption cipher (i.e. the inverse mapping of encoded character back to original), in a single text file with the format:

encrypted | decrypted
------- | -------
... | ...

for each character. No header row, thus there should be 26 rows (one for each English letter).

(2) The original Tweets decrypted based on this decryption cipher. This should be in a single text file, following the same formatting as the encrypted messages provided.

