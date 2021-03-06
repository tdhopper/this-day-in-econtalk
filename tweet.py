#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime as dt
import twitter as tw
import os
import json


def tweets(month, day):
    with open('econtalk.json', 'r') as f:
        d = json.load(f)
    for year, content in d.get(str(month), {}).get(str(day), {}).items():
        yield "🎧 " + str(" ".join(content) + " ({})".format(year))


def tweet(event, context):
    cred = {
        "consumer_key": os.environ['CONSUMER_KEY'].strip(),
        "consumer_secret": os.environ['CONSUMER_SECRET'].strip(),
        "token": os.environ['TOKEN'].strip(),
        "token_secret": os.environ['TOKEN_SECRET'].strip(),
    }
    auth = tw.OAuth(**cred)
    t = tw.Twitter(auth=auth)

    now = dt.datetime.now()
    for update in tweets(now.month, now.day):
        t.statuses.update(status=update)
