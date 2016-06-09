import requests
from bs4 import BeautifulSoup
import functools
import networkx as nx
from networkx.exception import NetworkXNoPath

PAGES_SCRAPED = 0

URL_TEMPlATE = 'https://en.wikipedia.org/wiki/{}'


@functools.lru_cache(maxsize=None)
def scrape_page(page):
    response = requests.get(URL_TEMPlATE.format(page))
    soup = BeautifulSoup(response.content, 'html.parser')

    def filtered_hrefs(href):
        if href is None:
            return False
        if ':' in href:
            return False
        if href.startswith('/wiki'):
            return True

    links = soup.find_all('a')
    hrefs = [link.get('href') for link in links]
    articles = filter(filtered_hrefs, hrefs)

    for article in articles:
        yield article.lstrip('/wiki/')


# def random_page():
#     return 'some random wiki page'


def wiki_distance(start_page_name, end_page_name):
    depth = 0
    G = nx.Graph()
    while True:
        articles = scrape_page(start_page_name)

        for article in articles:
            G.add_edge(start_page_name, article)

        try:
            shortest_path = nx.shortest_path(
                G, source=start_page_name, target=end_page_name
            )
        except NetworkXNoPath:
            print('No path found, continuing...')
            print(depth)
            depth += 1
            continue

        length = len(shortest_path) - 1
        print('The shortest path is {}, and the distance is {}'.format(str(shortest_path), length))
        return length


if __name__ == '__main__':
    wiki_distance('Jesus', 'Christianity')
