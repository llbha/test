import requests
import json
import time
import random
import base64


def mimvp_ip_pool():
    url = 'https://proxyapi.mimvp.com/api/fetchsecret.php?orderid=865050906019182392&num=5&http_type=3&result_fields=1,2,3&result_format=json'
    response = requests.get(url).content.decode()
    # print("*"*88)
    # print(response)
    # print("*"*88)
    s = json.loads(response)
    pool = []
    if s['code_msg'] == '提取成功':
        for i in s['result']:
            pool.append(i["ip:port"])
        return json.dumps(pool)
    else:
        time.sleep(5)

        mimvp_ip_pool()


# s = mimvp_ip_pool()
# print(s)

# http://h.jiguangdaili.com/ucenter/recharge_ucenter.html
def golangapi_ip_pool():
    # url = 'http://d.jghttp.golangapi.com/getip?num=50&type=2&pro=&city=0&yys=0&port=11&pack=11034&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions='
    url = 'http://d.jghttp.golangapi.com/getip?num=1&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='
    response = requests.get(url).content.decode()
    # print("*"*88)
    # print(response)
    # print("*"*88)
    s = json.loads(response)
    # print(response)
    pool = []
    if s['msg'] == '0':
        for i in s['data']:
            pool.append(str(i["ip"]) + ":" + str(i["port"]))
        return json.dumps(pool)
    else:
        time.sleep(2)
        golangapi_ip_pool()


# p = mimvp_ip_pool()
# print(p)
# s = golangapi_ip_pool()
# print(s)

def golangapi_ip_pool_n(n):
    # url = 'http://d.jghttp.golangapi.com/getip?num=50&type=2&pro=&city=0&yys=0&port=11&pack=11034&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=2&regions='
    url = 'http://d.jghttp.golangapi.com/getip?num={}&type=2&pro=&city=0&yys=0&port=11&time=1&ts=1&ys=0&cs=0&lb=1&sb=0&pb=45&mr=1&regions='.format(
        n)
    response = requests.get(url).content.decode()
    # print("*"*88)
    # print(response)
    # print("*"*88)
    s = json.loads(response)
    # print(response)
    pool = []
    if s['msg'] == '0':
        for i in s['data']:
            pool.append(str(i["ip"]) + ":" + str(i["port"]))
        return json.dumps(pool)
    else:
        time.sleep(2)
        golangapi_ip_pool()


# def base_code(username, password):
#         str = '%s:%s' % (username, password)
#         encodestr = base64.b64encode(str.encode('utf-8'))
#         return '%s' % encodestr.decode()
#
# def tip(_ip):
#         url = "http://myip.ipip.net"
#
#         ip_port = _ip # 从api中提取出来的代理IP:PORT
#         username = 'laurence@bluehui.com'
#         password = 'Admin1210'
#
#         # basic_pwd = base_code(username, password)
#
#         # headers = {
#         #     'Proxy-Authorization': 'Basic %s' % (base_code(username, password))
#         # }
#
#         proxy = {
#             'http' : 'socks5://{}'.format(ip_port),
#             'https' : 'socks5://{}'.format(ip_port)
#         }
#
#         r = requests.get(url,proxies=proxy
#                          # , headers=headers
#                          )
#         print(r.text)
#
def wandouip_ip_pool(n="5"):
    url = 'http://api.wandoudl.com/api/ip?app_key=88a34462e4f758ee750dac2bf22ba6c6&pack=205555&num={}&xy=3&type=2&lb=\r\n&mr=1&'.format(n)
    response = requests.get(url).content.decode()
    # print(response)
    s = json.loads(response)
    pool = []
    for i in s['data']:
        ip_ = str(i["ip"]) + ":" + str(i["port"])
        pool.append(ip_)
    return json.dumps(pool)

def wandouip_ip_pool_one():
    url = 'http://api.wandoudl.com/api/ip?app_key=88a34462e4f758ee750dac2bf22ba6c6&pack=205555&num=1&xy=3&type=2&lb=\r\n&mr=1&'
    response = requests.get(url).content.decode()
    # print(response)
    s = json.loads(response)
    ip_port = str(s['data'][0]["ip"]) + ":" + str(s['data'][0]["port"])
    return ip_port

def wandouip_http_one():
    url = 'http://api.wandoudl.com/api/ip?app_key=88a34462e4f758ee750dac2bf22ba6c6&pack=205555&num=1&xy=2&type=2&lb=\r\n&mr=1&'
    response = requests.get(url).content.decode()
    # print(response)
    s = json.loads(response)
    ip_port = str(s['data'][0]["ip"]) + ":" + str(s['data'][0]["port"])
    return ip_port


# ip_pool = json.loads(wandouip_ip_pool())
# for ip_ in ip_pool:
#     print(ip_)
#     response = requests.get("http://myip.ipip.net", proxies={
#                 'HTTPS': 'socks5://'+ip_}).content.decode()
#     print(response)
# response = requests.get("http://myip.ipip.net", proxies={'HTTPS': 'socks5://'+"27.194.134.228:4920"}).content.decode()
# print(response)

def zhimaruanjian_ip(n=20, z=0):
    url = 'http://http.tiqu.alicdns.com/getip3?num={}&type=2&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions='.format(
        n)
    response = requests.get(url).content.decode()
    # print(response)
    s = json.loads(response)
    pool = []
    if s['msg'] == '0':
        for i in s['data']:
            pool.append("http://"+str(i["ip"]) + ":" + str(i["port"]))
        return json.dumps(pool)
    else:
        if z <= 6:
            time.sleep(2)
            zhimaruanjian_ip(n, z + 1)
        else:
            return False

# s = zhimaruanjian_ip()
# print(s)
# s = wandouip_ip_pool()

# print(wandouip_ip_pool())