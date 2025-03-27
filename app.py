import requests_cache

import math
import re
from bs4 import BeautifulSoup

from flask import Flask, render_template

app = Flask(__name__)

main = 'https://www.realitytvrevisited.com/2016/02/hells-kitchen-contestants.html'

season_urls = []

session = requests_cache.CachedSession('data/hell')


def get_season_urls():
    page = session.get(main)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            href = link['href']
            if href and not href.startswith('#') and 'hells-kitchen-' in href and '-season' in href:
                season_urls.append(href)


def get_season_url(season):
    return list(filter(lambda x: f'-{season}-' in x, season_urls))[0]


def get_season_numbers():
    numbers = []

    for url in season_urls:
        m = re.search('season-(.*)-contestants', url)
        numbers.append(int(m.group(1)))

    return numbers


def get_soup(season):
    url = get_season_url(season)
    page = session.get(url)
    return BeautifulSoup(page.content, 'html.parser')


@app.route("/")
def index():
    numbers = get_season_numbers()
    return render_template('index.html', seasons=numbers, column_count=math.ceil(len(numbers)/2))


@app.route('/<int:season>/<int:episode>')
def show_post(season, episode):
    soup = get_soup(season)
    result = soup.find_all(string=re.compile("eliminated (.)*episode {}[^0-9]".format(episode)))

    context = {
        'season': season,
        'episode': episode,
        'season_url': get_season_url(season),
        'content': [],
        'contestants': []
    }

    for person in result:
        context['content'].append(str(person.parent))
        context['contestants'].append(str(person.parent.find('b').text))


    return render_template('episode.html', **context)


@app.route('/final/<int:season>')
def show_final(season):
    soup = get_soup(season)
    winner = soup.find(string=re.compile("[Ss]eason {} winner".format(season)))
    runner_up = soup.find(string=re.compile("runner up".format(season)))

    context = {
        'season': season,
        'season_url': get_season_url(season),
        'winner': str(winner.parent),
        'runner_up': str(runner_up.parent),
        'contestants': [str(winner.parent.find('b').text), str(runner_up.parent.find('b').text)]
    }

    return render_template('final.html', **context)


get_season_urls()

if __name__ == '__main__':
    app.run()