#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import datetime as dt
import twitter as tw
import os
import json


def tweets(month, day):
    with open('data.json', 'r') as f:
        d = json.loads(f)
    for year, content in d.get(str(month), {}).get(str(day), {}).items():
        yield " ".join(content) + "({})".format(year)


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
    try:
        for t in tweets(now.month, now.day):
            t.PostUpdate(status=t)
    except Exception as e:
        print(e)
