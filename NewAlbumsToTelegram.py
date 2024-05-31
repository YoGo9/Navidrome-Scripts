import requests

# Configuration Variables
navidrome_api_url = 'https://your-navidrome-url/rest'
navidrome_user = 'your_username'
navidrome_password = 'your_password'
client_name = 'your_client_name'
api_version = '1.16.1'
telegram_bot_token = 'your_telegram_bot_token'
telegram_chat_id = 'your_telegram_chat_id'
known_albums_file = 'known_albumstest.txt'

def get_known_albums():
    try:
        with open(known_albums_file, 'r') as file:
            known_albums = set(file.read().splitlines())
    except FileNotFoundError:
        known_albums = set()
    return known_albums

def save_known_album(album_id):
    with open(known_albums_file, 'a') as file:
        file.write(f"{album_id}\n")

def get_recent_albums(count=6):
    params = {
        'u': navidrome_user,
        'p': navidrome_password,
        'c': client_name,
        'v': api_version,
        'f': 'json',
        'type': 'newest',
        'size': count
    }
    response = requests.get(f"{navidrome_api_url}/getAlbumList2", params=params)
    if response.status_code == 200:
        data = response.json()
        albums = data['subsonic-response']['albumList2']['album']
        return albums
    else:
        print(f"Failed to fetch data: {response.status_code}")
    return []

def get_cover_art_url(album_id):
    """Generate the URL for the album's cover art."""
    params = {
        'u': navidrome_user,
        'p': navidrome_password,
        'c': client_name,
        'v': api_version,
        'id': album_id
    }
    return f"{navidrome_api_url}/getCoverArt?{requests.compat.urlencode(params)}"

def send_telegram_message(message, photo_url=None):
    """Send a message and optional photo via Telegram."""
    if photo_url:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendPhoto"
        data = {
            'chat_id': telegram_chat_id,
            'caption': message,
            'photo': photo_url
        }
    else:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        data = {
            'chat_id': telegram_chat_id,
            'text': message
        }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")

def main():
    known_albums = get_known_albums()
    print("Checking for recent albums...")
    recent_albums = get_recent_albums()
    for album in recent_albums:
        album_id = album['id']
        if album_id not in known_albums:
            release_year = album.get('year', 'Unknown release year')
            track_count = album.get('songCount', 'Unknown number of tracks')
            message = f"New album added: {album['name']} by {album['artist']}, released in {release_year}. Total tracks: {track_count}."
            cover_art_url = get_cover_art_url(album_id)
            print(message)
            send_telegram_message(message, photo_url=cover_art_url)
            save_known_album(album_id)

if __name__ == "__main__":
    main()import requests

# Configuration Variables
navidrome_api_url = 'https://your-navidrome-url/rest'
navidrome_user = 'your_username'
navidrome_password = 'your_password'
client_name = 'your_client_name'
api_version = 'your_api_version'
telegram_bot_token = 'your_telegram_bot_token'
telegram_chat_id = 'your_telegram_chat_id'
known_albums_file = 'known_albums.txt'

def get_known_albums():
    try:
        with open(known_albums_file, 'r') as file:
            known_albums = set(file.read().splitlines())
    except FileNotFoundError:
        known_albums = set()
    return known_albums

def save_known_album(album_id):
    with open(known_albums_file, 'a') as file:
        file.write(f"{album_id}\n")

def get_recent_albums(count=6):
    """Fetch the latest albums from Navidrome using the Subsonic API."""
    params = {
        'u': navidrome_user,
        'p': navidrome_password,
        'c': client_name,
        'v': api_version,
        'f': 'json',
        'type': 'newest',
        'size': count
    }
    response = requests.get(f"{navidrome_api_url}/getAlbumList2", params=params)
    if response.status_code == 200:
        data = response.json()
        albums = data['subsonic-response']['albumList2']['album']
        return albums
    else:
        print(f"Failed to fetch data: {response.status_code}")
    return []

def send_telegram_message(message):
    """Send a message via Telegram."""
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    data = {
        'chat_id': telegram_chat_id,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print(f"Failed to send message: {response.status_code}")

def main():
    known_albums = get_known_albums()
    print("Checking for recent albums...")
    recent_albums = get_recent_albums()
    for album in recent_albums:
        album_id = album['id']
        if album_id not in known_albums:
            release_year = album.get('year', 'Unknown release year')
            track_count = album.get('songCount', 'Unknown number of tracks')
            message = f"New album added: {album['name']} by {album['artist']}, released in {release_year}. Total tracks: {track_count}."
            print(message)
            send_telegram_message(message)
            save_known_album(album_id)

if __name__ == "__main__":
    main()
