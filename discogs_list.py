# todos: clean code, oop, etc

from selenium import webdriver
from selenium.webdriver.common.by import By
import configparser
import deezer
import time
import re
import os

config = configparser.ConfigParser()
config.read("config.ini")
driver = webdriver.Chrome(config["General"]["chromedriver_path"])

albums_list = []
albums_links = []
albums_unavailaible = []

def fuck_cookies():
    print("Accepting cookies...")
    e = driver.find_element(By.XPATH, config["Auth"]["cookie_btn_xpath"])
    e.click()

def is_empty(string):
    return re.search("^\s*$", string)

def clean_list(w_list):
    for string in w_list:
        if is_empty(string):
            w_list.remove(string)

def check_album_title(info, album_str):
    # Some EPs on Discogs are listed with or without at the end
    # Some EPs on Deezer are listed with or without "EP" at the end
    # This is used to make the search more "clear"
    # It's safer to just search for the album without the "EP"
    # e.g. (Laurent Garnier - Club Traxx EP)
    if "EP" in album_str:
        return album_str[:-2]

# def if_various(info, album_str):
#     # If Various Artists album, check only album title and tracks inside
#     # e.g. "Various - Ambient-Compilation 4"

# def check_artist_name(info, artist_str):
#     # Some artists on Discogs are listed without "The" or with an integer inside parenthesis
#     # Also discogs adds a "*" after an artist name (?)
#     # Discogs also refers Various Artists albums as "Various"
#     # Discogs refers to multiple album artists with "&" while Deezer ","
#     # e.g. "Higher Intelligence Agency* & Pete Namlook" == "Higher Intelligence Agency, Pete Namlook"
#     # e.g. "The Orb" / "Orb" or "Air (2)"

def getAlbumInfo(link):
    print("Getting albums from: " + link)
    driver.get(link)
    fuck_cookies()
    all_albums = driver.find_elements_by_css_selector("h3.listitem_title a")
    for album in all_albums:
        albums_list.append(album.text)
    clean_list(albums_list)

def get_album_title(album):
    return album.split("- ", 1)[1]

def get_album_artist(album):
    return album.split(" -")[0]

def file_exists(file):
    if os.path.isfile(file):
        print(file + " exists.")
        return True
    else:
        print(file + " does not exist.")
        return False

def is_correct_album(info, album_str):
    if info.title == get_album_title(album_str) OR 
       info.title == check_album_title(info.title, get_album_title(album_str)):
        if info.artist.name == get_album_artist(album_str):
            albums_links.append(info.link)
        else:
            print("Artist doesn't match... Skipping!")
    else:
        # Should improve 
        print("Album title doesn't match... Skipping!")

def search_deezer(album_str):
    client = deezer.Client(access_token=config["Auth"]["access_token"])
    album = client.search(album_str, relation="album")
    for info in album:
        is_correct_album(info, album_str)

# Clean this! Actually clean the whole project once you're done.
getAlbumInfo("https://www.discogs.com/fr/lists/test-list/631065")
for album in albums_list:
    print("Searching: " + album)
    search_deezer(album)
with open('downloadLinks.txt', 'w') as f:
    for link in albums_links:
        f.write("%s\n" % link)
with open('downloadUnavailaible.txt', 'w') as f:
    for album in albums_unavailaible:
        f.write("%s\n" % album)