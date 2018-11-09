from scrapy.spiders import CrawlSpider, Rule
from scrapy_polyratings.items import PolyratingsProfessor, PolyratingsReview
from scrapy.linkextractors import LinkExtractor
from scrapy_polyratings.item_loaders import ProfessorLoader, ReviewLoader


class PolyratingsSpider(CrawlSpider):
    name = "polyratings"
    allowed_domains = ["polyratings.com"]
    start_urls = ["http://www.polyratings.com/list.php"]

    pid_count = 1
    rid_count = 1

    rules = {
        Rule(LinkExtractor(allow=('/eval\.php\?profid')),
             callback='parse_professor',
             follow=True),
    }

    def parse_professor(self, response):
        prof_loader = ProfessorLoader(
            item=PolyratingsProfessor(), response=response)
        prof_loader.add_value('pid', self.pid_count)
        self.pid_count += 1
        prof_loader.add_xpath(
            'first_name', '/html/body/div[1]/div[2]/div/div/h1/strong/text()')
        prof_loader.add_xpath(
            'last_name', '/html/body/div[1]/div[2]/div/div/h1/strong/text()')
        prof_loader.add_xpath(
            'department', '/html/body/div[1]/div[2]/div/div/h4[2]/text()')
        rating_difficulty = response.xpath(
            '/html/body/div[1]/div[3]/span/b[2]/text()').extract_first()
        rating_overall = response.xpath(
            '/html/body/div[1]/div[3]/span/h2/text()').extract_first()
        reviews = []
        for class_group in response.xpath('/html/body/center/div/div/section'):
            class_name = class_group.xpath('./h2/text()').extract_first()

            for review_group in class_group.xpath('./div'):
                review_loader = ReviewLoader(
                    item=PolyratingsReview(), selector=review_group)
                review_loader.add_value('pid', self.pid_count - 1)
                review_loader.add_value('rid', self.rid_count)
                self.rid_count += 1
                review_loader.add_value('class_name', class_name)
                review_loader.add_xpath(
                    'class_standing', './div/div[1]/text()[1]')
                review_loader.add_xpath(
                    'grade_received', './div/div[1]/text()[2]')
                review_loader.add_xpath(
                    'reason_taking', './div/div[1]/text()[3]')
                review_loader.add_xpath(
                    'date_posted', './div/div[1]/text()[4]')
                review_loader.add_value('rating_difficulty', rating_difficulty)
                review_loader.add_value('rating_overall', rating_overall)
                review_loader.add_xpath('content', './div/div[2]/text()')
                reviews.append(review_loader.load_item())

        yield {'professor': prof_loader.load_item(), 'reviews': reviews}
