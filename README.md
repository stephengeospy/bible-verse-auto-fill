# bible-verse-auto-fill

## 1. Auto-Fill Bible Verses using Crossway ESV API : populate_bible_verses_api.py

Populate the BOOK, CHAPTER, VERSE, REFERENCE fields in the excel sheet and let the code auto-fill the VERSE_TEXT field using [Crossway ESV API](https://api.esv.org/v3/passage/text/)

**Libraries Used:**  
- pandas
- requests
- configparser

## 2. Auto-Fill Bible Verses by Web Scrapping : populate_bible_verses.py

Populate the BOOK, CHAPTER, VERSE, REFERENCE fields in the excel sheet and let the code auto-fill the VERSE_TEXT field for any Bible versions by web-scraping [BibleGateway](https://www.biblegateway.com)

**Libraries Used:**  
- xlrd
- xlwt
- BeautifulSoup
- requests

## 3. Update Sermon Notes with VerseText & BibleGateway URL Link : sermon_notes_verse_fetch.py

Read Sermon Notes and replace all Verse References with the actual Verse Text and add [Biblegateway](https://www.biblegateway.com/) URL for ease of reference

**Libraries Used:**  
- re
- os
- requests
- configparser
