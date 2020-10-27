# Contributing to Growcabulary

## Ideas
* User profile with tracking his WPM and learning progress
* Show the image for _each_ definition
* Maybe a slideshow of images for each definition
* A slideshow which contains alternative images for definitions
* Enlarge the image on hover
* Make every _view_ unique by adding support in the URL. This allows sharing the link and seeing what was shared, common items sharing the same link isn't good.
* Allow to hide image, notes, synonyms, etc.
* Click on word and get taken to the meaning if it exists
* Slightly darker shade for the navbar
* 2 folders for images, one containing small 250 x 250 images and one containing large 750 x 750 images. The large ones are for enlarged images which get shown on hover. The preprocessing helps to load the images faster as some images are super large and take time to load otherwise.
* Typing test which contains jus the _words_ of GRE
* Show the user the number of _corrections_ that were made and the number of _errors_ that were made
* Keyboard shortcut buttons to do things such as play audio (US/UK), next word, previous word, etc.
* For spell-check component, press enter upon completion of word to make sure the user can't correct it if the _actual_ word is longer or to make sure the user thinks he's right when he's wrong cause he assumed the _actual_ word was shorter.

## Required
* navbar should be fixed upon scrolling
* Login page with user authentication
* Show is caps lock key is on
* Chart.js, show the value of WPM on hover
* Upon completion of set, add an alert box stating "Set Completed. Would you like to move to the next set? Yes/No buttons"
* Control menu with options to select what to type (key, pos, def, synonyms, antonyms, and notes)
* Test section where you _hear_ the audio of a word and you need to type it. It will help you learn the spelling.

## Bugs

#### Word List
* Loads slightly lowered in terms of the page

#### Word Item
* In the reading view, clicking the audio of some card below scrolls to the first word. This can be fixed by making the index a query parameter in the url and only scroll when you see a query parameter.
* Go to elusive the word dragonflies, the characters "f" and "l" are different span tags with different stylings but show up together as one :/. Type f correctly but l incorrectly, both will be green but the classes are applied correct and incorrect which is right! Could be the width of the background color? Idk.
* The "current" letter underline doesn't work for all, such as commas
* The "current" letter underline is too small to be noticed when the width of the character is small such as ")"
* When going to learning mode, the card is at the top of the screen (you can't see the text "Learning Mode"), and on incorrect letter, the card scrolls up.
* When going F11, if you type incorrect letter, the page shifts right.
* When a single line breaks over to the next line, hitting enter instead of space doesn't show an error when there is an error. You can verify this by inspecting the span tags and the " "(space) will have the incorrect class applied, but it doesn't show on the card. The user sees the Accuracy has gone down when according to him he did not make an error.
* Upon completion of word, pressing backspace also takes you to the next word (or set) when only hitting the enter key should
* There are non-ascii characters that need to be converted when typing. Check empathetic it has an em dash and a quotation mark, these need to be mapped to hyphen and single quote.

## Better Images

#### Common Words 1
* construe
* delineate (add Note drawing for criminal investigation)
* parsimonious

#### Common Words 2
* betray: same as perfidy
* predilection
* platitude: same as conspicuous
* vociferous: better definition without vehement?

#### Common Words 3
* abstain: same image as eschew
* ascetic: noun definition uses the word, then it's not a definition now is it?
* delineate: add Note drawing for investigation reasons
* denote
* derivative: people won't know it's Mona lisa, so either find a similar better image or add a note
* fallacious: image where "if A then B, A, therefore B" but the assumption of "A." itself was wrong
* treacherous: 2nd word, add image for dangerous bridge which may fall
* vilify: same image as recrimination

#### Common Words 4
* implausible
* injunction: feels like justice rather than an order
* intransigent: add Note about the KKK
* pragmatic: feels like emotions instead of theory (knowledge vs experience should be the goal), also same image as cerebral
* provincial

#### Common Words 5
* austere
* dilettante: doesn't make much sense and also same image as unpropitious
* garrulous: seems angry rather than talkative
* insolent: image already used for frivolous
* intrepid: change definition to synonym and add an actual definition
* lionize: paparazzi or something similar would be nice, and when the photo was taken is irrelevant
* ostracize: bad image

#### Common Words 6
* antipathy: same image already used
* banality: same image as hackneyed
* harried: doesn't show people wanting things from you
* indecorous: add note that using phone is bad manners?
* maladroit: feels like hasty but it means not clever or skillful?
* pejorative: feels like you shouldn't speak
* specious: the image is bad, and the second definition can be used for the image. Also, isn't it a synonym for spurious?

#### Common Words 7
* panache: same image as illustrious
* placate: some image as mollify

#### Basic Words 1
* indignant: add Note about George Floyd
* inundate
* retiring: doesn't show the person likes being alone
* tawdry: looks poor quality and cheap but isn't showy, you wanna have both
* telling
* unnerve: doesn't show the height isn't really much, maybe one where there's a person for reference like in a pool

#### Basic Words 2
* cogent: same image as posit
* errant
* extenuating
* heyday: check the spelling
* immaterial
* junta: audio pronunciation doesn't match the phonetics
* misanthrope
* moment: maybe an image which changes life of that person and that "moment" was captured
* replete: add a note that it's a supermarket?
* sanctimonious

#### Basic Words 3
* appreciable
* boon: add Note why microwave is a boon and how it changed
* consummate: an image of sculpting?
* moot: image which says "What came first the chicken or the egg?"
* muted
* obdurate

#### Basic Words 4
* conducive
* credence
* detrimental: an actual image instead of portrait would be nice
* empathetic: has an em dash and the single quote "\'" isn't proper
* glib: change it, it sucks.
* grovel: same image used for obsequious
* impeccable
* irresolute: doesn't show hesitant, shows confused

#### Basic Words 5
* abysmal
* balk
* colossal: I _think_ the same image is used
* complacent: I _think_ the same image is used and it looks like he's rich
* placid
* savvy
* unseemly: image used for derivative
* begrudge: doesn't make sense
* cavalier
* emulate
* glean
* implicate
* inarticulate: even worse handwriting would be nice
* incumbent
* intermittent
* rakish: same image as raffish
* redress: same image as venality
* veneer: you can't really notice the thin layer?

#### Basic Words 6
* antedate: (US) audio pronunciation sounds like atedate
* carp: (US) (UK) the audio pronunciation and phonetics is of carp when the word is carping
* cavalier: doesn't make much sense
* redress: same as venal and the image looks more like corruption when it should be giving money to help and fix mistake

#### Basic Words 7
* badger: could use this image for tout which means selling something
* contemptuous
* deliberate
* embroiled: (US) (UK) the audio pronunciation is of embroil and _not_ embroil-ed
* resignation: same image as concede
* serendipity: add note about penicillin

#### Advanced Words 1
* abrogate
* churlish: feels like you are attacking someone
* conciliate: feels like you are forming peace
* despot: (US) the audio pronunciation sounds like despit
* diatribe: the image of churlish can be used here
* exegesis
* saturnine
* vicissitude: we don't want text, we want visual images

#### Advanced Words 2
* benighted: feels confused and frustrated instead of without morals or knowledge
* diminutive: an image with a name such as Sam-uel where uel is greyed out
* dissemble: the idea is nice, maybe an image where you can see the gun more clearly
* dissipate: throwing money in all directions would cover both the definitions
* excoriate: (US) the audio sounds like exgoriate
* hedge: should restrict not dodge
* jaundice: doesn't really make sense
* peremptory
* Pollyanna & Pollyannaish: handle the capital letter in spell-check
* Pollyannaish: (US) the audio pronunciation is lower than usual volume
* sententious
* tendentious: white lives matter isn't exactly controversial

#### Advanced Words 3
* flummox: the image is flipped
* litany: same image used for exorbitant
* mordant
* pecuniary: more elaborate definition would be nice
* probity: textual image to visual image, (US) the audio pronunciation sounds like probidy
* recapitulation: textual image to visual image

#### Advanced Words 4
* intimation
* machinate: (US) the audio pronunciation has the phonetic of UK, (UK) the audio pronunciation has the phonetic of US
* surreptitious: add Note
* unflappable: there's no crisis shown in the picture
* untenable: shows the opposite meaning

#### Advanced Words 5
* appurtenant: visually very similar (only color difference) image with obliging
* bristle
* browbeat: same image as banish
* effervescent: not much excitement
* epigram: a clever _and_ amusing idea would be nice
* pith: (US) the audio sounds like piff

#### Advanced Words 6
* assiduously: the image could be better used
* fecund: use the image assiduously of
* impugn
* malingerer: man in suit would be nice
* pontificate: doesn't make sense
* self-effacing: how would you include the hyphen in spell-check?

#### Advanced Words 7
* apotheosis: same as aesthetic
* estimable: same image is used for deferential
* extrapolate
* misattribute: (US) the audio sound is _slightly_ lower than usual
* modicum: an even smaller diamond ring?
* veritable

#### Extra Words
* notorious