# -*- coding:utf-8 -*-

import base64

from fontTools.ttLib import TTFont
import requests
import re
from lxml import etree

num_list = ['.', '6', '9', '1', '4', '2', '5', '7', '0', '8', '3']
base_font_list = ['x', 'uniF523', 'uniE7F8', 'uniE324', 'uniF655', 'uniE5C2', 'uniE112', 'uniE9B5', 'uniE25C', 'uniE0DD', 'uniE043']
num = []
url = "http://piaofang.maoyan.com/?ver=normal"
# 爬取猫眼网站的请求头
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
    'refer': 'http://maoyan.com/',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'piaofang.maoyan.com'
}
fonts = {
    'Host': 'vfile.meituan.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:62.0) Gecko/20100101 Firefox/62.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'If-Modified-Since': 'Thu, 04 Mar 2019 10:35:12 GMT',
    'Cache-Control': 'max-age=0'
}


def generate_base(fontface):

    #fontface = "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"
    decode_fontface = base64.b64decode(fontface)

    with open("base.woff", 'wb') as f:
        f.write(decode_fontface)
    font = TTFont('base.woff')
    font.saveXML('base.xml')

    print("写入成功！")


def crawler():

    req = requests.get(url, headers=header)

    print("请求状态：{0}".format(req.status_code))

    data = req.text

    print(data)

    cmp = re.search(r'url\(data:application/font-woff;charset=utf-8;base64,(.*)\) format\("woff"\)', data).group(1)

    decode_fontface = base64.b64decode(cmp)

    with open("fontfamily.woff", 'wb') as f:
        f.write(decode_fontface)
    font = TTFont('fontfamily.woff')
    font.saveXML('font.xml')

    print("写入成功！")

    #data = data.encode('utf-8')

    # fontUrl = "http:" + cmp
    # print(fontUrl)
    # reqfont = requests.get(fontUrl, stream=True)
    #
    # print(reqfont.content)
    #
    # with open("fontfamily.woff", "wb") as pdf:
    #     for chunk in reqfont.iter_content(chunk_size=1024):
    #         if chunk:
    #             pdf.write(chunk)
    #
    # print("写入成功！")

    font = TTFont('fontfamily.woff')
    font.saveXML('font.xml')
    base = TTFont('base.woff')

    download_font_list = font['cmap'].tables[0].ttFont.getGlyphOrder()

    for i in range(1 , 12):
        download_font = font['glyf'][download_font_list[i]]
        for j in range(11):
            base_font = base['glyf'][base_font_list[j]]
            if download_font == base_font:
                num.append(num_list[j])
                download_font_list[i] = str(download_font_list[i].replace(str(download_font_list[i])[0:3],'&#x')).lower() + ";"
                break
    print(num)
    print(download_font_list)
    #download_font_list = download_font_list[2:]
    for i in range(2,len(download_font_list)):
        data = data.replace(str(download_font_list[i]), str(num[i-1]))

    resp = etree.HTML(data);

    #tbody1 = resp.xpath('/html/*div[@id="ticket_tbody"]')

    tbody = resp.xpath('//*[@id="ticket_tbody"]/ul')
    print(tbody)
    for ul in tbody:
        #print(etree.tostring(ul))
        name = ul.xpath('./li[1]/b/text()')[0]
        span = ul.xpath('./li[1]/em[1]/text()')[0]
        c2 = ul.xpath('./li[2]/b/i/text()')[0]

        print("%-30s" % name, "%-20s" % span, "%10s" % c2)

crawler()
#ttftoxml()
#generate_base()


