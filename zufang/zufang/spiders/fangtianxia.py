# -*- coding: utf-8 -*-
import scrapy,re
from zufang.items import NewHouseItem
from zufang.items import ESFHouseItem


class FangtianxiaSpider(scrapy.Spider):
    name = 'fangtianxia'
    allowed_domains = ['fang.com']
    start_urls = ['http://www.fang.com/SoufunFamily.htm']
    province = None

    def parse(self, response):
        trs = response.xpath("//div[@class='outCont']//tr")

        for tr in trs:



            # 省份
            province_td = tr.xpath("./td[2]")
            province_text = province_td.xpath(".//text()").get()
            province_text = re.sub(r'\s','',province_text)

            # 不爬取省份为其它的城市
            if province_text == '其它':
                continue
            # 如果某一行的省份为空，则使用上一行的省份名
            if province_text:
                self.province = province_text

            #           http://hf.fang.com/
            # 新房链接   http://hf.newhouse.fang.com/house/s/
            # 二手房链接 http://hf.esf.fang.com/

            city_links = tr.xpath("./td/a")
            for city_link in city_links:
                city_url = city_link.xpath("./@href").get()
                city = city_link.xpath("./text()").get()

                # 北京比较特殊，下面的方法处理北京得到的地址无效

                if 'bj.' in city_url:
                    newhouse_url = 'http://newhouse.fang.com/house/s/'
                    esf_url = 'http://esf.fang.com/'
                else:
                    # 构建新房的url链接
                    url_module = city_url.split('.',1)
                    # 协议头
                    scheme = url_module[0]      # http://hf
                    domain = url_module[1]      # fang.com/
                    # 拼接成新房链接
                    newhouse_url = scheme+'.newhouse.'+domain+'house/s/'

                    # 构建二手房的url链接
                    esf_url = scheme+'.esf.'+domain
                # print('新房链接：%s  二手房链接：%s'%(newhouse_url,esf_url))

                yield scrapy.Request(
                    url = newhouse_url,
                    callback=self.parse_newhouse,
                    meta={'info':(self.province, city)}
                )

                yield scrapy.Request(
                    url=esf_url,
                    callback=self.parse_esf,
                    meta={'info': (self.province, city)}
                )


    def parse_newhouse(self, response):
        province, city = response.meta['info']

        div_list = response.xpath("//div[@class='nl_con clearfix']/ul/li//div[@class='nlc_details']")
        for div in div_list:
            name = div.xpath(".//div[@class='nlcd_name']/a/text()").get().strip()
            # name = re.sub(r'\s','',name) 与 strip 方法作用相同

            price = ''.join(div.xpath("./div[@class='nhouse_price']//text()").getall())
            price = re.sub(r'\s|广告','',price)

            rooms = div.xpath(".//div[contains(@class, 'house_type')]/a/text()").getall()
            rooms = [i for i in rooms if '居' in i]

            # 字符串才能使用re.sub 所以先join
            area = ''.join(div.xpath(".//div[@class='house_type clearfix']/text()").getall())
            area = re.sub(r'\s|/|－','',area)

            address = div.xpath(".//div[@class='address']/a/@title").get()

            district = ''.join(div.xpath(".//div[@class='address']/a//text()").getall())
            district = re.sub(r'\n|\t','',district)
            district = district[district.index('[')+1:district.index(']')] if ']' in district else None

            sale = div.xpath(".//div[@class='fangyuan']/span/text()").get()

            # 详情页
            origin_url = div.xpath(".//div[@class='nlcd_name']/a/@href").get()
            origin_url = response.urljoin(origin_url)

            item = NewHouseItem(province=province,city=city,name=name,price=price,rooms=rooms,area=area,address=address,district=district,sale=sale,origin_url=origin_url)
            yield item

        next_url = response.xpath("//div[@class='page']//a[@class='next']/@href").get()

        if next_url is not None:
            # next_url = 'http://{}.newhouse.fang.com' + next_url
            yield scrapy.Request(
                url=response.urljoin(next_url),
                callback=self.parse_newhouse,
                meta={'info': (province,city)},
            )


    def parse_esf(self, response):

        province, city = response.meta['info']

        dl_list = response.xpath("//div[@class='shop_list shop_list_4']/dl")

        for dl in dl_list:
            rooms = None
            area = None
            floor = None
            toward = None
            year = None

            title = dl.xpath("./dd/h4/a/@title").get()

            origin_url = dl.xpath("./dd/h4/a/@href").get()
            # 补全网址
            origin_url = response.urljoin(origin_url)


            # room_info = ''.join(dl.xpath("./dd/p//text()").getall())
            # room_info = (re.sub(r'\s','',room_info))
            # 上面得到的时字符串 ，如果需要列表形式去遍历的话使用下面的方法
            room_info = dl.xpath("./dd/p[@class='tel_shop']//text()").getall()
            room_info = list(map(lambda x:(re.sub(r'\s|(\|)','',x)),room_info))
            # print(room_info)
            for room in room_info:
                if '室' in room:
                    rooms = room
                elif '㎡' in room:
                    area = room
                elif '层' in room:
                    floor = room
                elif '向' in room:
                    toward = room
                elif '年' in room:
                    year = room


            print(rooms,area,floor,toward,year)

            name = dl.xpath("./dd/p[@class='add_shop']/a/@title").get()

            address = dl.xpath("./dd/p[@class='add_shop']/span/text()").get()

            price = dl.xpath("./dd[@class='price_right']//text()").getall()
            # 可以使用替换实现插入的方法
            price = re.sub(r'\s','',''.join(price)).replace('万','万,')

            agent = dl.xpath("./dd/p[@class='tel_shop']/span[@class='people_name']/a/text()").get()


            item = ESFHouseItem(province=province,city=city,name=name,title=title,rooms=rooms,floor=floor,toward=toward,year=year,address=address,area=area,price=price,agent=agent,origin_url=origin_url)

            yield item

        content = response.xpath(".//div[@class='page_al']/p[last()-2]/a/text()").get()
        if content is not None and content != '首页':
            next_url = response.xpath(".//div[@class='page_al']/p[last()-2]/a/@href").get()
            next_url = response.urljoin(next_url)
            # print(city,content,next_url)

            # if next_url is not None
            yield scrapy.Request(
                url=next_url,
                callback=self.parse_esf,
                meta={'info':(province,city)}
            )



