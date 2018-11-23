import scrapy

class DotaSpider(scrapy.Spider):
    name = 'Warcraft'
    start_urls = ['https://dota2.gamepedia.com/Heroes']

    def parse(self,response):
        loop = 0
        ability = ['Strength','Agility','Intelligence']
        value = response.xpath('//*[@id="mw-content-text"]/div/table[1]/tbody')
        for heros in value.xpath('.//td'):
            for hero in heros.xpath('div'):
                yield {
                    'hero' : hero.xpath('.//div[1]/a/@title').extract(),
                    'ability': ability[loop],
                    'counters': scrapy.Request(url=f"https://dota2.gamepedia.com/{hero.xpath('.//div[1]/a/@title').extract().replace(' ','_')}/Counters",
                                               callback=self.parse_counter)
                }
            loop = loop +1

    def parse_counter(self,response):
        pass
