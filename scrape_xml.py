import xml.etree.ElementTree as ET
import requests
import re
import unidecode
import json
import logging
from collections import Mapping
from itertools import islice
from collections import defaultdict
from dateutil.parser import parse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

FULL_REBUILD = False
MAX_ITEMS = None
DATA = "econtalk.json"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}
feeds = [
    "http://files.libertyfund.org/econtalk/EconTalk.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2014.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2013.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2012.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2011.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2010.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2009.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2008.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2007.xml",
    "http://files.libertyfund.org/econtalk/EconTalk2006.xml",
]


def slugify(text):
    text = unidecode.unidecode(text).lower()
    text = text.replace("'", "")
    return re.sub(r"[\W_]+", "-", text)


def get_podcasts(feeds):
    for feed in feeds:
        page = requests.get(feed)
        tree = ET.fromstring(page.content)
        items = tree.getchildren()[0].findall("item")
        yield from items


def dict_merge(dct, merge_dct):
    for k, v in merge_dct.items():
        if k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], Mapping):
            dict_merge(dct[k], merge_dct[k])
        else:
            dct[k] = merge_dct[k]


if __name__ == "__main__":
    with open(DATA, "r") as f:
        old_data = json.load(f)
    data = defaultdict(lambda: defaultdict(dict))

    for item in islice(get_podcasts(feeds), MAX_ITEMS):
        title = item.find("title").text
        date = parse(item.find("pubDate").text)
        url = f"http://www.econtalk.org/{slugify(title)}/"
        logger.info(f"{title} {url} {date}")

        if requests.get(url, headers=headers).status_code != 200:
            logger.error(f"ERROR: {title} {url} {date}")
            continue
        if FULL_REBUILD is not True and (
            old_data.get(str(date.month), {}).get(str(date.day), {}).get(str(date.year))
            is not None
        ):
            dict_merge(data, old_data)
            break
        else:
            data[str(date.month)][str(date.day)][str(date.year)] = (title, url)

    with open(DATA, "w") as f:
        json.dump(data, f)
