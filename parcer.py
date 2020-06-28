import requests
from bs4 import BeautifulSoup
import csv
from get_city import get_city
from threading import Thread
	
	

def get_table_from_site(year,month,city):
	
	headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
	value = get_city()[city]
	url = 'https://www.gismeteo.ru/diary/%s/%s/%s/' %(value,year,month)
	try:
		r = requests.get(url, headers = headers)		
		soup = BeautifulSoup(r.text,'lxml')
		table = soup.find('tbody').find_all('tr',{'align':'center'})
		#print('Request succesful!')
		return table
	except:
		pass
		#print("Request don't sent!")
def image_to_str(line,n):
	def weather(img):
		weather_dict = {'gismeteo.ru/static/diary/img/dull.png':'Пасмурно',
						'gismeteo.ru/static/diary/img/sun.png':'Ясно',
						'gismeteo.ru/static/diary/img/sunc.png':'Малооблачно',
						'gismeteo.ru/static/diary/img/suncl.png':'Облачно',
						'gismeteo.ru/static/diary/img/rain.png':'Дождь',
						'gismeteo.ru/static/diary/img/snow.png':'Снег',
						'gismeteo.ru/static/diary/img/storm.png':'Гроза'
		}
		return weather_dict[img]
		
	
	
	if (n == 8 or n == 3):
		try:
			cloud_line = line.find_all('td')[n]
			img = cloud_line.find('img').get('src')
			return weather(img[6:])
		except:
			return ''
	else:
		try:
			ph_line = line.find_all('td')[n]
			img = ph_line.find('img').get('src')
			return weather(img[6:])
		except:
			return ''
		

def get_str(line,year,month):
	global n
	global city
	date = str(line.find_all('td')[0].text) + '.' + str(month) + '.' + str(year)
	day = [n,city,date,line.find_all('td')[1].text,
			line.find_all('td')[2].text,
			image_to_str(line,3),
			image_to_str(line,4),
			line.find_all('td')[5].text,
			line.find_all('td')[6].text,
			line.find_all('td')[7].text,
			image_to_str(line,8),
			image_to_str(line,9),
			line.find_all('td')[10].text]
	return day
			
			

def write_year(year):
	global city
	global n
	with open('test.csv','a',) as f:
		wr = csv.writer(f)
		for city in get_city():
			if year<2020:
				for month in range(1,12):
					table = get_table_from_site(year,month,city)
					#print("City: %15s Year: %4d Month: %2d\nComplete write:%10d" %(city,year,month,n), end='\r')
					try:
						for line in table:
							wr.writerow(get_str(line,year,month))
							n+=1
					except:
						pass
			else:
				for month in range(1,6):
					table = get_table_from_site(year,month,city)
					#print("City: %15s Year: %4d Month: %2d\nComplete write:%10d" %(city,year,month,n), end='\r')
					try:
						for line in table:
							wr.writerow(get_str(line,year,month))
							n+=1
					except:
						pass
def check_status():
	global n
	proc=0
	while proc!=100:
		total = (365*4+366+31+29+31+30+31)*len(get_city())
		proc = int((n/total)*100)
		stat = '[%s%s]' %("##"*(proc//10),'--'*(10-(proc//10)))
		string = 'Complete %22s %i%% Write:%i' %(stat,proc,n)
		print(string,end='\r')
def write_to_file():
	header_list = ['Num','City','Date','daytime_temperature','daytime_pressure','daytime_overcast'
					'daytime_phonemon','daytime_wind','nignttme_temperature',
					'nignttme_pressure','nighttime_overcast','nignttme_phonemon','nignttme_wind']	
	with open('test.csv','w',) as f:
		wr = csv.writer(f)
		wr.writerow(header_list)
	year2015 = Thread(target=write_year, args=(2015,))
	year2016 = Thread(target=write_year, args=(2016,))
	year2017 = Thread(target=write_year, args=(2017,))
	year2018 = Thread(target=write_year, args=(2018,))
	year2019 = Thread(target=write_year, args=(2019,))
	year2020 = Thread(target=write_year, args=(2020,))
	stat = Thread(target=check_status)
	year2015.start()
	year2016.start()
	year2017.start()
	year2018.start()
	year2019.start()
	year2020.start()
	stat.start()
	
		
		
		
	

city = ""
n=1
#write_to_file()
check_status()
