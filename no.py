import requests_cache

import re
from bs4 import BeautifulSoup

from flask import Flask

app = Flask(__name__)

year = 2016
month = 11
base_url = f'https://www.realitytvrevisited.com/{year}/{month}/hells-kitchen-season-{{}}-contestants.html'

session = requests_cache.CachedSession('hell')

def get_soup(season):
    url = base_url.format(season)
    page = session.get(url)
    return BeautifulSoup(page.content, 'html.parser')

@app.route("/")
def index():
    return """
    <html><body>
    <h1>Hells Kitchen</h1>
    <h2>No spoilers</h2>
    <a href='/6/1'>Season 6</a><br>
    <a href='/7/1'>Season 7</a><br>
    <a href='/8/1'>Season 8</a><br>
    </body></html>"""

@app.route('/<int:season>/<int:episode>')
def show_post(season, episode):
    soup = get_soup(season)
    result = soup.find_all(string=re.compile("eliminated in Hell's Kitchen season {} episode {}[^0-9]".format(season, episode)))

    content = ""

    for person in result:
        content += str(person.parent)

    return "<html><body><h1>Eliminated season {} episode {}</h1>{}<br><div style='width: 600px'>{}</div></body></html>".format(season, episode, nav_buttons(season, episode), content)


def nav_buttons(season, episode):
    return '<a href=/{}/{}>< Previous</a> <a href=/{}/{}>Next ></a>'.format(season, episode-1, season, episode+1)


if __name__ == '__main__':
    app.run()