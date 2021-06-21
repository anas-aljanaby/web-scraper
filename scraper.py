import os
import string

import requests
from bs4 import BeautifulSoup


def make_title(text):
    """Take title, return title without punctuation and replace spaces with underscore."""
    d = str.maketrans(dict.fromkeys(string.punctuation, None))
    text = text.translate(d)
    text = text.replace(' ', '_')
    return text + '.txt'


n_pages = input()  # number of pages to search starting at page 1 until page n_pages
required_type = input()  # type of articles to get the content of. leave articles of other types
for i in range(1, int(n_pages) + 1):
    n_pages = i
    os.mkdir(f'Page_{n_pages}')  # articles that belong in page 1 will be stored in Page_1 directory

    link = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={n_pages}'
    response = requests.get(link)
    soup = BeautifulSoup(response.content, 'html.parser')

    anchors = soup.find_all('a', attrs={'data-track-action': 'view article'})  # article links have this attribute
    for a in anchors:
        link = 'https://www.nature.com' + a.get('href')
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        try:
            current_type = soup.find('meta', {'name': 'dc.type'}).get('content')
        except AttributeError:
            continue
        if current_type == required_type:
            title = soup.find('meta', {'property': 'og:title'}).get('content')
            formatted_title = make_title(title)
            div = soup.find('div', {'class': ['c-article-body u-clearfix', 'article-item__body']}).text
            div = str(div).strip().encode('utf-8')
            file_path = os.path.join(os.getcwd(), f'Page_{n_pages}', formatted_title)
            with open(file_path, 'wb') as file:
                file.write(div)
