import logging
import bs4, tldextract
import datetime, time
import glob, os, re, sys
import uuid

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from urllib.parse import urlparse


class Crawler:
    site = ''
    logger = None
    timeout_delay = 10  # default to 10 seconds

    def __init__(self, site):
        self.site = site

        # initialize logger, use stdout by default (if no log file provided)
        # this can be overridden when called with the proper handlers
        if not self.logger:
            default_logger = logging.getLogger(__name__)
            default_logger.setLevel(logging.DEBUG)
            sh = logging.StreamHandler()
            default_logger.addHandler(sh)
            self.logger = default_logger


    def extract_links(self, source):
        """
        Grab all the internal URLs in a website
        Returns a list of URLs
        """
        
        soup = bs4.BeautifulSoup(source, 'html.parser')
        
        # get the base url
        ext = tldextract.extract(self.driver.current_url)
        urlp = urlparse(self.driver.current_url)
        base_url = urlp.scheme + '://' + urlp.netloc
        full_domain = ext.domain + '.' + ext.suffix

        self.logger.info('Current URL: ' + self.driver.current_url)
        self.logger.info('Base URL: ' + base_url)
        self.logger.info('Domain: ' + full_domain)

        # gather all the internal links
        # build them properly to their full absolute path because some are use relative linking
        self.logger.info('Gathering internal links...')
        links = []
        for link in soup.findAll('a'):
            href = link.get('href')
            if not href == None:
                # different conditions to consider a parseable link
                if href.startswith('/'):
                    if href.startswith('//'):
                        links.append(urlp.scheme + ':' + href)
                    elif not href == '/':
                        links.append(base_url + href)
                elif full_domain not in self.driver.current_url:
                    if self.driver.current_url in href and self.driver.current_url != href:
                        links.append(href)
                elif full_domain in href:
                    if not href.endswith(full_domain) and not href.endswith(full_domain + '/'):
                        links.append(href)
                elif not href.startswith('http') and not href.startswith('javascript') and href != '':
                    # for relative path schemes that do not start with '/'
                    if href[0].isalnum():
                        links.append(base_url + '/' + href)

        num_links = len(links)
        self.logger.info(links)
        self.logger.info('Site Internal Links Count: ' + str(num_links))

        return links


    def extract_text(self, source):
        """
        Grab all the text from a given website
        Returns a list of strings
        """

        soup = bs4.BeautifulSoup(source, 'html.parser')

        return soup.get_text(' ', strip=True)

    
    def run(self, site):
        self.logger.info('RUNNING: Crawler')
        self.site = site
        
        # initialize
        with Display(visible=0, size=(1920, 1080)):

            # configure webdriver profile
            options = Options()

            options.log.level = "trace"
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            
            profile = FirefoxProfile()
            profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:87.0) Gecko/20100101 Firefox/87.0')
            
            # speeding up load time by disabling js, css, images, etc
            # profile.set_preference('permissions.default.stylesheet', 2)
            # profile.set_preference('permissions.default.image', 2)
            # profile.set_preference('javascript.enabled', False)
            profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')

            options.profile = profile
            
            service = Service()

            # start firefox
            self.driver = webdriver.Firefox(service=service, options=options)
            self.driver.maximize_window()
            self.driver.implicitly_wait(7)
            self.driver.set_page_load_timeout(self.timeout_delay)
            
            # access site
            try:
                self.logger.info('Accessing ' + self.site + '...')
                self.driver.set_page_load_timeout(10)

                try:
                    self.driver.get(self.site)
                except TimeoutException:
                    # pages may need to be manually stopped after loading for too long
                    # the DOM is actually ready but some hung up javascript may be forcing it to load indefinitely
                    self.logger.info('Page has been loading for a long time. Interrupting the page load...')
                    self.driver.execute_script('window.stop();')
                
            except Exception:
                self.logger.error('An error occurred while trying to access ' + self.site)
                self.driver.quit()
                raise
            finally:
                img_name = str(uuid.uuid4().hex) + '.png'
                img_path = './api/static/' + img_name
                self.driver.save_screenshot(img_path)

            links = self.extract_links(self.driver.page_source)
            text = self.extract_text(self.driver.page_source)  

            self.logger.info(text)

            self.driver.quit()

        return links, text, img_name


