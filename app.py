import requests_cache

import re
from bs4 import BeautifulSoup

from flask import Flask, render_template

app = Flask(__name__)

main = 'https://www.realitytvrevisited.com/2016/02/hells-kitchen-contestants.html'

#year = 2016
#month = 11
#base_url = f'https://www.realitytvrevisited.com/{year}/{month}/hells-kitchen-season-{{}}-contestants.html'

season_urls = []

session = requests_cache.CachedSession('hell')


def get_season_urls():
    page = session.get(main)
    print("Cache", page.from_cache, "Expired", page.is_expired)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    for link in soup.find_all('a'):
        if link.has_attr('href'):
            href = link['href']
            if href and not href.startswith('#') and 'hells-kitchen-season-' in href:
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
    #url = base_url.format(season)
    url = get_season_url(season)
    page = session.get(url)
    print("Cache", page.from_cache, "Expired", page.is_expired)
    return BeautifulSoup(page.content, 'html.parser')


@app.route("/")
def index():
    numbers = get_season_numbers()
    return render_template('index.html', seasons=numbers)


@app.route('/<int:season>/<int:episode>')
def show_post(season, episode):
    soup = get_soup(season)
    result = soup.find_all(string=re.compile("eliminated (.)*episode {}[^0-9]".format(episode)))

    context = {
        'season': season,
        'episode': episode,
        'content': []
    }

    for person in result:
        context['content'].append(str(person.parent))

    return render_template('episode.html', **context)


get_season_urls()

if __name__ == '__main__':
    app.run()