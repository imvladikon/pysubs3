
### pysub3

A python3 library for parsing and manipulating subtitle files.
Fork of [pysub2](https://github.com/tkarabela/pysubs2) with small changes:

* optional language detection for each line of subtitles
* changed behaviour of using "\N" character in subtitles as a line break (just usual "\n" is used now) because sometimes it was causing problems with RTL languages
* small changes (like changes in timestamps)
* removing html tags from subtitles using bs4 instead of regex (which was causing problems with some subtitles)


### Installation

```bash
pip install git+https://github.com/imvladikon/pysubs3
```

### Usage

The same as in pysubs2, but with some changes for language detection:

```python
import pysubs3

file_sub = "subtitles.srt"
subs = pysubs3.load(file_sub, encoding="utf-8", detect_language=True)

text = open(file_sub).readlines()
for sub in subs:
    print(sub.text, sub.language)
```