#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Original script (kept up to date): https://github.com/robincamille/bot-tutorial/blob/master/mashup_madlib.py 

# Housekeeping: do not edit
import json, io, tweepy, time, urllib
from random import randint
"""
from credentials import *
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)
"""

import openpyxl
import csv
import random
import itertools

def randomName(namelist, biglist=[]):
    # generates a random value from namelist
    findaname = True
    fraught1 = [["Armenia"], ["Azerbaijan"], ["Iveta Mukuchyan", "Srbuk", "Kamil Show"], ["Chingiz Mustafayev", "Dihaj"]]
    fraught2 = [["Russia"], ["Ukraine"], ["Sergey Lazarev", "Dima Bilan", "Polina Gagarina", "Julia Samoylova", "Philipp Kirkorov"], ["Vidbir", "Verka Serduchka", "Ruslana", "Jamala", "Oleksandr Skichko", "Volodymyr Ostapchuk", "Timur Miroshnychenko", "Kazka", "Maruv"]]
    while findaname:
        randnum = randint(0, len(namelist) - 1)
        namefound = namelist[randnum]
        if (safetycheck(namefound, fraught1, biglist) and safetycheck(namefound, fraught2, biglist)):
            findaname = False
    return namefound

def pickFive(namelist, biglist=[]):
    # generates a list of five random values from namelist
    # biglist needed to make sure no controversial combinations are found
    five = []
    while (len(five) != 5):
        randName = randomName(namelist, biglist)
        if randName not in five: # screens out duplicates
            five.append(randName)
    return five

def safetycheck(value, fraughtlist, biglist):
    # makes sure no entities from country1 are mentioned with country2, and no entities from country2 are mentioned with country1
    longlist = list(itertools.chain(*fraughtlist))
    country1 = fraughtlist[0][0]
    country2 = fraughtlist[1][0]
    entities1 = fraughtlist[2] # entities from country1
    entities2 = fraughtlist[3] # entities from country2
    if value in biglist: # value no good if already in list
        return False
    elif value not in longlist: # value okay if not in fraught list
        return True
    elif (value == country1 and country2 not in biglist): # if country1 is chosen and country2 hasn't
        return (not (any(elem in biglist for elem in entities2))) # value okay if no entity from country2 is in big list
    elif (value == country2 and country1 not in biglist): # if country2 is chosen and country1 hasn't
        return (not (any(elem in biglist for elem in entities1))) # value okay if no entity from country1 is in big list
    elif value in entities1: # if value is an entity from country1
        return (not ((any(elem in biglist for elem in entities2)) or (country2 in biglist))) # value okay if entities from country2 and country2 itself are not in big list
    elif value in entities2: # if value is an entity from country2
        return (not ((any(elem in biglist for elem in entities1)) or (country1 in biglist))) # value okay if entityies from country1 and country1 itself are not in big list
    else:
        return False

# Create Python-readable lists of items in JSON files
celebs = json.load(open('celebs.json', mode='r'))['celebs'] # assorted non-Eurovision celebrities
escartists = json.load(open('esc.json', mode='r'))['artists'] # assorted Eurovision artists
escpersonalities = json.load(open('people.json', mode='r'))['people'] # assorted Eurovision-related/-adjacent personalities
artists = celebs + escartists + escpersonalities
active = json.load(open('ebu.json', mode='r'))['active'] # EBU member nations that competed in Eurovision in 2019
inactive = json.load(open('ebu.json', mode='r'))['inactive'] # EBU member nations that have competed in Eurovision but not in 2019
debut = json.load(open('ebu.json', mode='r'))['debut'] # EBU member nations that have yet to compete in Eurovision
notebu = json.load(open('ebu.json', mode='r'))['non-ebu'] # a selection of non-EBU nations
nfs = json.load(open('nfs.json', mode='r'))['nationalfinals'] # Eurovision national finals
exclamations = json.load(open('exclamations.json', mode='r'))['exclamations'] # exclamations
g1 = json.load(open('categorized-subset.json', mode='r'))['Avant-garde']
g2 = json.load(open('categorized-subset.json', mode='r'))['Caribbean and Caribbean-influenced']
g3 = json.load(open('categorized-subset.json', mode='r'))['Blues']
g4 = json.load(open('categorized-subset.json', mode='r'))['Country']
g5 = json.load(open('categorized-subset.json', mode='r'))['Electronic']
g6 = json.load(open('categorized-subset.json', mode='r'))['Folk']
g7 = json.load(open('categorized-subset.json', mode='r'))['Hip hop']
g8 = json.load(open('categorized-subset.json', mode='r'))['Jazz']
g9 = json.load(open('categorized-subset.json', mode='r'))['Pop']
g10 = json.load(open('categorized-subset.json', mode='r'))['R&B and soul']
g11 = json.load(open('categorized-subset.json', mode='r'))['Rock']
genres = g1+g2+g3+g4+g5+g6+g7+g8+g9+g10+g11 # Source: https://github.com/voltraco/genres

def randomRumor():
    # generates a madlibs-style tweet by randomly selecting values

    # Save everything that has been selected to prevent controversial tweets
    thebiglist = []

    # Pick five countries
    countries = pickFive(active, thebiglist)
    country = countries[0]
    country2 = countries[1]
    country3 = countries[2]
    country4 = countries[3]
    country5 = countries[4]
    thebiglist = thebiglist + countries

    # Pick a returning country
    returning = randomName(inactive)

    # Pick a debut country
    newcountry = randomName(debut)

    # Pick a non-ebu country
    onetime = randomName(notebu)

    # Pick five artists
    fiveartists = pickFive(artists, thebiglist)
    artist1 = fiveartists[0]
    artist2 = fiveartists[1]
    artist3 = fiveartists[2]
    artist4 = fiveartists[3]
    artist5 = fiveartists[4]
    thebiglist = thebiglist + fiveartists

    # Pick a non-ESC celeb
    celeb = randomName(celebs)
    
    # Pick an ESC celeb
    esc = randomName(escartists, thebiglist)
    thebiglist.append(esc)
    
    # Pick an ESC-related/-adjacent person
    person = randomName(escpersonalities, thebiglist)
    thebiglist.append(person)
    
    # Pick an exclamation
    exc = randomName(exclamations)

    # Pick a national final
    nf = randomName(nfs, thebiglist)
    thebiglist.append(nf)

    # Pick a genre
    genre = randomName(genres).lower()
    
    brk = '\n'
    tweet_templates = [f"{exc} {artist1} is rumored to represent {country} in Rotterdam 2020! #botgeneratedrumor",
        f"Rumor has it: {artist1} has been selected for {nf}! {exc}",
        f"Could we really be seeing {artist1} as the interval act in Rotterdam next year? #yesthisisfakenews",
        f"{exc} Billionaire seeks to book {celeb} as the Rotterdam 2020 interval act!",
        f"You didn't hear it from me but {artist1} may have a cameo in the Eurovision movie!",
        f"Don't tell anyone: {artist1} has reportedly been internally selected for {country}! {exc}",
        f"We looked into our crystal ball: {country} will win Eurovision 2020! #botscanseeintothefuture",
        f"It's a bold prediction, but we think {artist1} will win Eurovision in Rotterdam. #botgivesdouzepoints",
        f"{exc} We have a vision of {artist1} performing onstage in Rotterdam representing {country}!",
        f"Our Eurovision 2020 wishlist: {artist1}, {artist2}, {artist3}, and {artist4}. #abotcanbutdream",
        f"The collaboration we didn't know we needed: {artist1} and {esc}!",
        f"It's a crazy concept but it just might work: {artist1} and {artist2} representing {country} at Eurovision!",
        f"Those leaks are at it again: We found out {artist1}, {artist2}, {esc}, and {person} are ALL competing at {nf}!",
        f"Who would win {nf}: {artist1} or {esc}? #justbotquestions",
        f"{country} approached {artist1} to represent them at Eurovision in 2020, but they refused! {exc}",
        f"Rotterdam planning a MASSIVE interval act with {artist1}, {artist2}, {artist3}, and {esc} all singing each other's songs!",
        f"If {artist1} competed for {country} in Tel Aviv, do you think they would have won?",
        f"{exc} {country} turns down {artist1}! Is their Eurovision 2020 dream now dead?",
        f"{celeb} SLAMS Netflix for creating a Eurovision movie! {exc} #canabotmakethemovieinstead",
        f"{exc} {nf} line-up leaked! {artist1} and {artist2} are competing, while {artist3} and {artist4} are collaborating!",
        f"Eurovision 2020 won't be complete if {artist1} or {artist2} don't perform!",
        f"It's a common framework of {artist1}, {artist2}, {artist3}, and {artist4} for {country} in Rotterdam!",
        f"Your hosts for Eurovision 2020 in Rotterdam: {artist1}, {esc}, and {person}!",
        f"{exc} {esc} surprisingly storms the Billboard charts in the USA with their latest single!",
        f"{nf} will reportedly feature {artist1} and {artist2}, but shockingly not {esc}!",
        f"{artist1} submitted a song for {country}, but they reportedly want {esc} to represent them instead! {exc}",
        f"Shocking interview with {artist1} and {esc} reveals their secret plans to compete together for {country} in Rotterdam!",
        f"If {artist1} or {esc} aren't competing in {nf} this year, then this year's Eurovision season is RUINED.",
        f"{artist1}, {artist2}, {esc}, or {person}: Who will be representing {country} in the Netherlands?",
        f"{country} reportedly already planning their next three artists: {artist1} in 2020, {artist2} in 2021, and {artist3} in 2022!",
        f"{exc} {country} accused of bribing bloggers to give nothing but praise for their 2020 entry, {artist1}! #botcausescontroversy",
        f"{artist1}, {artist2}, {artist3}, and {esc} rumored to participate in Celebrity Big Brother in {country}!",
        f"If {artist1} competes for {country}, they'll definitely get their best result ever!",
        f"Instead of a mentalist, we'll be seeing {artist1} and {artist2} in the green room in Rotterdam.",
        f"{esc}'s tell-all YouTube video about their Eurovision experience has gone viral! {exc}",
        f"We hear {country} might withdraw from Eurovision 2020, unless {artist1} agrees to be their entry!",
        f"In a surprising move, {nf} has been cancelled, and instead {artist1} has been internally selected!",
        f"{exc} {onetime} has been invited for a one-time participation at Eurovision 2020, and {artist1} will be their entry!",
        f"Did {esc} really copy {artist1}, or are Eurovision fans on Twitter imagining things again?",
        f"{country} has some crazy ideas for their staging! {artist1} floats on a pole, while {esc} sings inside a glass box full of water!",
        f"No, it's definitely not true that {artist1} and {artist2} have a feud, in fact they're performing a duet together at {nf}!",
        f"Twitter fans SHOCKED as {artist1} admits they've never ever watched Eurovision! #ifabotsaysititmustbetrue",
        f"{esc} covered {celeb}'s song on Instagram, and {celeb} invited {esc} to sing with them onstage at their next concert in {country}!",
        f"The Twitter fandom has spoken: We don't want {celeb} as the interval act, we want {esc}!",
        f"{exc} Drama in the Twitter fandom! Who has had the better career: {artist1} or {esc}?",
        f"Spotted at a songwriting camp for {nf}: {artist1}, {artist2}, {artist3}, and {artist4}!",
        f"It's not looking great for {country}. They will be represented by {artist1} performing a song rejected from {nf}!",
        f"Fans on Twitter rejoice as {esc} goes on a following spree! #followthebot",
        f"This #twitterbot can see the future: {esc} goes straight to Number One at #ESC250 this year!",
        f"{exc} {country} tops the odds after revealing their entry: A song performed by {artist1}, written by {artist2}!",
        f"{exc} Rumors of a feud between {artist1} and {artist2} after it was revealed that {artist1} was chosen to represent {country}! #thisbotlovesfakedrama",
        f"Twitter is mad: You can't make a Eurovision movie without {esc} or {person}!",
        f"Hey Twitter! Would you rather have {artist1} represent {country}, or have {country} withdraw? #botstirsthepot",
        f"Here we go again... Fans are claiming {artist1}'s entry for {country} is a clone of Fuego...",
        f"Eurovision fans from {country} are RIOTING after {artist1} won their national selection over {artist2}.",
        f"What's going on? {esc} has unfollowed {artist2} on Instagram! What does this mean?",
        f"Everyone knows {esc} deserves to win #ESCBestOfTheDecade.",
        f"We look into our crystal ball to predict the Top Five at {nf} this year:{brk}1. {artist1}{brk}2. {artist2}{brk}3. {esc}{brk}4. {artist3}{brk}5. {artist4}",
        f"{exc} {artist1} will represent {country} with a song that {artist2} turned down! How will {artist2} react?",
        f"{exc} {artist1} turns down a chance to compete at Eurovision for {country}, instead focusing on their blossoming K-Pop career.",
        f"The hot new Tik-Tok challenge: Dancing to a nightcore version of {esc}'s Eurovision entry!",
        f"Current Eurovision winner odds:{brk}1. {esc}{brk}2. {artist1}{brk}3. {artist2}{brk}4. {artist3}{brk}5. Whatever {country} ends up sending",
        f"Happy Eurovision New Year! {artist1} is releasing a new single soon. Is that a possible Eurovision entry?",
        f"{artist1} and {artist2} seen spending time together. Could they be working on a song for {nf}?",
        f"{exc} We just saw {artist1} heading to {country}... a future Eurovision entry in the works, perhaps?",
        f"The official {nf} Instagram account has randomly started following {artist1}! Coincidence? Or is {artist1} competing in {nf}?",
        f"A {artist1} like this, can break a {country} like this. #abotlikethis #canshitpostlikethis",
        f"{artist1} and {esc}, it's getting exciting. #botandshitposting #itsgettingexciting",
        f"The most unexpected Eurovision friendship yet: {artist1} and {esc}!",
        f"Thanks to a leak, we heard {artist1}'s entry for {country} this year. They really turned down {esc} for THIS?!",
        f"In a controversial interview, {artist1} was asked about the artist from {country}. They refused to respond, instead saying, ‘Let's talk about {artist2}!‘ #dontgettoopolitical",
        f"{artist1} thinks {artist2} should represent {country} at Eurovision.",
        f"Would {esc} ever return to Eurovision? {artist1} certainly thinks they should!",
        f"{nf} reveals some of their jurors: {artist1}, {artist2}, and {esc}!",
        f"SCANDAL! {artist1} says they won't compete in Eurovision this year if {artist2} is chosen to represent {country}!",
        f"Reports indicate that it's now between {artist1} and {artist2} to be {country}'s representative to Eurovision this year.",
        f"{exc} {country} reports that they've approached {artist1} to be their representative this year, and they're considering it. Will they say 'yes' to Eurovision?",
        f"A look at Instagram Stories shows that {artist1} and {artist2} are working on a song together. Will they be competing at {nf} this year?",
        f"{artist1} just started following {esc} on Instagram. Is a collab in the works?",
        f"Fans are FUMING after {nf} adds {artist1} to their line-up at the last minute! {esc} threatens to drop out in protest!",
        f"After being turned down by {country}, {artist1} announces their intentions to audition for {nf}.",
        f"Following backlash from their internal selection of {artist1}, {country} withdraws their nomination and announces a national final instead. {artist2} and {artist3} are already confirmed to participate.",
        f"SHOCKER at {nf}! {artist1} won, but they turned down Eurovision! Runner-up {artist2} will be going to Rotterdam instead.",
        f"A broken {artist1} is all that's left. #smalltownbot #inabigarcade",
        f"{exc} {esc} is headed to Eurovision for {country} with a song written by {artist1}, {artist2}, {artist3}, and {artist4}.",
        f"In a risky move, {country} will be represented by a {genre} song by {artist1}.",
        f"{nf} just got more exciting! We'll be hearing some {genre} by {artist1}!",
        f"Did someone say {genre}? {artist1} will be bringing some of that to {nf}!",
        f"Was anyone expecting {country} to send {genre} this year?",
        f"{artist1} and {esc} are collaborating on a {genre} song!",
        f"{exc} {esc}'s new {genre} song is kinda messy...",
        f"We all knew {artist1} was representing {country}, we didn't know they were bring a {genre} song!",
        f"{country} is taking a risk this year with a {genre} song. Will it pay off?",
        f"{country} has decided to do an internal selection. {artist1} will be singing a {genre} song co-written by {artist2} and {artist3}.",
        f"There's always an unexpected entry in {nf}. This year it's a {genre} song by {artist1}!",
        f"Current Eurovision winner odds:{brk}1. {country}{brk}2. {country2}{brk}3. {country3}{brk}4. {country4}{brk}5. {country5}",
        f"{artist1} was turned down by {country}, so they're planning to approach {country2} and {country3}.",
        f"This bot predicts the following three countries will win in the next ten years: {country}, {country2}, and {country3}.",
        f"It looks like {newcountry} is finally going to debut in 2020! We hear their entry is gonna be a {genre} song by {artist1}!",
        f"EBU announced {onetime} will make a special one-time appearance at Eurovision in Rotterdam. Twitter fans are split: Is this a good thing or a bad thing? Does it matter that {artist1} is representing them?",
        f"Following the shocking announcement that {country} is withdrawing for Rotterdam 2020, the EBU announces that {onetime} will participate this year! They've even already announced their artist: {artist1}!",
        f"EBU is happy to announce the return of {returning} to Eurovision! We wish {artist1} the best of luck in Rotterdam!",
        f"{exc} We're hearing whispers that not only is {returning} coming back to Eurovision, but they've already chosen a {genre} song by {artist1} to represent them!",
        f"{exc} {country} announces that they'll WITHDRAW if {onetime} gets to participate at Eurovision!",
        f"Sigh.... it's the same story every year... 'Douze points from {country} go to.... {country2}!'",
        f"It looks like {artist1} is shopping around their {genre} song written by {artist2}.... {country} wasn't interested, but maybe {country2} is?",
        f"Twitter fans are FURIOUS at the EBU after they confirm {newcountry} isn't debuting at Eurovision 2020. Would they change their minds if {artist1} represents {newcountry}?",
        f"Twitter fans heartbroken after {returning} confirms they're not coming back to Eurovision in 2020. Maybe {artist1} can still change their minds?",
        f"Twitter fans scandalized by rumors that {artist1} is paying their way into Eurovision 2020. But if that secures {country}'s participation, is that really a bad thing?"]

    # Pick a tweet format
    twtnum = randint(0, len(tweet_templates) - 1)
    my_tweet = tweet_templates[twtnum]

    return(my_tweet)