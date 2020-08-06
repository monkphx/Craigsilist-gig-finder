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
from stem import process
import os
import streamlit as st


def start_tor():
    try:
        loc = os.getcwd()
        loc2 = loc + '\\Tor\\tor.exe'
        loc3 = loc + "\\Tor\\torrc"
        DEFAULT_INIT_TIMEOUT = 90
        tor_process = process.launch_tor(tor_cmd=loc2, torrc_path=loc3)
    except OSError:
        pass


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
    m = randint(0, 6)
    agents = []
    # Get aspect ratio list.
    r_agent = Randomize()
    r_agent.get_aspect_ratio_list()  # returns ['3:2', '4:3', '5:3', '5:4', '16:9', '16:10'].

    # Takes 2 arguments (self, aspect_ratio).
    r_agent.random_resolution('3:2')  # returns screen resolution.

    # Takes 3 arguments (self, device_type, os)
    agents.append(r_agent.random_agent('desktop', 'linux'))  # returns 'Desktop / Linux'
    agents.append(r_agent.random_agent('desktop', 'mac'))  # returns 'Desktop / Linux'
    agents.append(r_agent.random_agent('desktop', 'windows'))  # returns 'Desktop / Macintosh'

    agents.append(r_agent.random_agent('tablet', 'android'))  # returns 'Tablet / Android'
    agents.append(r_agent.random_agent('tablet', 'ios'))  # returns 'Tablet / iOS'

    agents.append(r_agent.random_agent('smartphone', 'android'))  # returns 'Smartphone / Android'
    agents.append(r_agent.random_agent('tablet', 'ios'))  # returns 'Smartphone / iOS'
    return (agents[m])


def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http': 'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session





# the link we will scrape
def get_countries():
	hed = {'User-Agent': user_a()}
	# The ip is reset before the request is called
	_set_new_ip()
	# untraceable tor session is requested
	session = get_tor_session()
	links = []
	pais = []
	res = requests.get("http://mercadolibre.com/", headers=hed)
	soup = bs4.BeautifulSoup(res.text, 'html')
	ts = soup.findAll("a", "ml-site-link")
	for t in ts:
		tx = t.get_text()
		ts = t['href'].replace("#from=homecom", "")
		print(ts)
		pais.append(tx)
		links.append(ts)

	dat = {'pais': pais, 'link': links}
	cat = pd.DataFrame(dat)
	return (cat)


def get_cat(country):
	hed = {'User-Agent': user_a()}
	# The ip is reset before the request is called
	_set_new_ip()
	# untraceable tor session is requested
	session = get_tor_session()
	links = []
	categories = []
	sub_categories = []
	res = requests.get(country + '/categorias#menu=categories', headers=hed)
	soup = bs4.BeautifulSoup(res.text, 'html')
	ts = soup.findAll("div", "categories__container")
	for t in ts:
		tx = t.find("a", "categories__title")
		ts = t.findAll("a", "categories__subtitle")

		for s in ts:
			links.append(s["href"])
			categories.append(tx.get_text())

			sub_categories.append(s.get_text())
		# links.append(t.get_text())
	# titles.append(t['href'])

	dat = {'sub-title': sub_categories, 'main-title': categories, 'link': links,
		   }
	cat = pd.DataFrame(dat)
	return (cat)



def secret_soup(link):
    strings = link.split("/")
    try:
        strings.remove("")
        strings.remove("https:")
    except ValueError:
        pass
    string = "https://validator.w3.org/nu/?showsource=yes&doc=https%3A%2F"
    link = string
    for s in strings:
        link = link + "%2F" + s
    hed = {'User-Agent': user_a()}
	# The ip is reset before the request is called
    _set_new_ip()
    # untraceable tor session is requested
    session = get_tor_session()
	# the link we will scrape
    res = session.get(link, headers=hed)
    soup = bs4.BeautifulSoup(res.text, 'html')
    source_code = ''
    for code in soup.select('ol.source > li > code'):
        if 'class' in code.attrs and 'lf' in code.attrs['class']:
            source_code += '\n'
        else:
            source_code += code.text
    soup2 = BeautifulSoup(source_code, 'lxml')
    return (soup2)


def get_dog(cat):
	hed = {'User-Agent': user_a()}
# The ip is reset before the request is called
	_set_new_ip()
# untraceable tor session is requested
	session = get_tor_session()
    # the link we will scrape
	image_links = []
	links = []
	price = []
	titles = []
	category = []
	subcategory = []
	envio = []
	ventas = []
	vendidos = []
	rating = []
	rank = []
	condition = []
	my_bar = st.progress(0)
	for x in range(len(cat.iloc[0])):
		my_bar.progress(x + 1 / len(cat.iloc[0]))
		soup2 = secret_soup(cat["link"].iloc[x])
		next_link = soup2.find('a', 'andes-pagination__link prefetch')
		my_bar2 = st.progress(0)
		results = soup.find("div", "quantity-results")
		pages = int(results.get_text().replace(",", "").replace("resultados", "")) / 50
		pages = int(pages)
		for page in pages:
			my_bar2.progress(x + (1 / pages))
			while next_link != None:

				next_link = soup2.find('a', "andes-pagination__link prefetch")
				ls = soup2.findAll('img', "lazy-load", src=True)
				divs = soup2.findAll('li', 'results-item highlighted article stack')
				for l in divs:

					i1 = l.find("img", src=True)
					if i1 != None:
						image_links.append(i1['src'])
					else:
						image_links.append(None)
					i = (l.find("a", "item__info-title")["href"])
					if i != None:
						links.append(i)
						category.append(cat["main-title"][1])
						subcategory.append(cat["sub-title"][1])
					u = l.find("span", "stack-item-info item--has-fulfillment")
					if u != None:
						envio.append(u.get_text())
					else:
						envio.append(None)

					t = l.find("a", "item__info-title")
					if t != None:
						titles.append(t.get_text())
					else:
						titles.append(None)
					p = l.find("span", "price__fraction")
					if p != None:

						price.append(int(p.get_text().split()[0].replace(",", "")))
					else:
						price.append(None)
					res = session.get(l.find("a", "item__info-title")["href"], headers=hed)
					soup2 = bs4.BeautifulSoup(res.text, 'html')
					g = soup2.find("div", "item-conditions")
					if g != None:
						st = g.get_text().split()

						try:
							vendidos.append(int(g.get_text().split()[2]))
						except IndexError:
							for word in st:
								if word.isdigit():
									vendidos.append(int(word))
					else:
						vendidos.append(None)
					y = soup2.find("div", "item-conditions")
					if y != None:
						if "Nuevo" in y.get_text().split():
							condition.append("Nuevo")
						else:
							if "Usado" in y.get_text().split():
								condition.append("Usado")
							else:
								condition.append(None)
					else:
						condition.append(None)
					u = soup2.find("span", "review-summary-average")
					if u != None:
						rating.append(float(u.get_text().split()[0]))

					else:
						rating.append(None)
					a = soup2.find("p", "card-subtitle section-subtitle power-seller")
					if a != None:
						rank.append(a.get_text().replace('MercadoLíder', ""))
					else:
						rank.append(None)
					z = soup2.find("dd", "reputation-relevant")
					if z != None:
						ventas.append(int(z.get_text().split()[0]))
					else:
						ventas.append(None)

	dat = {'title': titles, 'sub-title': subcategory, 'main-title': category, 'link': links,
		   'image': image_links, 'price': price,
		   'envio': envio,
		   'sales': ventas,
		   'product sales': vendidos,
		   "stars": rating,
		   "rank": rank,
		   "new": condition,
		   }

	dog = pd.DataFrame(dat)
	return (dog)


import streamlit as st


def get_the_loot(link):
    hed = {'User-Agent': user_a()}
    # The ip is reset before the request is called
    _set_new_ip()
    # untraceable tor session is requested
    session = get_tor_session()
    soup2 = secret_soup(link)

    res = requests.get(link, headers=hed)
    soup2 = bs4.BeautifulSoup(res.text, 'html')
    next_link = soup2.find('a', 'andes-pagination__link prefetch')
    results = soup2.find("div", "quantity-results")
    try:
        results=results.get_text()
        results=results.replace(",", "").replace(".", "").replace("resultados", "")
        pages = int(results)
        return(int(pages/50))
    #st.write('Hello, *World!* :sunglasses:')
    except AttributeError:
        return("Intenta de nuevo")

def single_scrape(link,rounds):
    import streamlit as st
    hed = {'User-Agent': user_a()}
    # The ip is reset before the request is called
    _set_new_ip()
    # untraceable tor session is requested
    session = get_tor_session()
    # the link we will scrape
    # the link we will scrape
    image_links = []
    links = []
    price = []
    titles = []
    category = []
    subcategory = []
    envio = []
    ventas = []
    vendidos = []
    rating = []
    rank = []
    condition = []
    soup2 = secret_soup(link)
    next_link = soup2.find('a', 'andes-pagination__link prefetch')
    my_bar2 = st.progress(0)
    results = soup2.find("div", "quantity-results")
    if results==None:
        return("Error No hay resultados")
    pages = int(results.get_text().replace(",", "").replace(".", "").replace("resultados", "")) / 50
    pages = int(pages)

    import time
    c=0
    for page in range(rounds):
        start_time = time.time()
        i=(1/rounds)*100

        for queef in range(int(i)):
            c=c+1
            if c<=99:
                my_bar2.progress(c+1)
        next_link = soup2.find('a', "andes-pagination__link prefetch")
        ls = soup2.findAll('img', "lazy-load", src=True)
        divs = soup2.findAll('li', 'results-item highlighted article stack')

        for l in divs:

            i1 = l.find("img", src=True)
            if i1 != None:
                image_links.append(i1['src'])
            else:
                image_links.append(None)
            i = (l.find("a", "item__info-title")["href"])
            if i != None:
                links.append(i)
                #category.append(cat["main-title"][1])
                #subcategory.append(cat["sub-title"][1])
            u = l.find("span", "stack-item-info item--has-fulfillment")
            if u != None:
                envio.append(u.get_text())
            else:
                envio.append(None)

            t = l.find("a", "item__info-title")
            if t != None:
                titles.append(t.get_text())
            else:
                titles.append(None)
            p = l.find("span", "price__fraction")
            if p != None:

                price.append(int(p.get_text().split()[0].replace(",", "")))
            else:
                price.append(None)
            res = session.get(l.find("a", "item__info-title")["href"], headers=hed)
            soup2 = bs4.BeautifulSoup(res.text, 'html')
            g = soup2.find("div", "item-conditions")
            if g != None:
                st = g.get_text().split()

                try:
                    vendidos.append(int(g.get_text().split()[2]))
                except IndexError:
                    for word in st:
                        if word.isdigit():
                            vendidos.append(int(word))
            else:
                vendidos.append(None)
            y = soup2.find("div", "item-conditions")
            if y != None:
                if "Nuevo" in y.get_text().split():
                    condition.append("Nuevo")
                else:
                    if "Usado" in y.get_text().split():
                        condition.append("Usado")
                    else:
                        condition.append(None)
            else:
                condition.append(None)
            u = soup2.find("span", "review-summary-average")
            if u != None:
                rating.append(float(u.get_text().split()[0]))

            else:
                rating.append(None)
            a = soup2.find("p", "card-subtitle section-subtitle power-seller")
            if a != None:
                rank.append(a.get_text().replace('MercadoLíder', ""))
            else:
                rank.append(None)
            z = soup2.find("dd", "reputation-relevant")
            if z != None:
                ventas.append(int(z.get_text().split()[0]))
            else:
                ventas.append(None)
    dat = {'title': titles, 'link': links,
           'image': image_links, 'price': price,
           'envio': envio,
           'sales': ventas,
           'product sales': vendidos,
           "stars": rating,
           "rank": rank,
           "new": condition,
           }

    dog = pd.DataFrame(dat)

    return (dog)




def single_scrape2(link,rounds):
    link=link+"_DisplayType_LF"
    import streamlit as st
    from selenium import webdriver
    from webdriver_manager.chrome import ChromeDriverManager
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)
    html = driver.page_source
    soup=BeautifulSoup(html)
    results = soup.find("div", "quantity-results")
    if results==None:
        return("Error No hay resultados")
    pages = int(results.get_text().replace(",", "").replace(".", "").replace("resultados", "")) / 50
    pages = int(pages)
    hed = {'User-Agent': user_a()}
    # The ip is reset before the request is called
    _set_new_ip()
    # untraceable tor session is requested
    session = get_tor_session()
    # the link we will scrape
    # the link we will scrape
    image_links = []
    links = []
    price = []
    titles = []
    category = []
    subcategory = []
    envio = []
    ventas = []
    vendidos = []
    rating = []
    rank = []
    condition = []
    my_bar2 = st.progress(0)
    results = soup.find("div", "quantity-results")
    if results==None:
        return("Error No hay resultados")
    pages = int(results.get_text().replace(",", "").replace(".", "").replace("resultados", "")) / 50
    pages = int(pages)

    import time
    c=0
    for page in range(rounds):
        start_time = time.time()
        i2 = (1 / rounds) * 100
        ls = soup.findAll('img', "lazy-load")
        divs = soup.findAll('li', 'results-item highlighted article stack')

        for l in divs:

            i1 = l.find("img", src=True)
            if i1 != None:
                image_links.append(i1['src'])
            else:
                image_links.append(None)
            i = (l.find("a", "item__info-title")["href"])
            if i != None:
                links.append(i)
                #category.append(cat["main-title"][1])
                #subcategory.append(cat["sub-title"][1])
            u = l.find("span", "stack-item-info item--has-fulfillment")
            if u != None:
                envio.append(u.get_text())
            else:
                envio.append(None)

            t = l.find("a", "item__info-title")
            if t != None:
                titles.append(t.get_text())
            else:
                titles.append(None)
            p = l.find("span", "price__fraction")
            if p != None:

                price.append(int(p.get_text().split()[0].replace(",", "")))
            else:
                price.append(None)
            u=l.find("a", "item__info-title")["href"]
            soup2=secret_soup(u)
            #res = session.get(l.find("a", "item__info-title")["href"], headers=hed)
            #soup2 = bs4.BeautifulSoup(res.text, 'html')
            print(soup2)
            g = soup2.find("div", "item-conditions")
            if g != None:
                st = g.get_text().split()
                for word in st:
                    if word.isdigit():
                        vendidos.append(int(word))

            else:
                vendidos.append(None)
            if len(vendidos)!=len(titles):
                vendidos.append(None)
                
            y = soup2.find("div", "item-conditions")
            if y != None:
                if "Nuevo" in y.get_text().split():
                    condition.append("Nuevo")
                else:
                    if "Usado" in y.get_text().split():
                        condition.append("Usado")
                    else:
                        condition.append(None)
            else:
                condition.append(None)
            u = soup2.find("span", "review-summary-average")
            if u != None:
                rating.append(float(u.get_text().split()[0]))

            else:
                rating.append(None)
            a = soup2.find("p", "card-subtitle section-subtitle power-seller")
            if a != None:
                rank.append(a.get_text().replace('MercadoLíder', ""))
            else:
                rank.append(None)
            z = soup2.find("dd", "reputation-relevant")
            if z != None:
                ventas.append(int(z.get_text().split()[0]))
            else:
                ventas.append(None)
            for queef in range(int(i2)):
                c = c + 1
                if c <= 99:
                    my_bar2.progress(c + 1)
        next_link = soup.find('a', "andes-pagination__link prefetch")
        if next_link:
            driver.get(next_link['href'])
        html = driver.page_source
        soup = BeautifulSoup(html)
    dat = {'title': titles, 'link': links,
           'image': image_links, 'price': price,
           'envio': envio,
           'sales': ventas,
           'product sales': vendidos,
           "stars": rating,
           "rank": rank,
           "new": condition,
           }
    print(len(titles))
    print(len(links))
    print(len(image_links))
    print(len(price))
    print(len(envio))
    print(len(ventas))
    print(len(vendidos))
    print(len(rank))
    print(len(condition))

    dog = pd.DataFrame(dat)

    return (dog)