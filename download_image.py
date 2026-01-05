import urllib.request

def download_image(url, save_as):
    urllib.request.urlretrieve(url, save_as)

def main():
    for i in range(1, 401):
        image_url = f'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{i}.png'
        save_as = f'asset/{i}.png'

        download_image(image_url, save_as)

main()