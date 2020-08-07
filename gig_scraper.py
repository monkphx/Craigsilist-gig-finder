from bs4 import BeautifulSoup
import requests
from random_useragent.random_useragent import Randomize
from stem import process
import os
import requests
from random import randint
import bs4
from torrequest import TorRequest
from stem import Signal
from stem.control import Controller
import email2
import smtplib
import pandas as pd
import time 
import datetime

def start_tor():
	loc=os.getcwd()
	loc2=loc+'\\Tor\\tor.exe'
	loc3=loc+"\\Tor\\torrc"
	DEFAULT_INIT_TIMEOUT = 90
	tor_process=process.launch_tor(tor_cmd =loc2,torrc_path=loc3)
	return(tor_process)
	
def _set_new_ip():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='rastafari')
        controller.signal(Signal.NEWNYM)

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        _set_new_ip()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log('Proxy : %s' % request.meta['proxy'])

def user_a():
    m=randint(0,6)
    agents=[]
    # Get aspect ratio list.
    r_agent = Randomize()
    r_agent.get_aspect_ratio_list() # returns ['3:2', '4:3', '5:3', '5:4', '16:9', '16:10'].
  

    
    # Takes 2 arguments (self, aspect_ratio).
    r_agent.random_resolution('3:2') # returns screen resolution.
    
    # Takes 3 arguments (self, device_type, os)
    agents.append(r_agent.random_agent('desktop','linux')) # returns 'Desktop / Linux'
    agents.append(r_agent.random_agent('desktop','mac')) # returns 'Desktop / Linux'
    agents.append(r_agent.random_agent('desktop','windows')) # returns 'Desktop / Macintosh'

    agents.append(r_agent.random_agent('tablet','android')) # returns 'Tablet / Android'
    agents.append(r_agent.random_agent('tablet','ios')) # returns 'Tablet / iOS'

    agents.append(r_agent.random_agent('smartphone','android')) # returns 'Smartphone / Android'
    agents.append(r_agent.random_agent('tablet','ios')) # returns 'Smartphone / iOS'
    return(agents[m])



def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


	
def craigslist_gig_scrape(v):
	
	hed={'User-Agent':user_a()}
	#The ip is reset before the request is called
	_set_new_ip()  
	#untraceable tor session is requested
	session=get_tor_session()
	#the link we will scrape
	link="https://geo.craigslist.org/iso/us"
	res=session.get(link,headers=hed)
	soup=bs4.BeautifulSoup(res.text,'html')
	Elements=soup.find_all("p","result-info")
	link_list = [a['href'] for a in soup.find_all('a', href=True)]
	text = [a.text for a in soup.find_all('a', href=True)]
	dat={ 'links':link_list,
         'titles':text,       }
	df = pd.DataFrame(dat)
	df.drop(df.tail(10).index,inplace=True)
	df.drop(df.head(5).index,inplace=True)
	links2=[]
	titles2=[]
	c=0
	for f in df["links"]:
		c=c+1
		try:
			if "www" not in f:
				links2.append(f+v)
				titles2.append(df["titles"].iloc[c])
		except :
			print("error")
	links2.pop(0)        
	print(len(titles2))
	print(len(links2))  
	dat={ 'links':links2,
			 'titles':titles2, }
	df2 = pd.DataFrame(dat)
	ls=[]
	ts=[]
	ds=[]
	post_links=[]
	post_titles=[]
	place=[]
	dates=[]
	timestamps=[]
	c=0
	for f in df2['links']:
		try:
			res=session.get(f,headers=hed)
			soup=bs4.BeautifulSoup(res.text,'html')
			Elements=soup.findAll("p","result-info")
			
			for element in Elements:
				post_links.append(element.find("a",'result-title hdrlnk')['href'])
				post_titles.append(element.find("a",'result-title hdrlnk').get_text())
				place.append(df2['titles'].iloc[c])
				dates.append(element.find("time",'result-date').get_text())
				s=element.find("time",'result-date').get_text()
				s=s.replace("Jun ","6/")
				s=s.replace("Jul ","7/")
				s=s.replace("Aug ","8/")
				s=s.replace("Sep ","9/")
				s=s.replace("Oct ","10/")
				now = datetime.datetime.now()
				s=s+"/"+str(now.year)
				t=time.mktime(datetime.datetime.strptime(s, "%m/%d/%Y").timetuple())            
				timestamps.append(t)
		except TypeError: 
			print("eerror")
		c=c+1

	dat={ 'links':post_links,
			 'titles':post_titles,   
		'place':place,
		'date':dates,
		'timestamp':timestamps}
	df3 = pd.DataFrame(dat)
	df3=df3.drop_duplicates(subset=['links'],keep="first")

	return(df3)