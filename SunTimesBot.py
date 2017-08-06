# -*- coding: utf-8 -*-
"""
    File Name: main.py
    Author: Ari Madian
    Created: August 4, 2017 4:42 PM
    Python Version: 3.6

    main.py - Main code for SunTimesBot
    Repo: github.com/akmadian/SunTimesBot
"""
import configparser
import arrow
import tweepy
import datetime
import textwrap
from astral import Astral

times_dict = {'Dawn': None,
              'Sunrise': None,
              'Sunset': None,
              'Dusk': None}


def refresh_times():
    """Refreshes the sun times in the times_dict"""
    global times_dict

    date = arrow.utcnow().to('US/Pacific').format('YYYY-MM-DD')
    city = Astral()['Seattle']
    sun = city.sun(date=datetime.date(int(date[:4]),
                                      int(date[5:-3]),
                                      int(date[8:])),
                   local=True)
    for key in times_dict:
        times_dict[key] = sun[key.lower()]

    for key, value in times_dict.items():
        string = key + ' - ' + arrow.get(value).format('h:m A')
        times_dict[key] = string


def api_connect():
    """Connects to the twitter api, makes the tweet, and sends it."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    print('Config parsed')
    auth = tweepy.OAuthHandler(config['twitterbotauth']['C_KEY'],
                               config['twitterbotauth']['C_SECRET'])
    auth.set_access_token(config['twitterbotauth']['A_TOKEN'],
                          config['twitterbotauth']['A_TOKEN_SECRET'])
    api = tweepy.API(auth)
    print('Good Auth')
    refresh_times()
    date = arrow.utcnow().to('US/Pacific').format('MMM D, YYYY')
    tweet = textwrap.dedent('For today, ' + date + '\n\n' +
                            times_dict['Dawn'] + '\n' +
                            times_dict['Sunrise'] + '\n' +
                            times_dict['Sunset'] + '\n' +
                            times_dict['Dusk'])
    api.update_status(tweet)
    quit()


api_connect()
