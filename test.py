# Should replace with artist.name instead of artist alone
class Info:
    def __init__(self, artist):
        self.artist = artist

info = Info("The Orb")

# Should probably use regex (?)
def check_artist_name(artist_name, artist_str):
    # Some artists on Discogs are listed without "The" or with an integer inside parenthesis
    # Also discogs adds a "*" after an artist name (?)
    # Discogs also refers Various Artists albums as "Various"
    # Discogs refers to multiple album artists with "&" while Deezer ","
    # e.g. "Higher Intelligence Agency* & Pete Namlook" == "Higher Intelligence Agency, Pete Namlook"
    # e.g. "The Orb" / "Orb" or "Air (2)"

    # Detects if "The" in artist's name
    if "The" in artist_name:
        print(info.artist[4:])

    # Detects for "*" at the end of string
    if artist_str[-1] == "*":
        print(artist_str[-1])

check_artist_name(info.artist, "Orb")
check_artist_name(info.artist, "The Heavenly Music Corporation*")
check_artist_name(info.artist, "Air (2)")