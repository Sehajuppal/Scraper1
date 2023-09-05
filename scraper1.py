import scrapy
import logging
import random


class MySpider(scrapy.Spider):
    name = "my_spider"
    
    # Specify the start URLs here
    start_urls = [
        'https://example.com',
    ]
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.get_headers())
    
    def parse(self, response):
        try:
            # Check if the response is successful
            if response.status == 200:
                # Extract data from the response using CSS selectors, XPath, or regex
                titles = response.css('.title::text').getall()
                descriptions = response.xpath('//div[@class="description"]/p/text()').getall()
                
                # Process the extracted data as needed (e.g., store in a database, write to a file)
                for title in titles:
                    self.log(f"Title: {title}", level=logging.INFO)
                    
                for description in descriptions:
                    self.log(f"Description: {description}", level=logging.INFO)
                
                # Follow links to other pages if needed
                # Example: yield response.follow(next_page_url, callback=self.parse, headers=self.get_headers())
                
            else:
                self.log(f"Failed to retrieve website data. Status code: {response.status}", level=logging.ERROR)
        
        except AttributeError as e:
            self.log(f"AttributeError: {str(e)}", level=logging.ERROR)
        
        except scrapy.SelectorError as e:
            self.log(f"SelectorError: {str(e)}", level=logging.ERROR)
        
        except scrapy.XPathError as e:
            self.log(f"XPathError: {str(e)}", level=logging.ERROR)
        
        except Exception as e:
            self.log(f"Error parsing response: {str(e)}", level=logging.ERROR)
    
    def get_headers(self):
        # Rotate user-agents to avoid detection
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
        ]
        
        headers = {
            'User-Agent': random.choice(user_agents)
        }
        
        return headers