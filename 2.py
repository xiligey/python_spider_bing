import win32api
import win32con
import win32gui
import os
import time


def Windows_img(paperPath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    # 在注册表中写入属性值
    win32api.RegSetValueEx(k, "wapaperStyle", 0, win32con.REG_SZ, "2")  # 0 代表桌面居中 2 代表拉伸桌面
    win32api.RegSetValueEx(k, "Tilewallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, paperPath, win32con.SPIF_SENDWININICHANGE)  # 刷新桌面


def changeWallpaper():
    """文件夹/文件夹/图片"""
    path = input('请输入文件路径:')
    L2 = os.listdir(path=path)  # 得到文件路径下的壁纸文件夹，列表类型
    i = 0
    print(L2)  # 壁纸文件夹
    url_list = []
    for l2 in L2:
        detail_path = path + '\\' + l2
        L3 = os.listdir(detail_path)  # 得到壁纸文件夹路径下的图片，列表类型
        for l3 in L3:
            url_list.append(detail_path + '\\' + l3)
    print(url_list)
    while True:
        Windows_img(url_list[i])
        print('{}'.format(url_list[i]))
        time.sleep(2)  # 设置壁纸更换间隔，这里为10秒，根据用户自身需要自己设置秒数
        i += 1
        if i == len(url_list):  # 如果是最后一张图片，则重新到第一张
            i = 0


def changeWallpaper_2():
    """文件夹/图片"""
    path = input('请输入文件路径:')
    L2 = os.listdir(path=path)  # 得到文件路径下的图片，列表类型
    i = 0
    print(L2)
    while True:
        Windows_img(path + '\{}'.format(L2[i]))
        print(path + '\{}'.format(L2[i]))
        time.sleep(1000)  # 设置壁纸更换间隔，这里为10秒，根据用户自身需要自己设置秒数
        i += 1
        if i == len(L2):  # 如果是最后一张图片，则重新到第一张
            i = 0


if __name__ == '__main__':
    changeWallpaper()
