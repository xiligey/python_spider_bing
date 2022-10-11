import requests
import time
import os
import random

# 添加请求头
g_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 '
                  'Safari/537.36 '
}


def get_bing_image_urls(num):
    """
    从cn.bing.com下载每日的桌面壁纸
    :param num: 最多获取壁纸数
    :return: 返回获取的壁纸地址列表
    """
    start_url = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx={}&n=1'
    images = []
    page = 1
    while len(images) < num and page < num * 2:
        page += 1
        page_url = start_url.format(page)
        try:
            r = requests.get(page_url, headers=g_headers).json()
            img = 'https://cn.bing.com' + r['images'][0]['url']
            if images.count(img) <= 0:
                images.append(img)
            else:
                break
        except Exception:
            pass
    return images


def download_image(url, save_path):
    """
    根据图片地址下载图片至指定路径
    :param url: 图片url地址
    :param save_path: 图片保存路径
    :return: 下载是否成功
    """
    try:
        r = requests.get(url, headers=g_headers, stream=True)
        if r.status_code != 200:
            return False
        open(save_path, 'wb').write(r.content)
        return True
    except Exception:
        return False


def get_image_id(url):
    """
    从URL地址获取图片的参数id信息
    :param url: bing图片url地址
    :return: 图片id
    """
    try:
        paras = url[url.find('?') + 1:].split('&')
        for p in paras:
            kv = p.split('=')
            if kv[0] == 'id':
                return kv[1].strip()
    except Exception:
        pass
    return url


def set_desktop_image(img):
    """
    将图片设置为桌面壁纸
    :param img: 图片
    :return:
    """
    import win32gui
    import win32con
    import win32api
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,
                                "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2")
    # 2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, os.path.abspath(img), 1 + 2)


def auto_change_desktop_image(img_dir, seconds=300, order='rand'):
    """
    根据指定的壁纸目录，定时更新桌面壁纸，当前日期变化后会退出
    :param img_dir: 壁纸目录
    :param seconds: 自动更新时间间隔，单位为秒
    :param order: 图片更新顺序，默认为顺序，rand为随机
    :return:
    """
    files = os.listdir(img_dir)
    images = []
    for file in files:
        temp = os.path.join(img_dir, file)
        if os.path.isfile(temp):
            images.append(temp)
    start_date = time.strftime('%Y%m%d', time.localtime(time.time()))
    index = -1
    while True:
        # 日期变了退出，重新获取
        cur_date = time.strftime('%Y%m%d', time.localtime(time.time()))
        if cur_date != start_date:
            break
        index += 1
        if order == 'rand':
            index = random.randint(0, len(images) - 1)
        index = index % len(images)
        set_desktop_image(images[index])
        print(time.time(), ' 已设置桌面壁纸为:', images[index])
        time.sleep(seconds)


if __name__ == '__main__':
    while True:
        # 获取每日壁纸
        urls = get_bing_image_urls(20)
        save_dir = './' + time.strftime('%Y%m%d', time.localtime(time.time()))
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for url in urls:
            name = get_image_id(url)
            save_path = save_dir + '/' + name
            print('下载', url, '成功' if download_image(url, save_path) else '失败')
        # 自动更新壁纸
        auto_change_desktop_image(save_dir, 60)
