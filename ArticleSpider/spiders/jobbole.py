import scrapy
import undetected_chromedriver
from scrapy import Request
from urllib import parse


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']
    custom_settings = {
        'COOKIES_ENABLE': True
    }

    def start_requests(self):
        import undetected_chromedriver.v2 as uc
        browser = uc.Chrome()
        browser.get('https://account.cnblogs.com/signin')
        input('回车继续：')
        cookies = browser.get_cookies()
        cookie_dic = {}
        for cookie in cookies:
            cookie_dic[cookie['name']] = cookie['value']
        for url in self.start_urls:
            headers = {
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
            }
            yield scrapy.Request(url, cookies=cookie_dic, headers=headers, dont_filter=True)

    def parse(self, response):
        # 获取新闻列表页中的url并交给scrapy进行下载后调用相应的解析方法
        # 获取下一页url，并交给scrapy进行下载，下载完成后交给parse继续跟进
        # urls = response.css('div#news_list h2 a::attr(href)').extract()
        post_nodes = response.css('#news_list .news_block').extract()
        for post_node in post_nodes:
            image_url = post_node.css('.entry_summary a img::attr(href)').extract_first('')
            post_url = post_node.css('h2 a::attr(href)').extract_first('')
            yield Request(url=parse.urljoin(response.url, post_url), meta={'font_image_url': image_url},
                          callback=self.parse_detai)

    def parse_detail(self, response):
        pass
