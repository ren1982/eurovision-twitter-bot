# Housekeeping: do not edit
import json, io, tweepy, time, urllib3
from random import randint

import csv
import random

def rankinator(num):
    # converts a number in string form to its ranking form
	number = int(num)
	last = num[-1]
	if number >= 11 and number <= 13:
		return (num+"th")
	elif last == '1':
		return (num+"st")
	elif last == '2':
		return (num+"nd")
	elif last == '3':
		return (num+"rd")
	else:
		return (num+"th")

def whichshow(year, show):
    # generates text depending on which year and show an entry is referring to
    if year >= 2008:
    	if show == "Grand Final":
    		return " in the Grand Final"
    	else:
    		return (" in " + show)
    elif year >= 2004:
    	return (" in the " + show)
    else:
        return ""

def pointorpoints(pts):
    # determines whether the singular or plural form of "point" is needed
	if int(pts) == 1:
		return "1 point"
	else:
		return (pts + " points")

def entryinfotweet():
    # generates a tweet about a Eurovision entry and its performance in a particular show

    # Picks a random row in the CSV
    with open('output.csv', mode='r') as csv_file:
    	lines = sum(1 for line in csv_file)
    	line_number = random.randrange(1,lines)

    # Gets information from the row, composes a tweet
    with open('output.csv', mode='r') as csv_file:
    	reader = csv.reader(csv_file, delimiter=';')
    	chosen_row = next(row for row_number, row in enumerate(reader) if row_number == line_number)
    	artist = chosen_row[4]
    	song = chosen_row[5]
    	year = chosen_row[0]
    	country = chosen_row[3]
    	show = whichshow(int(year), chosen_row[1])
    	if year == "1956":
    		if chosen_row[7] == "1":
    			my_tweet = (f'"{song}" by {artist} representing {country} placed 1st in {year}. #Eurovision')
    		else:
    			aps = "\'s"
    			my_tweet = (f'"{song}" by {artist} was one of {country}{aps} two entries in {year}. #Eurovision')
    	else:
    		rank = rankinator(chosen_row[7])
    		points = pointorpoints(chosen_row[8])
    		my_tweet = (f'"{song}" by {artist} representing {country} placed {rank}{show} with {points} in {year}. #Eurovision')
    return my_tweet