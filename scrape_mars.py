from bs4 import BeautifulSoup
import requests
import pandas as pd
from splinter import Browser
import time

def scrape():
	#NASA MARS NEWS
	html = requests.get("https://mars.nasa.gov/news/").text
	soup = BeautifulSoup(html, 'lxml')
	news_title = soup.find('div', class_='content_title').text.strip()
	news_p = soup.find('div', class_='rollover_description_inner' ).text.strip()
	
	#JPL MARS SPACE IMAGES - FEATURED IMAGE
	#browser = Browser("chrome",headless="False")
	browser = Browser("chrome",headless="False")
	url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
	browser.visit(url)
	browser.find_by_id('full_image').first.click()
	time.sleep(2)
	browser.find_link_by_partial_text('more info').first.click()
	browser.find_by_css('img.main_image').first.click()
	image_url = browser.url

	#MARS WEATHER
	html = requests.get("https://twitter.com/marswxreport?lang=en").text
	soup = BeautifulSoup(html, 'lxml')
	tweet_list = soup('p', 'TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
	#Not all tweets are weather reports; all weather reports seem to start with 'Sol'
	mars_weather = ''
	weather_found = False
	weather_index = 0
	while weather_found == False:
		if "Sol" in tweet_list[weather_index].text.strip():
			mars_weather = tweet_list[weather_index].text.strip()
			weather_found = True
		else:
			weather_index += 1

	# MARS FACTS
	html = requests.get("https://space-facts.com/mars/").text
	table = pd.read_html(html)[0]
	table = table.rename(columns =  { 0:"Feature", 1:"Value" })
	table = table.set_index('Feature')
	table_html = table.to_html()

	# MARS HEMISPHERES
	browser = Browser("chrome",headless="False")
	url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
	browser.visit(url)
	links = browser.find_link_by_partial_text('Enhanced')
	url_list = []
	title_url_list = []
	for j in range(4):
		browser.find_link_by_partial_text('Enhanced')[j].click()
		time.sleep(1)
		browser.click_link_by_partial_href('jpg')
		time.sleep(1)
		url_list.append(browser.windows[1].url)
		title_url_list.append(browser.windows[0].url)
		browser.windows[1].close()
		browser.click_link_by_partial_text("Back")
	hemisphere_list = [title_url_list[j].split('/')[7].split('_enhanced')[0] for j in range(4)]
	hemisphere_dicts = [ { "title" : hemisphere_list[j] , "img_url": url_list[j]  } for j in range(4) ]

	mars_info = {"News_Title":news_title,
	 "News_p":news_p,
	 "Featured_Image": image_url,
	 "Weather":mars_weather,
	 "Facts":table_html,
	 "Hemispheres":hemisphere_dicts  }
	return mars_info





















