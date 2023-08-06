import urllib 
#import urllib2 
import requests
def download(filepath,savepath):
    print("downloading with urllib")
    url = 'http://***/test/demo.zip' 
    print("downloading with urllib")
    urllib.urlretrieve(url, "demo.zip")