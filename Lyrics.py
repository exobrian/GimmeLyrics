# Make HTTP requests
import requests
# Scrape data from an HTML document
from bs4 import BeautifulSoup
from IPython.display import HTML
# I/O
import os
# Search and manipulate strings
import re

GENIUS_API_TOKEN='3ZXND66V7YoAmTauKC05UEKCu5jeQFTnOovEG7YMAvRR0XK0s73AcwZUV4hlyAdw'

print("Hello!")

# Get artist object from Genius API
def request_artist_info(artist_name, page):
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + GENIUS_API_TOKEN}
    search_url = base_url + '/search?per_page=10&page=' + str(page)
    data = {'q': artist_name}
    response = requests.get(search_url, data=data, headers=headers)
    return response
# Get Genius.com song url's from artist object
def request_song_url(artist_name, song_cap):
    page = 1
    songs = []
    
    while True:
        response = request_artist_info(artist_name, page)
        json = response.json()
        # Collect up to song_cap song objects from artist
        song_info = []
        for hit in json['response']['hits']:
            if artist_name.lower() in hit['result']['primary_artist']['name'].lower():
                song_info.append(hit)
    
        # Collect song URL's from song objects
        for song in song_info:
            if (len(songs) < song_cap):
                url = song['result']['url']
                songs.append(url)
            
        if (len(songs) == song_cap):
            break
        else:
            page += 1
        
    print('Found {} songs by {}'.format(len(songs), artist_name))
    return songs    

# Scrape lyrics from a Genius.com song URL
def scrape_song_lyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div.p', class_='lyrics').get_text()
    #remove identifiers like chorus, verse, etc
    lyrics = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
    #remove empty lines
    lyrics = os.linesep.join([s for s in lyrics.splitlines() if s])         
    return lyrics

# Test
demo_songs = request_song_url('Slice the cake', 1)
url = 'https://genius.com/Slice-the-cake-the-exile-part-i-the-razors-edge-lyrics'

page = requests.get(url)
html = BeautifulSoup(page.text, 'html.parser')
html.find('div', class_='Lyrics__Container-sc-1ynbvzw-6 YYrds').get_text().prettify()

#Saving html to file
file = open('/home/brian/Documents/repos/GimmeLyrics/html.txt', 'w')
file.write(html.prettify())
file.close()

