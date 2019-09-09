from bs4 import BeautifulSoup
import wikipedia

def whichsemi(year, n):
    # determines which show is currently being scraped
    if year >= 2008: # two semifinals and a grand final since 2008
        if n == 1:
            return "Semifinal 1"
        elif n == 2:
            return "Semifinal 2"
        else:
            return "Grand Final"
    elif year >= 2004: # one semifinal and a grand final 2004-2007
        if n == 1:
            return "Semifinal"
        else:
            return "Grand Final"
    else: # just one show
        return "Grand Final"


def stripcell(cell):
    try:
        unwanted = cell.find('sup')
        unwanted.extract()
    except AttributeError:
        pass
    try:
        unwanted = cell.find('span', { "class" : "sortkey" })
        unwanted.extract()
    except AttributeError:
        pass
    return cell.get_text().strip()

basename = "Eurovision Song Contest "

f = open('output.csv', 'w')

header = "YEAR;SHOW;RUNNING ORDER;COUNTRY;ARTIST;SONG TITLE;LANGUAGE;PLACE;POINTS\n"
f.write(header)

for year in range(1956,2020):
    articlename = basename + str(year)
    wiki = wikipedia.page(articlename)
    soup = BeautifulSoup(wiki.html(), "lxml")
 
    draw = ""
    country = ""
    artist = ""
    song = ""
    language = ""
    place = ""
    points = ""

    tables = soup.findAll("table", { "class" : ["wikitable sortable", "sortable wikitable"] })
 
    usabletable = 0

    for table in tables:
        currow = 1
        validentry = False
        for row in table.findAll("tr"):
            cells = row.findAll("td")
            #For each "tr", assign each "td" to a variable.
            if year == 1956 and len(cells) == 6: # 1956 does not have a points column, hence a length of 6 is needed
                if currow == 1:
                    usabletable += 1
                draw = stripcell(cells[0])
                country = stripcell(cells[1])
                artist = stripcell(cells[2])
                song = stripcell(cells[3])
                language = stripcell(cells[4])
                place = stripcell(cells[5])
                if place == "N/A": # some rankings are listed as N/A
                    place = ""
                points = "" # no points column
                validentry = True
            elif len(cells) == 7:
                if currow == 1:
                    usabletable += 1
                draw = stripcell(cells[0])
                country = stripcell(cells[1])
                artist = stripcell(cells[2])
                song = stripcell(cells[3])
                language = stripcell(cells[4])
                place = stripcell(cells[5])
                points = stripcell(cells[6])
                validentry = True
            if validentry and ((usabletable < 4 and year > 2007) or (usabletable < 3 and year > 2003) or (usabletable == 1)):
                write_to_file = str(year) + ";" + whichsemi(year, usabletable) + ";" + draw + ";" + country + ";" + artist + ";" + song + ";" + language + ";" + place + ";" + points + "\n"
                print(write_to_file)
                currow += 1
                f.write(write_to_file)
                validentry = False

f.close()