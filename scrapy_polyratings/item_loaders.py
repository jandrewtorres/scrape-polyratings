from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, MapCompose
from scrapy_polyratings.items import PolyratingsProfessor, PolyratingsReview
from datetime import datetime


def parse_first(x):
    return x.replace(',', "").split()[1]


def parse_last(x):
    return x.replace(',', "").split()[0]


def clean_whitespace(x):
    return ' '.join(x.split())


class ProfessorLoader(ItemLoader):
    default_item_class = PolyratingsProfessor()
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    first_name_in = MapCompose(parse_first, clean_whitespace)
    last_name_in = MapCompose(parse_last, clean_whitespace)
    department_in = MapCompose(
        clean_whitespace)


def extract_difficulty_rating(s):
    if 'N/A' in s:
        return None
    return s[33:]


def extract_overall_rating(s):
    if 'N/A' in s:
        return None
    return s[:4]


def extract_date_posted(s):
    return datetime.strptime(s, '%b %Y').strftime('%Y-%m-%d')


def extract_reason_taken(s):
    if 'Major' in s:
        return 'R'
    elif 'Support' in s:
        return 'S'
    return 'E'


class ReviewLoader(ItemLoader):
    default_item_class = PolyratingsReview
    default_input_processor = Identity()
    default_output_processor = TakeFirst()
    class_standing_in = MapCompose(clean_whitespace)
    content_in = MapCompose(clean_whitespace)
    class_name_in = MapCompose(clean_whitespace)
    rating_overall_in = MapCompose(extract_overall_rating)
    rating_difficulty_in = MapCompose(extract_difficulty_rating)
    reason_taking_in = MapCompose(clean_whitespace, extract_reason_taken)
    date_posted_in = MapCompose(clean_whitespace, extract_date_posted)
    grade_received_in = MapCompose(clean_whitespace)
