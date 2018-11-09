# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy_polyratings.models import Professor, Review, db_connect, create_tables
from sqlalchemy.orm import sessionmaker


class ScrapyPolyratingsPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.session = sessionmaker(bind=engine)

    def insert_item(self, item):
        session = self.session()

        try:
            session.add(item)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def process_item(self, item, spider):
        self.insert_item(Professor(**item['professor']))
        for review in item['reviews']:
            self.insert_item(Review(**review))

        return item
