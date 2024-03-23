import wikipedia
import cv2
from newspaper import Article


def serch_wiki(pesquisa, lingua = "pt"):
    wikipedia.set_lang(lingua)
    temas = wikipedia.search(pesquisa)
    return temas

def extract_text_wiki(tema):
    return wikipedia.WikipediaPage(title=tema).content


def extract_allimg(tema):
    return wikipedia.WikipediaPage(title=tema).images

def serch_web(url):
    article = Article(url)
    article.download()
    article.html
    article.parse()
    return article.text

