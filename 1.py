import requests
import re


def download(title, url):
    path = 'img\\' + title
    response = requests.get(url=url)
    with open(path, mode='wb+') as f:
        f.write(response.content)


for page in range(1, 126):
    url = 'https://wallhaven.cc/toplist?page={}'.format(page)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)

    urls = re.findall('<a class="preview" href="(.*?)"', response.text)
    for i in urls:
        response_2 = requests.get(url=i, headers=headers)
        img_url = re.findall('<img id="wallpaper" src="(.*?)"', response_2.text)[0]
        title = img_url.split('-')[-1]
        download(title, img_url)
        print(img_url)
