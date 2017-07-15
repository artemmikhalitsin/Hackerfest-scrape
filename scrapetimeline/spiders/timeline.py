import scrapy
import json

class TimelineSpider(scrapy.Spider):
    name = "timeline"

    def start_requests(self):
        urls = [
            'https://github.com/artemmikhalitsin'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'timeline.txt'
        counts = response.css('rect.day::attr(data-count)').extract()
        dates = response.css('rect.day::attr(data-date)').extract()
        with open(filename, 'w') as f:
            for i in range(0, len(dates)):
                result = 'Day: %s, Activity count: %s\n' % (dates[i], counts[i])
                f.write(result)
