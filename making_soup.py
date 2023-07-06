import requests
from bs4 import BeautifulSoup

def openLinkAndReturnSoup(root_link):
    response = requests.get(root_link)
    soup = BeautifulSoup(response.text, "html.parser")
    return soup
