# Contributing

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

### Table Of Contents

* [Contribute to the Website](#contribute-to-the-website)
  * [Website Suggestions](#website-suggestions)
  * [Future Ideas](#future-ideas)
  * [Must-add Features](#must-add-features)

* [Provide or Handle Bugs! :beetle:](#provide-or-handle-bugs)
  * [Word List Component](#word-list-component)
  * [Word Item Component](#word-item-component)
  * [`fetch.py`](#fetch.py)

* [Bestow or Improve Images :framed_picture:](#bestow-or-improve-images)


## Contribute to the Website

### Website Suggestions

* Slightly darker shade for the navbar.
* Add better router navigation: Make every _view_ unique by adding support in the URL. This allows sharing the link and seeing what was shared, common items sharing the same link isn't good.

### Future Ideas

* User profile with statistics such as the WPM and learning progress.
* Show the image for _each_ definition.
* Add support for multiple images by using slideshow.
* Enlarge the image on hover.
* Allow to hide attributes: These may include the image, notes, synonyms, etc.
* Click on a word _anywhere_ on the website and get taken to the meaning if it exists.
* 2 folders for images, one containing small 250 x 250 images and one containing large 750 x 750 images. The large ones are for enlarged images which get shown on hover. The preprocessing helps to load the images faster as some images are super large and take time to load otherwise.
* Typing test which contains just the _words_ alone to test for spelling and reiterate the definition in your head.
* Show the user the number of _corrections_ that were made and the number of _errors_ that were made.
* Keyboard shortcut buttons to do things such as play audio (US/UK), next word, previous word, etc.
* For self-evaluation of spelling or the spell-check component: press enter upon completion of word to make sure the user can't correct it if the _actual_ word is longer, this allows for false positives.
* If the user types the spelling incorrectly, give him an option to practice by typing the word 5 times.
* Show the words the user has typed incorrectly, maybe with a click of a button.
* Summarize the results at the end of completing a set.
	- Show the average WPM
	- Show the total time taken
	- Show the incorrect words
	- Show the average accuracy
* Allow the user to **flag** certain words for review later.
* Allow the user to add a word just by typing it. Perhaps you can fetch all the information like the definition, synonyms, antonyms, example, etc. from _sources_.
* Deal with words which are duplicate of each other in terms of parts of speech. For example, Pollyanna and Pollyannaish.

### Must-add Features

* Navbar should be fixed when scrolling the page.
* Login page with user authentication.
* Show if the `Caps Lock` key is _on/off_.
* `Chart.js`, show the value of WPM on hover.
* Upon completion of a set, add an alert box stating "Set Completed. Would you like to move to the next set?" with Yes/No _button_.
* _Control menu_ with options to select what to type or show in the UI (key, pos, def, synonyms, antonyms, and notes).
* Test section where the user _hears_ the audio of a word and needs to type it. Helps wire the spelling of different words in the head.
* Search functionality doesn't work for words containing accents (both in scripts and on website, for example, _précis_).
* Remove extra words that have the same word root but in a different part of speech (_discern_, _discerning_, _discernment_).
* Ability to search using alternatives.


## Provide or Handle Bugs! :beetle:

#### Word List Component

* Loads slightly lower in terms of the page.

#### Word Item Component

* In the reading view, clicking the audio of some card below scrolls to the first word. This can be fixed by making the index a query parameter in the url and only scroll when you see a query parameter.
* Go to **elusive**, then the word **dragonflies** in the _Notes_, the characters `f` and `l` are different span tags with different stylings but show up together as one :confused:. Type `f` correctly but `l` incorrectly, both will be green but the classes are applied correct and incorrect which is right! Could be the width of the background color? I am not sure.
* The _current_ letter underline doesn't work for all, such as commas.
* The _current_ letter underline is too small to be noticed when the width of the character is small, for example, the character `)`
* When switching to learning mode, the card is at the top of the screen (you can't see the text _Learning Mode_), and on incorrect letter, the card scrolls up for some reason.
* When full screen (can be done by pressing F11 on Windows), if you type an incorrect letter, the page shifts right.
* When a single line breaks over to the next line, hitting enter instead of space doesn't show an error when there is an error. You can verify this by inspecting the span tags and the ` `(space) will have the incorrect class applied, but it doesn't show on the card. The user sees the **Accuracy** has gone _down_ when according to him he did not make an error.
* Upon completion of word, pressing backspace also takes you to the next word (or set) when only hitting the enter key should work.	
* There are non-ascii characters that need to be converted to the corresponding ascii characters when typing. Check the word _empathetic_, it has an em dash and a quotation mark, these need to be mapped to hyphen and single quote.
* When in `keyOnly` mode, many words get taken as `0 WPM`, try typing `modicum` extremely fast and you will notice this behaviour.
* When in _not_ `keyOnly` mode, typing till the definition and then switching to `keyOnly` causes a bug where it doesn't do anything, it's like typing without any checks.

#### `fetch.py`

* The incorrect audio pronunciation and IPA phonetics gets downloaded for some words. For example, vacillating gets the audio and phonetics of _vacillate_. This is because on [cambridge](https://dictionary.cambridge.org/dictionary/english/vacillating) the word _vacillating_ is present at the top hence passing the key check, but the audio files and phonetics are down from _vacillate_ and those incorrectly get downloaded.


## Bestow or Improve Images :framed_picture:

#### Common Words 1

* _banal_: same image used as _hackneyed_.
* _construe_
* _parsimonious_

#### Common Words 2

* _betray_: same as _perfidy_.
* _predilection_
* _platitude_: same image as _conspicuous_.
* _vociferous_: better definition without vehement?

#### Common Words 3

* _abstain_: same image as _eschew_.
* _ascetic_: noun definition uses the word, then it's not a definition now is it?
* _delineate_: add a note stating the importance of a portrait drawing for criminal investigation.
* _denote_
* _derivative_: not all people wil realize it's Mona lisa, so either find a similar better image or add a note.
* _fallacious_: a better image would reflect the clause _if A then B, A, therefore B_ but the assumption of _A_ itself was wrong.
* _supplant_: assumes the user knows the meaning of the word _supersede_, bear in mind these are common words.
* _treacherous_: for the second word, add an image for a dangerous bridge which may collapse.
* _vilify_: same image as _recrimination_.

#### Common Words 4

* _implausible_: same image as _antipathy_.
* _injunction_: feels like justice rather than an order.
* _intransigent_: add a note about the [_KKK_](https://en.wikipedia.org/wiki/Ku_Klux_Klan).
* _pragmatic_: feels like emotions instead of theory, however, knowledge vs experience should be the goal. Also the same image as _cerebral_.
* _provincial_

#### Common Words 5

* _austere_
* _dilettante_: doesn't make much sense and also same image as _unpropitious_.
* _garrulous_: seems angry rather than talkative.
* _insolent_: same image as _frivolous_.
* _intrepid_: change definition to synonym and add an actual definition.
* _lionize_: paparazzi or something similar would be nice, and when the photo was taken is irrelevant.
* _ostracize_: the image doesn't make much sense and is of bad quality.

#### Common Words 6

* _banality_: same image as _hackneyed_.
* _harried_: the image doesn't depict people wanting things from you.
* _indecorous_: add a note that using a phone while eating is bad manners?
* _maladroit_: feels like hasty but it means not clever or skillful?
* _pejorative_: feels like you shouldn't speak when in reality it means to express contempt.
* _specious_: the image is bad, and the second definition can be used for the image. Also, isn't it a synonym for spurious?

#### Common Words 7

* _panache_: same image as _illustrious_.
* _placate_: some image as _mollify_.

#### Basic Words 1

* _indignant_: add a note about George Floyd.
* _inundate_
* _retiring_: doesn't depict the person likes being alone.
* _tawdry_: looks poor quality and cheap but isn't showy, you wanna have both.
* _telling_
* _unnerve_: doesn't show the height isn't really much, maybe one where the person is afraid of drowning in a shallow pool.

#### Basic Words 2

* _cogent_: same image as _posit_.
* _errant_
* _extenuating_: the image could be improved.
* _immaterial_
* _junta_: the audio pronunciation doesn't match the phonetics.
* _lassitude_: add word to this set.
* _misanthrope_
* _moment_: maybe an image which changes the life of a person and that _moment_ was captured.
* _replete_: add a note stating the shop in the image is a supermarket?
* _sanctimonious_: the picture depicts the meaning of protecting something sacred, but we want something along the lines of making a show of being holy.
* _unconscionable_: Magoosh has a different meaning.

#### Basic Words 3

* _appreciable_
* _boon_: add a note stating why microwave is a boon and how it changed?
* _consummate_: could also mean sculpting, consequently, an image of sculpting?
* _fledgling_: maybe switch the definition to synonyms and use an _actual_ definition?
* _flounder_: it also denotes having difficulties for a task.
* _moot_: an image which says _What came first the chicken or the egg?_
* _muted_
* _obdurate_
* _resolve_: different meaning in Magoosh.

#### Basic Words 4

* _buck_: add word to this set.
* _conducive_
* _credence_
* _detrimental_: an actual image instead of a portrait would be nice.
* _empathetic_: has an em dash and the single-quote `'` isn't a regular singe-quote.
* _facetious_: different meaning in Magoosh.
* _glib_: the image isn't memorable.
* _grovel_: same image used for _obsequious_.
* _impeccable_
* _irresolute_: the image doesn't show the notion of being hesitant, but rather, shows confused.

#### Basic Words 5

* _abysmal_
* _balk_
* _colossal_: a similar image is used for _prodigious_.
* _complacent_: the image just looks like he's rich, also different meaning in Magoosh representing being happy with failure.
* _placid_
* _savvy_
* _unseemly_: same image used for _derivative_.
* _begrudge_: the image doesn't make _too_ sense.
* _cavalier_
* _emulate_
* _glean_
* _implicate_
* _inarticulate_: even worse handwriting would depict it better.
* _incumbent_
* _intermittent_
* _rakish_: same image as _raffish_.
* _veneer_: it's hard to notice the thin layer.

#### Basic Words 6

* _antedate_: (US) audio pronunciation sounds like _atedate_.
* _carping_: (US) (UK) the audio pronunciation and phonetics is of _carp_ when the word is _carping_. Also, the image seems more as scolding but again _faultfinding_ is hard to describe.
* _cavalier_: the image doesn't make much sense.
* _redress_: same as _venal_ and the image looks more like corruption when it should be giving money to help and fix a mistake.

#### Basic Words 7

* _badger_: could use this image for _tout_ which means selling something, consequently, fetching a new image for this as well.
* _contemptuous_
* _deliberate_
* _embroiled_: (US) (UK) the audio pronunciation is of _embroil_ and not _embroil-ed_
* _resignation_: same image as _concede_.
* _serendipity_: add a note about penicillin.

#### Advanced Words 1

* _abrogate_
* _churlish_: feels like you are attacking someone.
* _conciliate_: feels like you are forming peace.
* _despot_: (US) the audio pronunciation sounds like _despit_.
* _diatribe_: the image of _churlish_ can be used here.
* _exegesis_
* _saturnine_
* _vicissitude_: we don't want text, we want visual images.

#### Advanced Words 2

* _benighted_: feels _confused and frustrated_ instead of _without morals or knowledge_.
* _diminutive_: an image with a name such as _Sam-uel_ where _uel_ is greyed out.
* _dissemble_: the idea is nice, maybe an image where you can see the gun more clearly.
* _dissipate_: throwing money in all directions would cover both the definitions.
* _excoriate_: (US) the audio sounds like _exgoriate_.
* _hedge_: the image should should depict restricting not dodging.
* _jaundice_: the image doesn't really make sense.
* _peremptory_
* _Pollyanna_: handle the capital letter in spell-check.
* _Pollyannaish_: handle the capital letter in spell-check.
* _Pollyannaish_: (US) the audio pronunciation is lower than the usual volume.
* _sententious_
* _tendentious_: white lives matter isn't exactly controversial.

#### Advanced Words 3

* _litany_: same image used for _exorbitant_.
* _mordant_
* _pecuniary_: more elaborate definition would be nice.
* _probity_: textual image to visual image, (US) the audio pronunciation sounds like _probidy_.
* _recapitulation_: convert textual image to visual image.

#### Advanced Words 4

* _intimation_
* _machinate_: the audio pronunciations are swapped, US to UK and vice-versa.
* _unflappable_: there's no crisis shown in the picture.
* _untenable_: the image shows the opposite meaning.

#### Advanced Words 5

* _appurtenant_: visually the exact same image as _obliging_, only color difference.
* _bemoan_: the picture just means sad, but the word means to express discontent or a strong regret.
* _bristle_
* _browbeat_: same image as _banish_, could definitely use a better image.
* _effervescent_: the image doesn't contain much excitement?
* _epigram_: a clever _and_ amusing idea would be nice.
* _ersatz_: (US) the audio pronunciation sounds like _ertsatz_, notice the additional _t_.
* _inanity_: an image that means the lack of _meaning_ or _ideas_.
* _pith_: (US) the audio sounds like _piff_.

#### Advanced Words 6

* _assiduously_: the image could be better used for another word, for example, _fecund_.
* _ethereal_: the image doesn't reflect the idea of extremely _light_ and _delicate_.
* _fecund_: use the image of _assiduously_.
* _impugn_: the image works **much** better for _impute_, you need something else here.
* _malingerer_: a person sleeping in a suit would work better.
* _panegyric_: there is no speech in the picture.
* _pontificate_: the image doesn't make sense.
* _self-effacing_: handle the hyphen in spell-check.

#### Advanced Words 7

* _anathema_: (US) the audio pronunciation is slower than usual.
* _apotheosis_: same as _aesthetic_.
* _estimable_: same image is used for _deferential_.
* _extrapolate_
* _graft_: same image used as _venality_.
* _infelicitous_: maybe it's used more conceptually rather than for actual events?
* _misattribute_: (US) the audio sound is _slightly_ lower than usual.
* _modicum_: an even smaller diamond ring?
* _perfunctory_: an image where the guy is annoyed but still does the work, would definitely describe it better.
* _trenchant_: the image doesn't describe it too well.
* _verisimilitude_: It's a good image, but maybe conceptually means that it is _indeed_ true and not _seeming_ to be true but false?
* _veritable_: a bad image example.

#### Personal Words 9

* _obturate_: (UK) the audio pronunciation and phonetics doesn't match up. The phonetic was taken from Google while the audio was taken from [audioenglish](https://www.audioenglish.org/audiodic/w1/87/92187_7TVNRLVG.mp3).

#### Personal Words 10

* _uproarious_: the definitions uses the word, nullifying the purpose of a definition

### PrepScholar Words 1

* _covet_: use a better image.

#### Extra Words

* _notorious_