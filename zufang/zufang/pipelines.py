# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exporters import JsonLinesItemExporter
from zufang.items import NewHouseItem
from zufang.items import ESFHouseItem

class ZufangPipeline(object):
    def __init__(self):
        self.newhouse_fb = open('newhouse.json','wb')
        self.esfhouse_fb = open('esfhouse.json','wb')
        self.newhouse_exporter = JsonLinesItemExporter(self.newhouse_fb, ensure_ascii=False)
        self.esfhouse_exporter = JsonLinesItemExporter(self.esfhouse_fb, ensure_ascii=False)


    def process_item(self, item, spider):
        if isinstance(item, NewHouseItem):
            self.newhouse_exporter.export_item(item)
        elif isinstance(item, ESFHouseItem):
            self.esfhouse_exporter.export_item(item)
        return item


