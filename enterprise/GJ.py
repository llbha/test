import base64
import time
from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from .chaojiying import Chaojiying_Client
from .mysql_db import Verify, Company
from .ip_pool import wandouip_ip_pool_http_one

import json


class Gx(object):
    def __init__(self, driver, company):
        self.driver = driver
        self.company = company

    def second_page(self):
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('search_list_item'))
        except Exception as e:
            self.run()
        self.driver.find_elements_by_class_name('search_list_item')[0].click()
        time.sleep(2)
        data = self.detail_page()
        return data

    def detail_page(self):
        time.sleep(2)
        try:
            WebDriverWait(self.driver, 12).until(lambda driver: driver.find_element_by_id('primaryInfo'))
        except Exception as e:
            self.driver.switch_to.window(self.driver.window_handles[1])
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('primaryInfo'))
        result = self.driver.find_elements_by_class_name('result')[1::]
        i = []
        for x in result:
            i.append(x.text)
        try:
            business_scope = self.driver.find_element_by_css_selector('dl.item:nth-child(13) > dd:nth-child(2)').text.strip()
        except Exception as e:
            business_scope = self.driver.find_element_by_css_selector(
                'dl.item:nth-child(12) > dd:nth-child(2)').text.strip()
        i.append(business_scope)
        company = Company()
        company.insert(i)
        result = []
        data = {}
        data['credit_code'] = i[0]
        data['company_name'] = i[1]
        data['types'] = i[2]
        data['legal_person'] = i[3]
        data['reg_capital'] = i[4]
        data['register_date'] = i[5]
        data['bengin_time'] = i[6]
        data['end_time'] = i[7]
        data['reg_auth'] = i[8]
        data['approver_date'] = i[9]
        data['reg_status'] = i[10]
        data['address'] = i[11]
        data['business_scope'] = i[12]
        result.append(data)
        print(result)
        return json.dumps(result)


    # 按语序点击文字
    def click_word(self, src, s):
        mysql = Verify()  # 用户中心>>软件ID 生成一个替换 96001
        res = mysql.select(src)
        if res == '无':
            urlretrieve(src, 'mage.jpg')
            im = open('mage.jpg', 'rb').read()
            chaojiying = Chaojiying_Client('qiyetong1', 'admin1219', '900203')
            a = chaojiying.PostPic(im, 9008)
            pic_str = a.get('pic_str')
        else:
            src = res[1]
            pic_str = res[2]
        if pic_str:
            pic_id = a.get('pic_id')
            groups = pic_str.split('|')
            locations = [[number for number in group.split(',')] for group in groups]
            for b in locations:
                ActionChains(self.driver).move_to_element_with_offset(s, int(b[0])-20,int(b[1])-20).click().perform()
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('geetest_commit')).click()
            try:
                time.sleep(5)
                aa = self.driver.find_element_by_class_name('geetest_item_img')
            except Exception as e:
                return src, pic_str
            else:
                chaojiying.ReportError(pic_id)
                sr = aa.get_attribute('src')
                src,pic_str = self.click_word(sr, aa)
                return src,pic_str
        else:
            src, pic_str = self.click_word(src, s)
            return src, pic_str

    # 滑块拼图验证
    # def sliding_block(self,res,src,s):
    #     # 下面的js代码根据canvas文档说明而来
    #     JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
    #     # 执行 JS 代码并拿到图片 base64 数据
    #     im_info = self.driver.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
    #     im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
    #     im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
    #     with open('a.png', 'wb') as f:  # 保存图片到本地
    #         f.write(im_bytes)
    #     im = open('a.jpg', 'rb').read()
    #     a = Chaojiying_Client.PostPic(im, 9101)
    #     pic_str = a.get('pic_str')
    #     groups = pic_str.split('|')
    #     locations = [[number for number in group.split(',')] for group in groups]
    #     for b in locations:
    #         ActionChains(self.driver).move_to_element_with_offset(s, int(b[0]) - 20, int(b[1]) - 20).click().perform()
    #     time.sleep(2)
    #     WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('geetest_commit')).click()
    #     return pic_str

    def run(self):
        a = Company()
        i = a.select(self.company)
        if '无' in i:
            self.driver.get('http://www.gsxt.gov.cn/index.html')
            time.sleep(2)
            qw = WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('keyword'))
            qw.clear()
            qw.send_keys(self.company)
            time.sleep(2)
            qw.send_keys(Keys.ENTER)
            try:
                time.sleep(2)
                s = WebDriverWait(self.driver, 30).until(
                    lambda driver: driver.find_element_by_class_name('geetest_item_img'))
                res = self.driver.find_element_by_class_name('geetest_mark').text  # 文字点击验证码
            except Exception as e:
                try:
                    s = WebDriverWait(self.driver, 10).until(
                        lambda driver: driver.find_element_by_class_name('geetest_panel_ghost'))
                    res = self.driver.find_element_by_class_name('geetest_mark').text  # 滑块拼图验证码
                except Exception as e:
                    self.second_page()  # 没有验证码

            src = s.get_attribute('src')
            if '语序' in res:
                src, pic_str = self.click_word(src, s)
            else:
                src, pic_str = self.sliding_block(res, src, s)
            s = WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('search_result'))
            if s:
                mysql = Verify()
                res = mysql.insert(src, pic_str)
                if res:
                    data = self.second_page()
                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])
                    self.driver.close()
                    return data
            else:
                g.run()
        else:
            result = []
            data = {}
            data['credit_code'] = i[1]
            data['company_name'] = i[2]
            data['types'] = i[3]
            data['legal_person'] = i[4]
            data['reg_capital'] = i[5]
            data['register_date'] = i[6]
            data['bengin_time'] = i[7]
            data['end_time'] = i[8]
            data['reg_auth'] = i[9]
            data['approver_date'] = i[10]
            data['reg_status'] = i[11]
            data['address'] = i[12]
            data['business_scope'] = i[13]
            result.append(data)
            return result


if __name__ == '__main__':
    data = wandouip_ip_pool_http_one()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--proxy-server=http://%s"% data)
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    # 刚刚解压的chromedriver路径
    driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options)
    # driver = webdriver.Firefox()
    g = Gx(driver, '天猫')
    a = g.run()
    print(a)






