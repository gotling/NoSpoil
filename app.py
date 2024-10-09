import requests_cache

import re
from bs4 import BeautifulSoup

from flask import Flask, render_template

app = Flask(__name__)

main = 'https://www.realitytvrevisited.com/2016/02/hells-kitchen-contestants.html'

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
    return render_template('index.html')


@app.route('/<int:season>/<int:episode>')
def show_post(season, episode):
    soup = get_soup(season)
    result = soup.find_all(string=re.compile("eliminated in Hell's Kitchen season {} episode {}[^0-9]".format(season, episode)))

    context = {
        'season': season,
        'episode': episode,
        'nav': nav_buttons(season, episode),
        'content': []
    }

    for person in result:
        context['content'].append(str(person.parent))

    return render_template('episode.html', **context)


def nav_buttons(season, episode):

   


if __name__ == '__main__':
    app.run()