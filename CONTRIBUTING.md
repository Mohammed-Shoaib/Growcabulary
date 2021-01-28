# Contributing

:+1::tada: First off, thanks for taking the time to contribute! :tada::+1:

### Table Of Contents

* [Contribute to the Website](#contribute-to-the-website)
  * [Website Suggestions](#website-suggestions)
  * [Future Ideas](#future-ideas)
  * [Must-add Features](#must-add-features)

* [Provide or Handle Bugs!](#provide-or-handle-bugs)
  * [Word List Component](#word-list-component)
  * [Word Item Component](#word-item-component)


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