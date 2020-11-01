# Instructions



### Terms

* `data.json`: Stores the word list for a given folder.
* `originals`: Stores the raw downloaded images in it's best resolution.
* `images`: Stores the cropped square images in it's best resolution.
* `audio`: Contains the pronunciation `.mp3` files for each word in the word list.



## Python Scripts

### Prerequisites

* [opencv](https://pypi.org/project/opencv-python/)
* [unidecode](https://pypi.org/project/Unidecode/)
* [reportlab](https://pypi.org/project/reportlab/)
* [selenium](https://pypi.org/project/selenium/)
* [regex](https://pypi.org/project/regex/)
* [requests](https://pypi.org/project/requests/)

### `utils.py`

Contains the utility functions that can be used in multiple scripts. Requires the implementation of `argparse` with the `--tests` property.

### `main.py`

Contains the crux of the implementation and functionality needed.

To check if a given word is present,

```bash
$ python main.py -w [WORD]
```

To delete only the images from `originals` and `images`,

```bash
$ python main.py -r [WORD]
```

To copy the images and audio files from the source word to the destination word,

```bash
$ python main.py -src [SOURCE] -dst [DESTINATION]
```

To run tests to check if everything is in order,

```bash
$ python main.py -t
```

To save the downloaded images (in the `Downloads` directory) to the specific word list,

```bash
$ python main.py -s
```

### `fetch.py`

Contains all the web scraping code required to fetch data.

To get the wikipedia link to the commons page from a raw wikipedia link,

```bash
$ python fetch.py -w [LINK]
```

To download the IPA phonetics and audio pronunciation,

```bash
$ python fetch.py -p >> phonetics.out	# currently fetches from dictionary.cambridge.org
```

The audio files get saved in `audio` in the same directory. The file `phonetics.json` contains the scraped phonetic transcript. The file `phonetics.out` contains errors and words for which either the audio or IPA phonetic was not found.

To move the downloaded audio files to the specific word list,

```bash
$ python fetch.py -a
```

To save the IPA phonetic to the specific word list,

```bash
$ python fetch.py -s
```

### `data_to_pdf.py`

Creates a pdf of all the words with their images and IPA phonetics.

```bash
$ python data_to_pdf.py
```
