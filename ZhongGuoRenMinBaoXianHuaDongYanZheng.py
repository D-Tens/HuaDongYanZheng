'''
中国人民保险
http://www.epicc.com.cn/idprovider/views/login.jsp?h=https://www.epicc.com.cn/?cmpid=3seb2pzBT00050GPX02&utm_source=baidu&utm_medium=search_cpc&utm_term=%e6%a0%87%e9%a2%98&utm_campaign=%e7%89%881&utm_adgroup=%e6%a0%87%e9%a2%98&utm_channel=%e7%bd%91%e9%a1%b5
'''
import random
import time
import re
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Crack():
    def __init__(self, username, pwd):
        self.url = 'http://www.epicc.com.cn/idprovider/views/login.jsp?h=https://www.epicc.com.cn/?cmpid=3seb2pzBT00050GPX02&utm_source=baidu&utm_medium=search_cpc&utm_term=%e6%a0%87%e9%a2%98&utm_campaign=%e7%89%881&utm_adgroup=%e6%a0%87%e9%a2%98&utm_channel=%e7%bd%91%e9%a1%b5'
        self.browser = webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 60)
        self.BORDER = random.uniform(9.9, 10.05)
        self.username = username
        self.pwd = pwd

    def open(self):
        '''打开浏览器，并输入查询内容'''
        self.browser.get(self.url)
        # 切换登录
        login_cut = self.browser.find_element_by_xpath('//ul[@class="login-tab-list"]/li[2]')
        login_cut.click()
        time.sleep(random.uniform(0.5, 1.5))
        # 用户名
        keyword = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="entryId"]')))
        keyword.send_keys(self.username)
        time.sleep(random.uniform(0.5, 1.5))
        # 密码
        keyword = self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="password"]')))
        keyword.send_keys(self.pwd)
        time.sleep(random.uniform(0.5, 1.5))

    def download_image(self, img_name, url):
        '''图片下载'''
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        response = requests.get(url, headers=headers)
        with open('./images/' + img_name + '.jpg', 'wb') as file:
            file.write(response.content)

    def get_imags(self, base_url='http://www.epicc.com.cn'):
        '''获取验证图片'''
        # 无卡槽
        img_name = 'img1'
        js = 'document.getElementsByClassName("captcha-box")[0].style.display="none";'
        self.browser.execute_script(js)
        img = self.browser.find_element_by_class_name('captcha-box-content ').get_attribute('style')
        img_url = base_url + re.search('url\("(.*?)"\);', img).group(1)
        self.download_image(img_name, img_url)
        # 有卡槽
        img_name = 'img2'
        js = 'document.getElementsByClassName("captcha-box")[0].style.display="block";'
        self.browser.execute_script(js)
        login_cut = self.browser.find_element_by_xpath('//span[@class="slide-bar"]')
        login_cut.click()
        img = self.browser.find_element_by_class_name('captcha-box-content ').get_attribute('style')
        img_url = base_url + re.search('url\("(.*?)"\);', img).group(1)
        self.download_image(img_name, img_url)
        time.sleep(random.random())

    def is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的指定位置的像素点
        # load()加载Image对象的像素
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if (abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
                pix1[2] - pix2[2]) < threshold):
            return True
        else:
            return False

    def get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图片
        :return:
        """
        left = 10
        # size是Image对象的属性，表示图片尺寸（宽，高）
        for i in range(left, img1.size[0]):  # 宽，水平方向
            for j in range(img1.size[1]):  # 高，垂直方向
                if not self.is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * random.uniform(0.68, 0.73)
        # 计算间隔
        t = random.uniform(0.09, 0.15)
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 40
            else:
                # 加速度为负3
                a = -24
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))

        v = 0

        # print(current, distance)
        move = distance - current
        # 加入轨迹
        track.append(round(move))
        return track

    def get_slider(self):
        """
        获取滑块
        :return: 滑块对象
        """
        while True:
            try:
                slider = self.browser.find_element_by_xpath('//span[@class="slide-bar"]')
                break
            except:
                time.sleep(0.5)
        return slider

    def move_to_gap(self, slider, track):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        :return:
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        while track:
            x = track.pop(0)
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(2)
        # print('release')
        ActionChains(self.browser).release(slider).perform()
        time.sleep(2)

    def crack(self):
        # 打开浏览器
        self.open()
        img1 = './images/img1.jpg'
        img2 = './images/img2.jpg'
        # 获取图片
        self.get_imags()
        # 加载验证码带阴影背景图和全背景图
        bg_img = Image.open(img1)
        fullbg_img = Image.open(img2)
        # 获取缺口位置
        gap = self.get_gap(fullbg_img, bg_img)
        # print('缺口位置', gap)
        # 生成移动的轨迹
        track = self.get_track(gap - self.BORDER)
        # print('滑动滑块')
        # print(track)
        # 点按呼出缺口
        slider = self.get_slider()
        # 拖动滑块到缺口处
        self.move_to_gap(slider, track)
        time.sleep(1)
        slide_content = self.browser.find_element_by_class_name('slide-tip').text.strip()
        if slide_content == '拖动滑块完成验证':
            self.crack()
        else:
            self.browser.close()
            print('验证成功！')


if __name__ == '__main__':
    crack = Crack('111111', '22222')
    crack.crack()
