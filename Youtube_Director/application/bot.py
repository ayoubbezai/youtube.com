import os
import time
import threading
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class BotVisitor:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        
    def visit(self, url):
        try:
            driver = webdriver.Chrome(options=self.chrome_options)
            driver.get(url) 
            time.sleep(1)
            driver.execute_script("localStorage.setItem('flag', 'shellmates{test}');")
            time.sleep(2)
            
            driver.quit()
            return True
        except Exception as e:
            print(f"Error during bot visit: {str(e)}")
            return False

bot_visitor = BotVisitor()

def visit_url(url):
    def task():
        bot_visitor.visit(url)
    
    # Run in a separate thread to avoid blocking
    thread = threading.Thread(target=task)
    thread.daemon = True
    thread.start()
    
    return True