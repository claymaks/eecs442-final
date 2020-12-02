import os
import time
import requests

from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager


nike_urls = {
    "mens": {
        "lifestyle": "https://www.nike.com/w/mens-lifestyle-shoes-13jrmznik1zy7ok",
        "jordan": "https://www.nike.com/w/mens-jordan-shoes-37eefznik1zy7ok",
        "running": "https://www.nike.com/w/mens-running-shoes-37v7jznik1zy7ok",
        "basketball": "https://www.nike.com/w/mens-basketball-shoes-3glsmznik1zy7ok",
        "football": "https://www.nike.com/w/mens-football-shoes-3hj8mznik1zy7ok",
        "soccer": "https://www.nike.com/w/mens-soccer-shoes-1gdj0znik1zy7ok",
        "training&gym": "https://www.nike.com/w/mens-training-gym-shoes-58jtoznik1zy7ok",
        "skateboarding": "https://www.nike.com/w/mens-skateboarding-shoes-8mfrfznik1zy7ok",
        "baseball": "https://www.nike.com/w/mens-baseball-shoes-99fchznik1zy7ok",
        "golf": "https://www.nike.com/w/mens-golf-shoes-23q9wznik1zy7ok",
        "tennis": "https://www.nike.com/w/mens-tennis-shoes-ed1qznik1zy7ok",
        "track&field": "https://www.nike.com/w/mens-track-field-shoes-7nem3znik1zy7ok",
        "walking": "https://www.nike.com/w/mens-walking-shoes-b3e0kznik1zy7ok",
    },
    "womens": {
        "lifestyle": "https://www.nike.com/w/womens-lifestyle-shoes-13jrmz5e1x6zy7ok",
        "running": "https://www.nike.com/w/womens-running-shoes-37v7jz5e1x6zy7ok",
        "basketball": "https://www.nike.com/w/womens-basketball-shoes-3glsmz5e1x6zy7ok",
        "soccer": "https://www.nike.com/w/womens-soccer-shoes-1gdj0z5e1x6zy7ok",
        "training&gym": "https://www.nike.com/w/womens-training-gym-shoes-58jtoz5e1x6zy7ok",
        "jordan": "https://www.nike.com/w/womens-jordan-shoes-37eefz5e1x6zy7ok",
        "skateboarding": "https://www.nike.com/w/womens-skateboarding-shoes-5e1x6z8mfrfzy7ok",
        "softball": "https://www.nike.com/w/womens-softball-shoes-2dlpvz5e1x6zy7ok",
        "golf": "https://www.nike.com/w/womens-golf-shoes-23q9wz5e1x6zy7ok",
        "tennis": "https://www.nike.com/w/womens-tennis-shoes-5e1x6zed1qzy7ok",
        "track&field": "https://www.nike.com/w/womens-track-field-shoes-5e1x6z7nem3zy7ok",
        "volleyball": "https://www.nike.com/w/womens-volleyball-shoes-5e1x6ztc2uzy7ok",
        "cheerleading": "https://www.nike.com/w/womens-cheerleading-shoes-1cyjkz5e1x6zy7ok",
        "walking": "https://www.nike.com/w/womens-walking-shoes-5e1x6zb3e0kzy7ok",
    }
}

adidas_urls = {
    "mens": {
        "lifestyle": "https://www.adidas.com/us/men-lifestyle-athletic_sneakers-shoes",
        "running": "https://www.adidas.com/us/men-running-athletic_sneakers-shoes",
        "basketball": "https://www.adidas.com/us/men-basketball-athletic_sneakers-shoes",
        "skateboarding": "https://www.adidas.com/us/men-skateboarding-athletic_sneakers-shoes",
        "training": "https://www.adidas.com/us/men-training-athletic_sneakers-shoes",
        "soccer": "https://www.adidas.com/us/men-soccer-athletic_sneakers-shoes",
        "baseball": "https://www.adidas.com/us/men-baseball-athletic_sneakers-shoes", 
    },
    "womens": {
        "lifestyle": "https://www.adidas.com/us/women-lifestyle-shoes",
        "running": "https://www.adidas.com/us/women-running-shoes",
        "basketball": "https://www.adidas.com/us/women-basketball-shoes",
        "soccer": "https://www.adidas.com/us/women-soccer-shoes",
        "golf": "https://www.adidas.com/us/women-golf-shoes",
        "training": "https://www.adidas.com/us/women-training-shoes"
    }
}

puma_urls = {
    "mens": {
        "classics": "https://us.puma.com/en/us/men/shoes/classics",
        "lifestyle": "https://us.puma.com/en/us/men/shoes/lifestyle",
        "training&gym": "https://us.puma.com/en/us/men/shoes/training-%2B-gym",                
        "running": "https://us.puma.com/en/us/men/shoes/running",
        "motorsport": "https://us.puma.com/en/us/men/shoes/motorsport",
        "performance_basketball": "https://us.puma.com/en/us/men/shoes/performance-basketball",
        "heritage_basketball": "https://us.puma.com/en/us/men/shoes/heritage-basketball",
        "soccer": "https://us.puma.com/en/us/men/shoes/soccer",
    },
    "womens": {
        "classics": "https://us.puma.com/en/us/women/shoes/classics",
        "lifestyle": "https://us.puma.com/en/us/women/shoes/lifestyle",
        "training&gym": "https://us.puma.com/en/us/women/shoes/training-%2B-gym",                
        "running": "https://us.puma.com/en/us/women/shoes/running",
        "performance_basketball": "https://us.puma.com/en/us/women/shoes/performance-basketball",
        "heritage_basketball": "https://us.puma.com/en/us/women/shoes/heritage-basketball",
    }
}

ua_urls = {
    "mens": {
        "training": "https://www.underarmour.com/en-us/c/mens/shoes/training/",
        "running": "https://www.underarmour.com/en-us/c/mens/shoes/running/",
        "baseball": "https://www.underarmour.com/en-us/c/mens/shoes/baseball/",
        "basketball": "https://www.underarmour.com/en-us/c/mens/shoes/basketball/",
        "football": "https://www.underarmour.com/en-us/c/mens/shoes/football/",
        "golf": "https://www.underarmour.com/en-us/c/mens/shoes/golf/",
        "soccer": "https://www.underarmour.com/en-us/c/mens/shoes/soccer/",
        "lacrosse": "https://www.underarmour.com/en-us/c/mens/shoes/lacrosse/",
    },
    "womens": {
        "training": "https://www.underarmour.com/en-us/c/womens/shoes/training/",
        "running": "https://www.underarmour.com/en-us/c/womens/shoes/running/",
        "basketball": "https://www.underarmour.com/en-us/c/womens/shoes/basketball/",
        "golf": "https://www.underarmour.com/en-us/c/womens/shoes/golf/",
        "soccer": "https://www.adidas.com/us/women-soccer-shoes",
        "softball": "https://www.underarmour.com/en-us/c/womens/shoes/softball/",
        "lacrosse": "https://www.underarmour.com/en-us/c/womens/shoes/lacrosse/",
        "volleyball": "https://www.underarmour.com/en-us/c/womens/shoes/volleyball/",
    }
}



chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-sh-usage')
chrome_options.add_argument('--no-sandbox')

class ImageScraper(object):
    def __init__(self, urls: {}, name="", file=None, parse=lambda x: lambda y: True):
        self.browser = webdriver.Chrome(ChromeDriverManager().install())
        self.image_urls = []
        self.urls = urls
        self.name = name
        self.cache = []
        self.parse = parse(self.name)
        
        dirname = os.path.dirname(__file__)
        # brand, sex, class, url
        self.log_string = "{},{},{},{}"
        if not file:
            self.file = open(os.path.join(dirname, f"images/{self.name}_urls_{int(time.time())}.csv"), "a+")
        else:
            self.file = open(file, "a+")
        

    def scrape(self):
        print(f"{self.name}:")
        for sex, classes in self.urls.items():
            print(f"\t{sex}:")
            for class_, url in classes.items():
                print(f"\t\t{class_}:")
                self.browser.get(url)
                print("\t\t\twaiting 3 seconds...")
                time.sleep(5)
                print("\t\t\t\tcontinuing")
                html = self.browser.page_source
                soup = bs(html, 'html.parser')
                if self.name == "nike":
                    sources = soup.find_all('source')
                    image_tag = 'srcset'
                elif self.name in ["adidas", "puma", "underarmor"]:
                    sources = soup.find_all('img')
                    image_tag = 'src'
                print(f"\t\t\t{len(sources)}")
                elim = 0
                null = 0
                bad = 0
                parsed = 0
                
                for source in sources:
                    if not source:
                        null += 1
                        continue
                    elif image_tag not in source.attrs:
                        bad += 1
                        continue
                    elif source[image_tag].split('/')[-1] in self.image_urls:
                        elim += 1
                        continue
                    elif not self.parse(source[image_tag]):
                        parsed += 1
                        continue
                    self.image_urls.append(source[image_tag].split('/')[-1])
                    print(self.log_string.format(
                        self.name, sex, class_, source[image_tag]), file=self.file)
                print(f"\t\t\tremoved {elim} duplicates, {null} nulls, {bad} bads, {parsed} parsed...")
                print(f"\t\t\taccepted: {len(sources) - (elim + null + bad + parsed)}")
        print(f"{len(self.image_urls)} images logged")
        self.file.close()

        
def remove_non_prod(name):
    def adidas(url):
        return "https://assets.adidas.com/images" in url
    def puma(url):
        return "https://images.puma.com/image/" in url
    def ua(url):
        return "https://underarmour.scene7.com/is/image/" in url
    
    if name == "adidas":
        return adidas
    elif name == "puma":
        return puma
    elif name == "underarmor":
        return ua

    return lambda x: True


if __name__ == "__main__":
    Nike = ImageScraper(nike_urls, name="nike")
    Nike.scrape()
    Adidas = ImageScraper(adidas_urls, name="adidas", parse=remove_non_prod)
    Adidas.scrape()
    # Puma = ImageScraper(puma_urls, name="puma", parse=remove_non_prod)
    # Puma.scrape()
    UA = ImageScraper(ua_urls, name="underarmor", parse=remove_non_prod)
    UA.scrape()
