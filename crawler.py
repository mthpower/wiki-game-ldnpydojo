import requests
from bs4 import BeautifulSoup
import functools
import networkx as nx
from networkx.exception import NetworkXError

PAGES_SCRAPED = 0

URL_TEMPlATE = 'https://en.wikipedia.org/wiki/{}'


@functools.lru_cache(maxsize=None)
def scrape_page(page):
    print(page)
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
    articles = scrape_page(start_page_name)
    global PAGES_SCRAPED
    PAGES_SCRAPED += 1
    print(PAGES_SCRAPED)

    for article in articles:
        G.add_edge(start_page_name, article)

    while True:
        try:
            shortest_path = nx.shortest_path(
                G, source=start_page_name, target=end_page_name
            )
            break
        except NetworkXError:
            print('No path found, continuing...')
            print(depth)
            depth += 1

        for article_boundary in nx.node_boundary(G, [start_page_name]):

            new_articles = scrape_page(article_boundary)
            for new_article in new_articles:
                G.add_edge(article_boundary, new_article)

        print('============= Next iteration')

    length = len(shortest_path) - 1
    print(
        'The shortest path is {}, and the distance is {}'.format(
            str(shortest_path), length
        )
    )
    return length


if __name__ == '__main__':
    wiki_distance('Bank_of_America', 'Jesus')
