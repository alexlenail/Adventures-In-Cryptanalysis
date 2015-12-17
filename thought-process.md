

# How I solved it (Log)

some words are all caps, make sure to replace them with lowercase when parsing (this will take a long time)

build a bigram model.

also get the vocabulary

somehow, ideally, we'd like to match partially figured out words against the vocabulary, e.g. aXXle -> apple? -> X => p

...

might be best to do frequency analysis over letters, not words.

I've built three structures: bigrams, words and letters. I want to optimize over all three.

... (cook dinner for self and gf)

The point of all of this is to narrow the search spane. There are 26! possibilities, and we don't want to search them all.

There are common words and common letters. We need to search some space, but we should keep it as small as possible.

At each point in this computation, we're deciding which eventualities to investigate, and which not to. Since we're not investigating every 26! possibilities, we may not get the correct answer -- it's impossible to guarantee the correct answer without examining every possibility. So we have to hope that our language model will give us sufficient direction that we'll only abandon worlds which are heuristically-speaking, extremely unlikely.

The current corpus claims that every letter of the alphabet is used somehwere as a single-letter word:
Counter({'a': 95610, 'i': 79585, 's': 29990, 'd': 15201, 't': 9660, 'o': 5534, 'm': 2231, 'e': 777, 'n': 431, 'v': 399, 'c': 384, 'p': 369, 'l': 352, 'f': 298, 'b': 226, 'r': 182, 'x': 159, 'y': 117, 'u': 108, 'h': 80, 'g': 75, 'j': 74, 'w': 63, 'k': 46, 'q': 29, 'z': 20})
Strange, huh?

The parameter KONSTANT is a branching factor, which we'll use to determine the breadth of the search space. At 26 we explore every possibility.
Intuitively, 5 seems like a good place to start.

Well this isn't good:

```
oia yreu ew ena udhc oiegyio tl uehoi ceha oidn cenaf

ienalof tl oia wthlo midboah tn oia xeep ew utlsec

t navah menltsahas d stwwahanma ew ebtnten tn bertotml  tn hartyten  tn bitrelebif  dl mdgla weh utoishdutny whec d whtans

tw ua dha gnmhtotmdr ua lidrr drudfl wtns uido ua udno  ua lidrr reep weh  dns wtns  menwthcdotenl  dns ua lidrr reep dudf whec  dns neo laa  uidoavah ctyio xa sdnyahegl oe egh bao oiaehtal

lmtanma cdf xa salmhtxas dl oia dho ew lfloacdotm evah ltcbrtwtmdoten - oia dho ew stlmahntny uido ua cdf utoi dsvdnodya ecto

oia gna dctnas rtwa tl neo uehoi rtvtny

oiaha tl enrf ena yees  pneurasya  dns ena avtr  tynehdnma

t mdnneo oadmi dnfxesf dnfoitny  t mdn enrf cdpa oiac oitnp

uensah tl oia xaytnntny ew utlsec

oia enrf ohga utlsec tl tn pneutny feg pneu neoitny
```

python is nice because it's intuitive, except for sorting. I don't understand why the default is low to high rather than high to low. I was keeping the worst models I had, not the best models.

```
the glow of one warm thought is worth more than money

honesty is the first chapter in the book of wisdom

i never considered a difference of opinion in politics  in religion  in philosophy  as cause for withdrawing from a friend

if we are uncritical we shall always find what we want  we shall look for  and find  confirmations  and we shall look away from  and not see  whatever might be dangerous to our pet theories

science may be described as the art of systematic over simplification - the art of discerning what we may with advantage omit

the une amined life is not worth living

there is only one good  knowledge  and one evil  ignorance

i cannot teach anybody anything  i can only make them think

wonder is the beginning of wisdom

the only true wisdom is in knowing you know nothing
```

that's more like it.

My approach turns out to be a lot like a genetic algorithm.

Unfortunately it's rather feeble, because if all the current ciphers in the pool have a single letter wrong each, the remainder of the computation is useless, it has no possibility of reconverging. This is the output for KONSTANT = 3

```
the glom of one marw thought is morth wore than woney.

honesty is the first chapter in the book of misdow.

i never considered a difference of opinion in politics, in religion, in philosophy, as cause for mithdraming frow a friend.

if me are uncritical me shall almays find mhat me mant: me shall look for, and find, confirwations, and me shall look amay frow, and not see, mhatever wight be dangerous to our pet theories.

science way be described as the art of systewatic over-siwplification — the art of discerning mhat me way mith advantage owit.

the uneEawined life is not morth living.

there is only one good, knomledge, and one evil, ignorance.

i cannot teach anybody anything. i can only wake thew think.

monder is the beginning of misdow.

the only true misdow is in knoming you knom nothing.
```



