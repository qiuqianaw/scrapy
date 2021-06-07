from scrapy.cmdline import execute

import sys
import os

# 当前文件的绝对路径
# print(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'jobbole'])