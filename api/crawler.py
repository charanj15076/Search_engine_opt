import logging
import bs4, tldextract
import datetime, time
import glob, os, re, sys

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import Options
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


    def extract_all_links(self, url, depth):
        """
        Grab all the URLs in a website
        Limited by the depth/how deep the crawler searches the site
        Returns a list of URLs
        """
        
        # get access to driver
        driver = self.driver

        timeout_delay = self.timeout_delay
        driver.set_page_load_timeout(timeout_delay)

        try:
            self.logger.info('Accessing ' + url + '...')
            driver.set_page_load_timeout(10)
            try:
                driver.get(url)
            except TimeoutException:
                # pages may need to be manually stopped after loading for too long
                # the DOM is actually ready but some hung up javascript may be forcing it to load indefinitely
                self.logger.info('Page has been loading for a long time. Interrupting the page load...')
                driver.execute_script('window.stop();')
            html_page = driver.page_source
            soup = bs4.BeautifulSoup(html_page, 'html.parser')
        except Exception:
            self.logger.error('An error occurred while trying to access ' + url)
            driver.quit()
            raise
        finally:
            driver.save_screenshot('/screenshots/img.png')

        ext = tldextract.extract(driver.current_url)
        urlp = urlparse(driver.current_url)
        base_url = urlp.scheme + '://' + urlp.netloc
        full_domain = ext.domain + '.' + ext.suffix
        self.logger.info('Current URL: ' + driver.current_url)
        self.logger.info('Base URL: ' + base_url)
        self.logger.info('Domain: ' + full_domain)

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
                elif full_domain not in driver.current_url:
                    if driver.current_url in href and driver.current_url != href:
                        links.append(href)
                elif full_domain in href:
                    if not href.endswith(full_domain) and not href.endswith(full_domain + '/'):
                        links.append(href)
                elif not href.startswith('http') and not href.startswith('javascript') and href != '':
                    # for relative path schemes that do not start with '/'
                    if href[0].isalnum():
                        links.append(base_url + '/' + href)

        return links

    
    def run(self):
        self.logger.info('RUNNING: Crawler')
        
        # initialize
        with Display(visible=0, size=(1920, 1080)):

            # configure webdriver profile
            options = Options()
            
            # profile = webdriver.FirefoxProfile()
            # profile.set_preference('general.useragent.override', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0')
            # # speeding up load time by disabling js, css, images, etc
            # profile.set_preference('permissions.default.stylesheet', 2)
            # profile.set_preference('permissions.default.image', 2)
            # profile.set_preference('javascript.enabled', False)
            # profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so','false')
            # caps = DesiredCapabilities.FIREFOX.copy()

            # access site
            driver = webdriver.Firefox(options=options)
            driver.maximize_window()

            self.driver = driver

            links = self.extract_all_links(self.site, 1)
            num_links = len(links)
            self.logger.info(links)
            
            self.logger.info('Site Internal Links Count: ' + str(num_links))

            driver.quit()

        return links


test = Crawler("www.google.com").run()