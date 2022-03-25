import os
import sys
import argparse
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options

helptext = 'WebGrabber'

parser = argparse.ArgumentParser(description=helptext)

parser.add_argument("--list", "-l", help="file list of domains to run WebGrabber against", required=True)
parser.add_argument("--driver", "-d", help="/path/to/chromedriver", required=True)
parser.add_argument("--browser", "-b", help="/path/to/chrome", required=True)
parser.add_argument("--out", "-o", help='output directory (default output/, will be created if it does not exist)')
parser.add_argument("--verbose", "-v", help="enable verbose output")
args = parser.parse_args()

CHROME_PATH = args.browser
CHROMEDRIVER_PATH = args.driver
WINDOW_SIZE = "1920,1080"

if not args.out:
    args.out = "output"

chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument("--test-type")
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.binary_location = CHROME_PATH

print(f"Starting WebGrabber on {args.list}")
driver = webdriver.Chrome(
    executable_path=CHROMEDRIVER_PATH,
    chrome_options=chrome_options
)  

if not os.path.exists(args.out):
    os.makedirs(args.out)

with open(args.list) as list:
   for domain in list:
        # http screenshot
        if (args.verbose):
            print(f"Making HTTP request to http://{domain}...")
        try:
            driver.get(f"http://{domain}/")
        except Exception as e:
            if (args.verbose):
                print(e)
        driver.save_screenshot(f"{args.out}/{domain}-HTTP.png")
        # http screenshot
        if (args.verbose):
            print(f"Making HTTPS request to https://{domain}...")
        try:
            driver.get(f"https://{domain}/")
        except Exception as e:
            if (args.verbose):
                print(e)
        driver.save_screenshot(f"{args.out}/{domain}-HTTPS.png")


driver.close()
print(f"Finished WebGrabber on {args.list}")
        

