Decipher
========

Goal
----
The goal of this problem is to write a program that decrypts a set of
short messages (roughly the length of Tweets) that have been encrypted
with a simple substitution cipher.

We use this as an interview problem because most algorithmic
approaches do not just work out of the box.  The problem forces you to
evolve your thinking, and thus your code must also evolve.  One
measure of engineering craftsmanship is how quickly a person can
evolve their thinking while still maintaining high-quality, readable
code.


Input Data
----------
Along with this documentation file, you have been given two data files.

"encoded-en.txt" is a set of short messages (e.g. Tweets) in English,
where each has been encrypted using a simple substitution cipher. Such
a cipher works by replacing all occurrences of a character with a
different (randomly selected, but consistent) character. The
substitution is not case sensitive.

For example:

Original message: "Hello world."
Encrypted message: "Lkccz mzfca."

Cipher:
d -> a
e -> k
h -> l
l -> c
o -> z
r -> f
w -> m

For this problem white space and punctuation are not substituted.

"corpus-en.txt" is a corpus of English text consisting of the contents
of a number of books.


Your Program
------------
We prefer that you code this in python.  If you would like to submit
solutions in other programming languages, we will certainly read them.
Language nimbleness is an important skill.  If non-standard libraries
are required to run the solution you need to provide them (ideally
none).

Your program should be runnable from the command line and output at
least two things:

(1) The decryption cipher (i.e. the inverse mapping of encoded
character back to original), in a single text file with the format:

<encrypted> -> <decrypted>
...

for each character. No header row, thus there should be 26 rows (one
for each English letter).

e.g.
a -> z
b -> y
c -> x
...
z -> a

(2) The original Tweets decrypted based on this decryption cipher.
This should be in a single text file, following the same formatting as
the encrypted messages provided.


You should submit at the conclusion of the exercise:

- All code written

- Example output files as specified above

- Any supplementary files (e.g. tests, data)

- A brief write-up explaining your approach, how well it worked, what
  further avenues you might explore given time, along with any
  necessary instructions on how to run the code. Specify the language
  version if important to running the solution.



Important Notes
---------------

In addition to evaluating the simplicity and cleverness of your
technical approach, we also give marks for ease of use, engineering
hygiene, craftmanship & style.

Correct solutions get the reverse cipher without fail.  That is,
programs should *not* require repeated manual operation to eventually
get a valid reverse cipher.

Your program should be sufficiently generalized that it can be run on
*other* input files, or even incorporated into a larger system.  We
want to see how you organize the interface to your algorithm.

Pythonic style counts.  `pip install pylint` and aim for >8.  Use the
python standard library.  Write docstrings and consider pytest.



---------------


# How I solved it (Log)

some words are all caps, make sure to replace them with lowercase when parsing (this will take a long time)

build a bigram model.

also get the vocabulary

somehow, ideally, we'd like to match partially figured out words against the vocabulary, e.g. aXXle -> apple? -> X => p

...

might be best to do frequency analysis over letters, not words.

I've built three structures: bigrams, words and letters. I want to optimize over all three.

... (cook dinner for self and gf)

The point of all of this is to narrow the search spance. There are 26! possibilities, and we don't want to search them all.

There are common words and common letters. We need to search some space, but we should keep it as small as possible.

# At each point in this computation, we're deciding which eventualities to investigate, and
# which not to. Since we're not investigating every 26! possibilities, we may not get the
# correct answer -- it's impossible to guarantee the correct answer without examining
# every possibility. So we have to hope that our language model will give us sufficient
# direction that we'll only abandon worlds which are heuristically-speaking, extremely unlikely.

The current corpus claims that every letter of the alphabet is used somehwere as a single-letter word:
Counter({'a': 95610, 'i': 79585, 's': 29990, 'd': 15201, 't': 9660, 'o': 5534, 'm': 2231, 'e': 777, 'n': 431, 'v': 399, 'c': 384, 'p': 369, 'l': 352, 'f': 298, 'b': 226, 'r': 182, 'x': 159, 'y': 117, 'u': 108, 'h': 80, 'g': 75, 'j': 74, 'w': 63, 'k': 46, 'q': 29, 'z': 20})
Strange, huh?

The parameter KONSTANT is a branching factor, which we'll use to determine the breadth of the search space. At 26 we explore every possibility.
Intuitively, 5 seems like a good place to start.

Well this isn't good:

oia yreu ew ena udhc oiegyio tl uehoi ceha oidn cenaf   ienalof tl oia wthlo midboah tn oia xeep ew utlsec   t navah menltsahas d stwwahanma ew ebtnten tn bertotml  tn hartyten  tn bitrelebif  dl mdgla weh utoishdutny whec d whtans   tw ua dha gnmhtotmdr ua lidrr drudfl wtns uido ua udno  ua lidrr reep weh  dns wtns  menwthcdotenl  dns ua lidrr reep dudf whec  dns neo laa  uidoavah ctyio xa sdnyahegl oe egh bao oiaehtal   lmtanma cdf xa salmhtxas dl oia dho ew lfloacdotm evah ltcbrtwtmdoten     oia dho ew stlmahntny uido ua cdf utoi dsvdnodya ecto   oia gna dctnas rtwa tl neo uehoi rtvtny   oiaha tl enrf ena yees  pneurasya  dns ena avtr  tynehdnma   t mdnneo oadmi dnfxesf dnfoitny  t mdn enrf cdpa oiac oitnp   uensah tl oia xaytnntny ew utlsec   oia enrf ohga utlsec tl tn pneutny feg pneu neoitny

python is nice because it's intuitive, except for sorting. I don't understand why the default is low to high rather than high to low. I was keeping the worst models I had, not the best models.

the glow of one warm thought is worth more than money   honesty is the first chapter in the book of wisdom   i never considered a difference of opinion in politics  in religion  in philosophy  as cause for withdrawing from a friend   if we are uncritical we shall always find what we want  we shall look for  and find  confirmations  and we shall look away from  and not see  whatever might be dangerous to our pet theories   science may be described as the art of systematic over simplification     the art of discerning what we may with advantage omit   the une amined life is not worth living   there is only one good  knowledge  and one evil  ignorance   i cannot teach anybody anything  i can only make them think   wonder is the beginning of wisdom   the only true wisdom is in knowing you know nothing

that's more like it.

My approach turns out to be a lot like a genetic algorithm.

Unfortunately it's rather feeble, because if all the current ciphers in the pool have a single letter wrong each, the remainder of the computation is useless, it has no possibility of reconverging. This is the output for KONSTANT = 3

the glom of one marw thought is morth wore than woney.	honesty is the first chapter in the book of misdow.	i never considered a difference of opinion in politics, in religion, in philosophy, as cause for mithdraming frow a friend.	if me are uncritical me shall almays find mhat me mant: me shall look for, and find, confirwations, and me shall look amay frow, and not see, mhatever wight be dangerous to our pet theories.	science way be described as the art of systewatic over-siwplification — the art of discerning mhat me way mith advantage owit.	the uneEawined life is not morth living.	there is only one good, knomledge, and one evil, ignorance.	i cannot teach anybody anything. i can only wake thew think.	monder is the beginning of misdow.	the only true misdow is in knoming you knom nothing.



