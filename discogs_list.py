# todos: clean code, oop, etc

from selenium import webdriver
from selenium.webdriver.common.by import By
import deezer
import time
import re

driverPath = "chromedriver.exe"
driver = webdriver.Chrome(driverPath)

albums_list = []

def fuck_cookies():
    print("Accepting cookies...")
    btn_cookie = "//*[@id='onetrust-accept-btn-handler']"
    e = driver.find_element(By.XPATH, btn_cookie)
    e.click()

def is_empty(string):
    return re.search("^\s*$", string)

def clean_list(w_list):
    for string in w_list:
        if is_empty(string):
            w_list.remove(string)

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

def is_correct_album(info, album_str):
    if info.title == get_album_title(album_str):
        print("Album title seems to match!")
        if info.artist.name == get_album_artist(album_str):
            print("Artist seems to match! Adding link to downloadLinks.txt")
            # Add link to text file
        else:
            print("Artist doesn't match... Skipping!")
    else:
        print("Album title doesn't match... Skipping!")

def search_deezer(album_str):
    client = deezer.Client(access_token="not_leaking_that")
    album = client.search(album_str, relation="album")
    for info in album:
        is_correct_album(info, album_str)

getAlbumInfo("https://www.discogs.com/fr/lists/test-list/631065")
for album in albums_list:
    print("Searching: " + album)
    search_deezer(album)