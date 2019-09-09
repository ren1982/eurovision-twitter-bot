# Eurovision Twitter Bot (@ESC_bot_)
A collection of various programs and scripts for the creation and deployment of a Twitter bot, [@ESC_bot_](https://twitter.com/ESC_bot_).

---

## What the bot does
The bot currently tweets every twelve minutes:
* hh00: A ridiculous rumor or "news" tweet, generated Madlibs-style using randomly chosen values
* hh12: A random YouTube video from [the official Eurovision YouTube channel](https://www.youtube.com/channel/UCRpjHHu8ivVWs73uxHlWwFA)
* hh24: Another ridiculous rumor
* hh36: Information about a random Eurovision entry, including (among others) the title of the song, the artist, and the country it represented
* hh48: Another ridiculous rumor

## What the bot will eventually do
* I am currently working on adding random text to a meme image and tweeting it.
* Eventually, information about Eurovision entries will be mapped with official performance videos, allowing the bot to tweet a video alongside the song information.

## What the bot will NOT do
I am *personally* not a fan of the following actions as performed by Twitter bots, so I do not intend to do this with my bot, but I *may* implement some of the functionality just to prove that I can do it, without deploying it (at least not long-term).
* Automatically follow users who interact with the bot, follow the bot, or tweet using a particular keyword or hashtag
* Automatically retweet tweets with a particular keyword or hashtag
* Automatically reply to tweets with a particular keyword or hashtag

---

## Background information
Before the bot began operation, data had to be collected and compiled. The original idea was to use the data for a personal data science project, but for now, it will be used for this bot. Using the YouTube API, **playlist.py** collected data from the Eurovision YouTube channel and saved the information to an Excel file. **mergeworkbooks.py** was used to combine the information from two executions of **playlist.py** and will likely be used to add new videos to the spreadsheet. The spreadsheet containing the video information is **esc-youtube.xlsx**.

In order to generate information regarding each entry, a Wikipedia scraper, **wikiscrape.py**, was used. The script went through the Wikipedia articles of each individual contest year and grabbed information about the entries there. The results are saved in **output.csv** (*Note to self: Give that CSV file a better filename.*)

JSON files for the Madlibs-style tweet generator were created by me, and I plan to continue adding names to the list as necessary. The exception to this is **categorized-subset.json**, which is a JSON file of assorted music genres, which was taken from https://github.com/voltraco/genres . The JSON files used are:
* **celebs.json** - Assorted non-Eurovision celebrities (f.e.: Lady Gaga, Stromae)
* **esc.json** - Assorted Eurovision artists (f.e.: Duncan Laurence, Netta)
* **people.json** - Assorted Eurovision-related/-adjacent personalities (f.e.: Petra Mede, Riga Beaver)
* **ebu.json** - EBU member nations classified according to their last Eurovision participation, as well as a selection of non-EBU countries
* **nfs.json** Eurovision national finals
* **exclamations.json** - Exclamations (f.e.: "Wig!", "OMFG.")

All information is current as of **2019-09-09**.

---

## The bot
The Twitter bot is currently deployed via [Heroku](http://www.heroku.com/). The following files are utilized for the bot:

### escbot.py
The main script, it calls all the other files to generate tweets, then posts the generated tweet.

### rumorbot.py
Handles the creation of the ridiculous rumors. Randomly selects data from the various JSON files, then picks a random tweet format, fills in the blanks with the selected values, then returns the created tweet. The random selection of values takes into consideration some fraught situations between countries, so that potentially controversial tweets are avoided, or at least minimized. (This means that certain pairs of countries will not be selected together, and entities from one country will not be selected if either the other country or an entity from the other country has been selected.)

### youtubevid.py
Handles the creation of tweets with links to YouTube videos. Adds a #Eurovision hashtag, because why not.

### entryinfo.py
Handles the creation of tweets with information about Eurovision entries. Takes data from the CSV file and turns it into a sensible sentence, ready for tweeting, complete with a #Eurovision hashtag.