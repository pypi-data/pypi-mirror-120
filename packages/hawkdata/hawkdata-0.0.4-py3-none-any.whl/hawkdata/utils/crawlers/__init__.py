from hawkdata.utils.crawlers import headers
USER_AGENT_LIST = headers.USER_AGENTS
REFERER_LIST = headers.REFERERS
SEC_CH_UA_LIST = headers.SEC_CH_UA

from hawkdata.utils.crawlers import web_crawler_base
WebCrawlerBase = web_crawler_base.WebCrawlerBase

from hawkdata.utils.crawlers import em_crawler
EmCrawler = em_crawler.EmCrawler
