import requests
import os

def get_emoji_image(name, size=256):
    path = f'./emoji_pictures/{name}-{size}.png'
    if not os.path.isfile(path):
        with open(path, 'wb') as f:
            f.write(requests.get(f'https://emojiapi.dev/api/v1/{name}/{size}.png').content)
    with open(path, 'rb') as f:
        return f.read()