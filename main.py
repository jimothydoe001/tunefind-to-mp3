import requests, sys, urllib
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json
import time
import os

allowedchars = '-.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
ua = UserAgent()
headers = {'User-Agent': ua.random}

def removeDuplicates(songs1,artists1):
    for x in songs1:
        y = songs1.count(x)
        z = songs1.index(x)
        if y != 1:
            songs1.remove(x)
            artists1.pop(z)

    return[songs1, artists1]
def getSeasonPage(seasonLink):
    selected_episode = None
    request_season_page = requests.get(seasonLink, headers=headers)
    soup = BeautifulSoup(request_season_page.text, 'html.parser')
    seasonEpisodes = soup.select('[class*="EpisodeListItem__title"]')
    ssongs = []
    sartists = []

    minEntryIndex = int(min(range(len(seasonEpisodes))) + 1)
    maxEntryIndex = int(max(range(len(seasonEpisodes))) + 1)

    for index, seasonEpisode in enumerate(seasonEpisodes):
        episodeURI = seasonEpisodes[int(index)].find('a')
        temp = getEpisodeSong(episodeURI['href'])
        for i in temp[0]:
            ssongs.append(i)
        for j in temp[1]:
            sartists.append(j)

    return [ssongs, sartists]

def getEpisodeSong(episode):
    selectedTrack = None
    get_episode_page = requests.get(str('https://www.tunefind.com' + episode), headers)
    soup = BeautifulSoup(get_episode_page.text, 'html.parser')
    allSongs = soup.find_all(class_='SongRow__container___3eT_L')
    epsongs = []
    epartists = []

    if not len(allSongs):
        return [[],[]]

    minEntryIndex = int(min(range(len(allSongs))) + 1)
    maxEntryIndex = int(max(range(len(allSongs))) + 1)

    for index, song in enumerate(allSongs):
        song_title = song.find(class_='SongTitle__link___2OQHD')
        song_author = song.find(class_='SongEventRow__subtitle___3Qli4')
        epsongs.append(song_title.text)
        epartists.append(song_author.text)

    return [epsongs, epartists]

def getSeason(URL):
    selectedSeason = None
    request_content_page = requests.get(URL)
    soup = BeautifulSoup(request_content_page.text, 'html.parser')
    allSeasons = soup.select('[class*="MainList__item"]')
    shsongs = []
    shartists = []

    minEntryIndex = int(min(range(len(allSeasons))) + 1)
    maxEntryIndex = int(max(range(len(allSeasons))) + 1)
    
    if minEntryIndex == maxEntryIndex:
        seasonLink = 'https://www.tunefind.com' + allSeasons[0].find('a')['href']
        getSeasonPage(seasonLink)
        return

    for index, season in enumerate(allSeasons):
        season_link = season.find('a')
        if season_link == None:
            continue
        selectedSeason = allSeasons[int(index) - 1]
        try:
            seasonLink = str('https://www.tunefind.com' + selectedSeason.find('a')['href'])
        except:
            continue
        temp2 = getSeasonPage(seasonLink)
        for k in temp2[0]:
            shsongs.append(k)
        for l in temp2[1]:
            shartists.append(l)

    return [shsongs, shartists]

def getTrack(URL, contenttype):
    selected_track = None
    request_content_page = requests.get(URL)
    soup = BeautifulSoup(request_content_page.text, 'html.parser')
    all_tracks = soup.find_all(class_='SongRow__container___3eT_L')
    epsongs = []
    epartists = []

    minEntryIndex = int(min(range(len(all_tracks))) + 1)
    maxEntryIndex = int(max(range(len(all_tracks))) + 1)

    for index, track_single in enumerate(all_tracks):
        song_title = track_single.find(class_='AppearanceRow__songInfoTitle___3nWel') if contenttype == 'artist' else track_single.find(class_='SongTitle__link___2OQHD')
        song_author = track_single.find(class_="Subtitle__subtitle___1rSyh")
        epsongs.append(song_title.text)
        epartists.append(song_author.text)

    return [epsongs, epartists]
class YoutubeSearch:
    def __init__(self, search_terms: str, max_results=None):
        self.search_terms = search_terms
        self.max_results = max_results
        self.videos = self.search()
    def search(self):
        encoded_search = urllib.parse.quote(self.search_terms)
        BASE_URL = "https://www.youtube.com"
        url = f"{BASE_URL}/results?search_query={encoded_search}&sp=EgIQAQ%253D%253D"
        response = BeautifulSoup(requests.get(url).text, "html.parser")
        results = self.parse_html(response)
        if self.max_results is not None and len(results) > self.max_results:
            return results[:self.max_results]
        return results
    def parse_html(self, soup):
        results = []
        for video in soup.select(".yt-uix-tile-link"):
            if video["href"].startswith("/watch?v="):
                video_info = {
                    "tunefind-title": line.strip('\n'),
                    "title": video["title"],
                    "link": "https://www.youtube.com" + video["href"]
                }
                results.append(video_info)
        return results
    def to_dict(self):
        return self.videos
    def to_json(self):
        return json.dumps(self.videos)
class TestSearch:
    def test_init_defaults(self):
        search = YoutubeSearch('test')
        assert search.max_results is None
        assert 1 <= len(search.videos)
    def test_init_max_results(self):
        search = YoutubeSearch('test', max_results=10)
        assert 10 == search.max_results
        assert 10 == len(search.videos)
    def test_dict(self):
        search = YoutubeSearch('test', max_results=10)
        assert isinstance(search.to_dict(), list)
    def test_json(self):
        search = YoutubeSearch('test', max_results=10)
        assert isinstance(search.to_json(), str)
        
URL = input("Please enter TuneFind URL of a TV show or movie: ")
print("This may take a while...")

contenttype = URL.split('/')[3]

if contenttype == 'artist' or contenttype == 'movie':
    result = getTrack(URL, contenttype)
elif contenttype == 'show':
    result = getSeason(URL)

temp = removeDuplicates(result[0], result[1])
songs = temp[1]
artists = temp[0]

listfile=open("tmp/files/" + URL.split('/')[4] + ".list.txt", "w")

print("Got all songs from " + URL.split('/')[4].replace("-", " ").title() + " and saved them in '" + URL.split('/')[4] + ".txt'\n")
for i in range(len(songs)):
    try:
        print("{} - {}".format(songs[i], artists[i]))
        listfile.write("{} - {}".format(songs[i], artists[i]) + "\n")
    except IndexError:
        print("Skipped {} - {}".format(songs[i], artists[i]))
listfile.close()
print("\n\nFinished retreiving the list, now getting the youtube links.")


ytlistfile=open("tmp/files/" + URL.split('/')[4] + ".yt.txt", "w")
emptystringy = '[]'
with open('tmp/files/' + URL.split('/')[4] + ".list.txt") as ytlistfile2:
    for line in ytlistfile2:
        results = YoutubeSearch(line, max_results=1).to_json()
        while results == emptystringy:
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
            if results == emptystringy:
                results = YoutubeSearch(line, max_results=1).to_json()
                print("\n\nSkipped " + line)
            break
        print("\n" + line.strip('\n'))
        ytlistfile.write(results.strip("[]") + "\n")
        print(results)
ytlistfile.close()

with open('tmp/files/' + URL.split('/')[4] + '.yt.txt') as f:
    for fofo in f:
        z = json.loads(fofo)
        newtitle = z["tunefind-title"]
        all_ascii = ''.join( c for c in newtitle if c in allowedchars )
        os.system(("mkdir -p {}").format(URL.split('/')[4]))
        os.system(("youtube-dl -o tmp/{}/'{}.%(ext)s' --cookies tmp/files/cookies.txt -4 --restrict-filenames -x --audio-format mp3 '{}' ").format(URL.split('/')[4], all_ascii, z["link"]))
f.close()
