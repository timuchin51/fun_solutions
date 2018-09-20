from bs4 import BeautifulSoup
from urllib.request import urlopen
import re

nouns_url = 'http://www.ruslo.net/index.php/contents/19-vse-suschestvitel-nye-russkogo-yazyka.xhtml'
adjective_url = 'http://www.ruslo.net/index.php/contents/16-imena-prilagatel-nye.xhtml'
verbs_url = 'http://www.ruslo.net/index.php/contents/18-vse-glagoly-russkogo-yazyka.xhtml'
adverb_url = 'http://www.ruslo.net/index.php/contents/7-vse-narechiya-russkogo-yazyka.xhtml'
orthographic_dictionary_url = 'http://www.ruslo.net/index.php/contents/1-orfograficheskiij-slovar-.xhtml'
list_url = [nouns_url, adjective_url, verbs_url, adverb_url, orthographic_dictionary_url]


def get_words(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    words = soup.findAll('p', {'class': 'xu'})
    return ((word.previous_sibling.text, word.text) for word in words)


def get_links(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, features='html.parser')
    result = soup.findAll('p', {'class': 'xu'})
    domain_part_url = re.findall(r'(http://[\w\.]+)', url)
    for objects in result[1:]:
        for word in objects.findAll('a'):
            yield (word.text, domain_part_url[0]+word.attrs['href'])


def get_text(url):
    word_list = []
    for (word, word_url) in get_links(url):
        if word not in word_list:
            word_list.append(word)
            html = urlopen(word_url)
            soup = BeautifulSoup(html, features='html.parser')
            try:
                soup_object = soup.find('span', {'class': 'trns-1'})
                text = re.findall(r'(?<=: ).+', soup_object.text)
            except AttributeError:
                text = ['No words in dictionary']
            yield (word, text)


def write_file(urls):
    with open('file.txt', 'w') as file:
        for url in urls[:-1]:
            for line in get_words(url):
                file.write(line[0]+'\n'+line[1]+'\n')
            file.write('-----------------------------------'+'\n')
        for line in get_text(urls[-1]):
            file.write('{}: {}.\n\n'.format(line[0], *line[1]))

if __name__ == '__main__':
    write_file(list_url)
