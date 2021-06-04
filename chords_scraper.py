from bs4 import BeautifulSoup
import requests
import re


headers = {
        'User-agent':
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.19582"
    }

def get_cifraclub_page(name, artist):
    #google recognizes urls with spaces
    url = "https://www.google.com/search?q=" + name + " " + artist + " cifra"
    html = requests.get(url, headers=headers).text
    #the first result will always be the corresponding cifraclub page
    soup = BeautifulSoup(html, 'lxml')
    
    #set up in a way that I could easily take into account more results
    #summary = []

    #could be problematic if google changes the "div class" naming conventions
    for container in soup.findAll('div', class_='tF2Cxc'):
        link = container.find('a')['href']
        return link
        #summary.append({
        #    'Link': link,
        #})

    #first = True
    #for link in summary:
    #    if first:
    #        return link
def get_chord_text(url):
    html = requests.get(url, headers=headers).text
    #the first result will always be the corresponding cifraclub page
    soup = BeautifulSoup(html, 'lxml')
    
    #set up in a way that I could easily take into account more results
    #summary = []

    #could be problematic if google changes the "div class" naming conventions
    for container in soup.findAll('div', class_='cifra_cnt g-fix cifra-mono'):
        text = container.find('pre').text
        return text

def scrape_chords(name, artist):
    #find the cifraclub url that describes the song's chords
    url = get_cifraclub_page(name, artist)
    print(get_chord_text(url))
    #print the page (in the future the chords will be extracted and matched to those extracted by Chordino)
    #pdfkit.from_url(url, 'out.pdf')
    return url
    

    

