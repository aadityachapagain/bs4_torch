import scrapy
import requests
from scrapy.selector import Selector


class DotaSpider(scrapy.Spider):
    name = 'Warcraft'
    start_urls = ['https://dota2.gamepedia.com/Heroes']

    def parse(self, response):
        loop = 0
        ability = ['Strength', 'Agility', 'Intelligence']
        value = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody')
        for heros in value.xpath('.//td'):
            for hero in heros.xpath('div'):
                yield {
                    'hero' : hero.xpath('.//div[1]/a/@title').extract(),
                    'img_link':hero.xpath('.//div[1]/a/img/@src').extract_first(),
                    'ability': ability[loop],
                    'bad_against': [*self.parse_bad_against(requests.get(f"https://dota2.gamepedia.com/{hero.xpath('.//div[1]/a/@title').extract_first().replace(' ','_')}/Counters"))],
                    'good_against': [*self.parse_good_against(requests.get(f"https://dota2.gamepedia.com/{hero.xpath('.//div[1]/a/@title').extract_first().replace(' ','_')}/Counters"))],
                    'work_well_with':[*self.parse_work_well_with(requests.get(f"https://dota2.gamepedia.com/{hero.xpath('.//div[1]/a/@title').extract_first().replace(' ','_')}/Counters"))],
                    'Roles':[*self.parse_roles(requests.get(f"https://dota2.gamepedia.com/{hero.xpath('.//div[1]/a/@title').extract_first().replace(' ','_')}"))]
                }
            loop = loop +1

    def parse_bad_against(self, response):
        select = Selector(response=response)
        starter = select.xpath('//*[@id="toc"]')
        for value in starter.xpath('.//following-sibling::*'):
            counter = value.xpath('.//span/@id').extract_first()
            if counter == 'Good_against...':
                break
            if value.xpath('.//b/a/text()').extract_first() is None:
                continue
            hero = value.xpath('.//b/a/text()').extract_first()
            pts = len(value.xpath('.//following-sibling::ul')[0].xpath('.//child::li'))
            yield {
                hero: pts
            }


    def parse_good_against(self,response):
        select = Selector(response=response)
        starter = select.xpath('//*[@id="mw-content-text"]/div/h2[2]')
        for value in starter.xpath('.//following-sibling::*'):
            counter = value.xpath('.//span/@id').extract_first()
            if counter == 'Works_well_with...':
                break
            if value.xpath('.//b/a/text()').extract_first() is None:
                continue
            hero = value.xpath('.//b/a/text()').extract_first()
            pts = len(value.xpath('.//following-sibling::ul')[0].xpath('.//child::li'))
            yield {
                hero: pts
            }


    def parse_work_well_with(self,response):
        select = Selector(response=response)
        starter = select.xpath('//*[@id="mw-content-text"]/div/h2[3]')
        for value in starter.xpath('.//following-sibling::*'):
            if value.xpath('.//b/a/text()').extract_first() is None:
                continue
            yield value.xpath('.//b/a/text()').extract_first()


    def parse_roles(self,response):
        select = Selector(response=response)
        head = select.xpath('//*[@id="Gameplay"]/parent::*')
        table = head.xpath('.//following-sibling::table')

        for role in table.xpath('.//tbody/tr[2]/td/child::a[@title="Role"]'):
            yield role.xpath('text()').extract_first()