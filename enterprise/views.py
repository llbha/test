from django.http import JsonResponse
import base64
import time
from urllib.request import urlretrieve

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver.support.ui import WebDriverWait

from .chaojiying import Chaojiying_Client
from .ip_pool import wandouip_http_one

from .models import *
from django.forms.models import model_to_dict
import json


class Gx(object):
    def __init__(self, driver, company):
        self.driver = driver
        self.company = company
        self.num = 0
        self.count = 0

    def second_page(self):
        time.sleep(2)
        try:
            self.num += 1
            WebDriverWait(self.driver, 10).until(lambda driver: driver.find_element_by_class_name('search_list_item'))
        except Exception as e:
            try:
                a = Company.objects.filter(unit=company)[0]
            except Exception as e:
                if self.num == 2:
                    dic = {
                        'credit_code': '暂无信息',
                        'company_name': self.company,
                        'types': '暂无信息',
                        'legal_person': '暂无信息',
                        'reg_capital': '暂无信息',
                        'register_date': '暂无信息',
                        'bengin_time': '暂无信息',
                        'end_time': '暂无信息',
                        'reg_auth': '暂无信息',
                        'approver_date': '暂无信息',
                        'reg_status': '暂无信息',
                        'address': '暂无信息',
                        'business_scope': '暂无信息',
                        'unit': self.company
                    }
                    Company.objects.create(**dic)
                    return json.dumps(dic)
                self.driver.refresh()
                data = self.second_page()
                return data
            if a:
                a = model_to_dict(a)
                return JsonResponse(dict(msg=a))
        self.driver.find_elements_by_class_name('search_list_item')[0].click()
        try:
            WebDriverWait(self.driver, 5).until(lambda driver: driver.find_element_by_id('primaryInfo'))
        except Exception as e:
            try:
                self.driver.switch_to.window(self.driver.window_handles[1])
                WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_id('primaryInfo'))
            except Exception as e:
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.close()
                return '未进入详情页'

        res = self.driver.find_elements_by_css_selector('.overview > dl')
        if len(res) == 13:
            result = self.driver.find_elements_by_class_name('result')[1::]
            data = []
            for x in result:
                data.append(x.text)
            business_scope = self.driver.find_element_by_css_selector('dl.item:nth-child(13) > dd:nth-child(2)').text.strip()
            data.append(business_scope)
            dic = {
                'credit_code': data[0],
                'company_name': data[1],
                'types': data[2],
                'legal_person': data[3],
                'reg_capital': data[4],
                'register_date': data[5],
                'bengin_time': data[6],
                'end_time': data[7],
                'reg_auth': data[8],
                'approver_date': data[9],
                'reg_status': data[10],
                'address': data[11],
                'business_scope': data[12],
                'unit': self.company
            }
        elif len(res) == 12:
            result = self.driver.find_elements_by_class_name('result')[1::]
            data = []
            for x in result:
                data.append(x.text)
            dic = {
                'credit_code': data[0],
                'company_name': data[1],
                'types': data[2],
                'legal_person': data[3],
                'reg_capital': '',
                'register_date': data[7],
                'bengin_time': data[4],
                'end_time': data[5],
                'reg_auth': data[6],
                'approver_date': data[9],
                'reg_status': data[8],
                'address': data[10],
                'business_scope': data[11],
                'unit': self.company
            }
        elif len(res) == 11:
            result = self.driver.find_elements_by_class_name('result')[2::]
            data = []
            for x in result:
                data.append(x.text)
            dic = {
                'credit_code': data[0],
                'company_name': data[1],
                'types': data[2],
                'legal_person': data[3],
                'reg_capital': '',
                'register_date': data[4],
                'bengin_time': data[5],
                'end_time': '',
                'reg_auth': data[6],
                'approver_date': data[7],
                'reg_status': data[8],
                'address': data[9],
                'business_scope': data[10],
                'unit': self.company
            }
        try:
            comp = Company.objects.filter(unit=self.company)[0]
            if comp.company_name == data[1]:
                comp.delete()
        except Exception as e:
            pass
        Company.objects.create(**dic)
        try:
            dic['reg_capital'] = dic['reg_capital'].split('.')[0]
        except Exception as e:
            pass
        return json.dumps(dic)

    # 按语序点击文字
    def click_word(self, src, s):
        try:
            res = Chaojiying.objects.get(img=src)
        except Exception as e:
            urlretrieve(src, 'mage.jpg')
            im = open('mage.jpg', 'rb').read()
            chaojiying = Chaojiying_Client('qiyetong1', 'admin1219', '900203')   # 用户中心>>软件ID 生成一个替换 96001
            a = chaojiying.PostPic(im, 9008)
            pic_str = a.get('pic_str')
            pic_id = a.get('pic_id')
        else:
            src = res.img
            pic_str = res.pic_str
        if pic_str:
            groups = pic_str.split('|')
            locations = [[number for number in group.split(',')] for group in groups]
            for b in locations:
                ActionChains(self.driver).move_to_element_with_offset(s, int(b[0])-20,int(b[1])-20).click().perform()
            WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('geetest_commit')).click()
            try:
                time.sleep(2)
                aa = self.driver.find_element_by_class_name('geetest_item_img')
            except Exception as e:
                return src, pic_str
            else:
                if self.count == 1:
                    return '两次打码失败！'
                if pic_id:
                    chaojiying.ReportError(pic_id)
                self.count += 1
                sr = aa.get_attribute('src')
                src, pic_str = self.click_word(sr, aa)
                return src, pic_str
        else:
            src, pic_str = self.click_word(src, s)
            return src, pic_str

    # 滑块拼图验证
    def sliding_block(self):
        # 下面的js代码根据canvas文档说明而来
        # JS = 'return document.getElementsByClassName("geetest_canvas_bg geetest_absolute")[0].toDataURL("image/png");'
        # # 执行 JS 代码并拿到图片 base64 数据
        # im_info = self.driver.execute_script(JS)  # 执行js文件得到带图片信息的图片数据
        # im_base64 = im_info.split(',')[1]  # 拿到base64编码的图片信息
        # im_bytes = base64.b64decode(im_base64)  # 转为bytes类型
        # with open('a.png', 'wb') as f:  # 保存图片到本地
        #     f.write(im_bytes)
        # im = open('a.jpg', 'rb').read()
        # a = Chaojiying_Client.PostPic(im, 9101)
        # pic_str = a.get('pic_str')
        # groups = pic_str.split('|')
        # locations = [[number for number in group.split(',')] for group in groups]
        # for b in locations:
        #     ActionChains(self.driver).move_to_element_with_offset(s, int(b[0]) - 20, int(b[1]) - 20).click().perform()
        # time.sleep(2)
        # WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('geetest_commit')).click()
        return '滑块验证'

    def run(self):
        self.driver.get('http://www.gsxt.gov.cn/index.html')
        try:
            qw = WebDriverWait(self.driver, 20).until(lambda driver: driver.find_element_by_id('keyword'))
        except Exception as e:
            self.driver.close()
            return '网址打开失败！'
        qw.clear()
        qw.send_keys(self.company)
        time.sleep(2)
        self.driver.find_element_by_id('btn_query').click()
        print('**********')
        # try:
        #     time.sleep(0.5)
        #     self.driver.find_element_by_id('btn_query').click()
        #     print('===========')
        # except Exception as e:
        #     pass
        try:
            time.sleep(1)
            s = WebDriverWait(self.driver, 25).until(
                lambda driver: driver.find_element_by_class_name('geetest_item_img'))
            res = self.driver.find_element_by_class_name('geetest_mark').text  # 文字点击验证码
        except Exception as e:
            try:
                s = WebDriverWait(self.driver, 2).until(
                    lambda driver: driver.find_element_by_class_name('geetest_panel_ghost'))
                res = self.driver.find_element_by_class_name('geetest_mark').text  # 滑块拼图验证码
            except Exception as e:
                try:
                    s = WebDriverWait(self.driver, 2).until(
                        lambda driver: driver.find_element_by_class_name('ads-sci-list'))
                except Exception as e:
                    self.driver.close()
                    return '验证码没有出现！'
                data = self.second_page()  # 没有验证码
                return data

        src = s.get_attribute('src')
        if '语序' in res:
            try:
                src, pic_str = self.click_word(src, s)
            except Exception as e:
                data = self.click_word(src, s)
                if data == '两次打码失败！':
                    self.driver.close()
                    return data
        else:
            # data = self.sliding_block()
            self.driver.close()
            return '滑块验证'
        s = WebDriverWait(self.driver, 30).until(lambda driver: driver.find_element_by_class_name('ads-sci-list'))
        if s:
            chao = Chaojiying()
            chao.img = src
            chao.pic_str = pic_str
            chao.save()
            data = self.second_page()
            self.driver.close()
            try:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.close()
            except Exception as e:
                pass
            return data
        else:
            self.driver.close()
            return '无法获取公司列表页信息！'


@csrf_exempt
def company(request):
    company = request.GET.get('company')
    if not company:
        return JsonResponse(dict(code=-1, msg='需要company参数'))
    try:
        a = Company.objects.filter(unit=company)[0]
        a = model_to_dict(a)
        a['num'] = len(a)-1
    except Exception as e:
        data = wandouip_http_one()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--proxy-server=http://%s" % data)
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=chrome_options)
        g = Gx(driver, company)
        a = g.run()
        print(a)
    return JsonResponse(dict(msg=a))
