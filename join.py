# script that attemps to join (full) leaderboard in regular intervals

import logging
import time

import requests
from bs4 import BeautifulSoup

from util import get_cookie

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
leaderboard_invite = "PUT INVITE HERE"

JOIN_URL = "https://adventofcode.com/2020/leaderboard/private/join"

JOIN_FAIL = "That private leaderboard is full"
RETRY_FREQ_IN_SECONDS = 60


def join(leaderboard, cookie):
    data = {"join_key": leaderboard}
    r = requests.post(JOIN_URL, data=data, cookies=cookie)

    soup = BeautifulSoup(r.text, 'html.parser')

    response = soup.find_all("main")[0].get_text()
    print(response)
    return not (JOIN_FAIL in response)


if __name__ == "__main__":
    while not join(leaderboard_invite, get_cookie()):
        logging.warning(f"failed to join. retrying in {RETRY_FREQ_IN_SECONDS}")
        time.sleep(RETRY_FREQ_IN_SECONDS)
