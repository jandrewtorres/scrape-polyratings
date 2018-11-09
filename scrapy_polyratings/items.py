# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class PolyratingsProfessor(Item):
    """ Polyratings container for scraped data """
    pid = Field()
    first_name = Field()
    last_name = Field()
    reviews = Field()
    department = Field()


class PolyratingsReview(Item):
    """ Polyratings container for scraped data """
    rid = Field()
    pid = Field()
    content = Field()
    class_name = Field()
    rating_overall = Field()
    rating_difficulty = Field()
    reason_taking = Field()
    date_posted = Field()
    grade_received = Field()
    class_standing = Field()
