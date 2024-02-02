import os
import requests
import re
import rich
from rich import print
import time
import json
import random

# 获取TOKEN    https://api.locyanfrp.cn/User/DoLogin?username=smallcreeper&password=wanghongjun1
# 创建隧道      https://api.locyanfrp.cn/Proxies/add?username=[用户名]&name=[隧道名]&ip=[内网地址]&type=[隧道类型]&lp=[本地端口]&rp=[远程端口]&ue=[是否加密]&uz=[是否压缩]&id=[服务器ID]&token=[登录token]
# 删除隧道      https://api.locyanfrp.cn/Proxies/remove?username=[用户名]&proxyid=[隧道ID]&token=[登录TOKEN]
# 获取服务器列表 https://api.locyanfrp.cn/Proxies/GetServerList
# 获取隧道列表   https://api.locyanfrp.cn/Proxies/GetProxiesList?username=smallcreeper&token=[登录TOKEN]
print('欢迎使用Frp Client [blue]Beta0.1[/blue]')
# time.sleep(0.3)
# print('2 | LoCyanFrp')
# print('当某个供应商使用时出现闪退请切换其他供应商')
# give = input('请选择Frp供应商:')
# if give == '1':
#     print('使用SakuraFrp API')
#     print('正在制作')
# elif give == '2':
print('使用LoCyanFrp API')
pwd = open('reponse/p','r').read()
un = open('reponse/u','r').read()
cl = open('reponse/sys','r').read()
if cl == '1':
    cls = 'cls'
elif cl == '2':
    cls = 'clear'
def get_list():
    # 获取服务器列表
    server = requests.get("https://api.locyanfrp.cn/Proxies/GetServerList")
    data = json.loads(server.text)
    for num in range(0, len(data)):
        id = data[num]['id']
        name = data[num]['name']
        ip = data[num]['ip']
        status = data[num]['status']
        no = num+1
        if status == '200':
            status = '正常'
        else:
            status = '错误'
        print('NO:'+str(no)+' | ID:' + str(id) + ' | ' + name + '[{ip}]'.format(ip=ip) + ' 响应情况:' + status)
def printer(text, delay: float = 0.22):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
if len(pwd) == 0 or len(un) == 0:
    print('使用Frp客户端前,请进行一些设置')
    time.sleep(0.5)
    print('1.', end='')
    time.sleep(0.3)
    printer('登录\n')
    un = input('用户名:')
    pwd = input('密码:')
    def get_token(un: str, pwd: str):
        get = requests.get("https://api.locyanfrp.cn/User/DoLogin?username={username}&password={password}".format(username=un, password=pwd))
        data = json.loads(get.text)
        token = data['token']
        print(data['message'])
        return token
    un_o = open('reponse/u','w').write(un)
    pwd_o = open('reponse/p','w').write(pwd)
    print('2.',end='')
    time.sleep(0.3)
    printer('您的系统是什么\n')
    print('1 | Windows')
    print('2 | Linux & Android')
    system = input('请输入序号:')
    if system == '1':
        sys_in = open('reponse/sys','w').write(system)
        print('设置完成')
        cls = 'cls'
    elif system == '2':
        sys_out = open('reponse/sys','w').write(system)
        print('设置完成')
        cls = 'clear'
    os.system(cls)
else:
    def get_token(un: str, pwd: str):
        # 获取token
        get = requests.get("https://api.locyanfrp.cn/User/DoLogin?username={username}&password={password}".format(username=un, password=pwd))
        data = json.loads(get.text)
        token = data['token']
        print(data['message'])
        return token
    get_bulletin = requests.get("https://javaminecraft.cn/frp.html")
    bulletin = get_bulletin.text
    pat = re.compile('<span class="gonggao">(.*?)</span>')
    bulletin = pat.findall(bulletin)
    print(bulletin)
    while True:
        print('1 | 创建隧道')
        print('2 | 删除隧道')
        print('3 | 运行frp')
        mode = input('请选择序号:')
        if mode == '1':
            os.system(cls)
            get_list()
            id = int(input('节点ID:'))
            name = input('隧道名[不能用中文]:')
            ip = input('本地IP:')
            port = input('本地端口:')
            long_port = input('远程端口[r=随机]:')
            if long_port == 'r':
                port = random.randint(2000,65555)
            zip = input('是否压缩[1=是,0=否]:')
            lock = input('是否加密[1=是,0=否;建议不加密]:')
            obj = input('穿透格式[1=TCP,2=UDP,3=HTTP,4=HTTPS]:')
            number = input('节点NO数:')
            if obj == '1':
                ini = 'tcp'
            elif obj == '2':
                ini = 'udp'
            elif obj == '3':
                ini = 'http'
            elif obj == '4':
                ini = 'https'
            get_ip = requests.get('https://api.locyanfrp.cn/Proxies/GetServerList')
            data = json.loads(get_ip.text)
            ip_c = data[int(number)]['ip']
            mk = '''[common]
server_addr = {ip}
server_port = 2333
tcp_mux = true;protocol = tcp
user = 9af0bc14a0e2ab797f19fe4b02842b3d
token = LoCyanToken
dns_server = 223.6.6.6
tls_enable = false

[{name}]
privilege_mode = true
type = {obj}
local_ip = {ip_frp}
local_port = {port_frp}
remote_port = {long}
            '''.format(name=name,obj=ini,long=long_port,ip_frp=ip,port_frp=port,ip=ip_c)
            print(mk)
            try:
                get = requests.get(
                    "https://api.locyanfrp.cn/User/DoLogin?username={username}&password={password}".format(username=un,
                                                                                                           password=pwd))
                data = json.loads(get.text)
                token = data['token']
                print(data['message'])
                create = requests.get('https://api.locyanfrp.cn/Proxies/add?username={username}&name={name}&ip={ip}&type={obj}&lp={port}'
                                      '&rp={long_port}&ue={lock}&uz={zip}&id={id}&token={token}'
                                      .format(username=un,name=name,ip=ip,obj=obj,port=port,long_port=long_port,lock=lock,id=id,zip=zip,token=token))
                print('隧道创建成功')
            except:
                print('隧道创建失败')
            os.system(cls)
        if mode == '2':
            os.system(cls)
            print('正在获取隧道列表...')
            get = requests.get(
                "https://api.locyanfrp.cn/User/DoLogin?username={username}&password={password}".format(username=un,
                                                                                                       password=pwd))
            data = json.loads(get.text)
            token = data['token']
            print(data['message'])
            proxies = requests.get('https://api.locyanfrp.cn/Proxies/GetProxiesList?username=smallcreeper&token={token}'.format(token=token))
            proxies = json.loads(proxies.text)
            proxies = proxies['proxies']
            for i in range(0,len(proxies)):
                print('ID: ' + str(proxies[i]['id'])+' | 名称: ' + proxies[i]['proxy_name']+'  本地端口:'+str(proxies[i]['local_port']))
            de = str(input('请输入需要删除的隧道ID[exit=退出]:'))
            delete = requests.get('https://api.locyanfrp.cn/Proxies/remove?username={username}&proxyid={proxy_id}&token={token}'.format(username=un,proxy_id=de,token=token))
            delete = json.loads(delete.text)
            print('[green]'+delete['message']+'[/green]')
            os.system(cls)
        if mode == '3':
            start = input('即将运行命令行.按回车继续,输n退出')
            if start == '' or start == '\n':
                time.sleep(1)
                print(open('frpc.ini','r').read())
                os.system('frpc.exe -c frpc.ini')
        else:
            break