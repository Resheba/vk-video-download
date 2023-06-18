import requests, json
from bs4 import BeautifulSoup as bs

headers = {
    'authority': 'vk.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9',
    'cache-control': 'max-age=0',
    'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
}


def download(url: str, filename: str = 'video') -> None:
    with open(filename + '.mp4', 'wb') as file:
        response = requests.get(url, headers=headers, stream=True)
        for chunk in response.iter_content(1024 * 1000):
            file.write(chunk)


def get_player_url(url: str) -> str:
    response = requests.get(url, headers=headers)
    soup = bs(response.text, 'html.parser')
    meta_og_video = soup.find("meta", property="og:video")
    return meta_og_video.attrs['content']


def get_video_url(pleer_url: str) -> str:
    # GET HTML
    response = requests.get(pleer_url, headers=headers)
    soup = bs(response.text, 'html.parser')
    # CLEAN JS CODE
    js_code = soup.select_one('body > script:nth-child(11)').text
    first_split = js_code.split('var playerParams = ')[1]
    second_split = first_split.split('var container')[0]
    replacements = second_split.strip().replace(' ', '').replace('\n', '').replace(';', '')
    # JS TO JSON
    info = json.loads(replacements)
    info = info.get('params')[0]
    # GET VIDEO URL
    for quality in ('1080', '720', '480', '360', '240'):
        url = info.get('url' + quality)
        if url:
            url = url.replace('\\', '')
            return url


def download_video(video_url: str, filename: str = 'video') -> None:
    player_url = get_player_url(video_url)
    download_url = get_video_url(player_url)
    download(download_url, filename)


# avoid shadow scope
def main():
    video_url = "https://vk.com/video-22822305_456239018"
    download_video(video_url)


if __name__ == '__main__':
    main()
