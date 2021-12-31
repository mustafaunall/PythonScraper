import sys
import requests
from bs4 import BeautifulSoup
from time import sleep
import xlrd
from xlutils.copy import copy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from flask import Flask, jsonify
from flask_cors import CORS

sys.setrecursionlimit(999999999)
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
CORS(app)
excel_path = './dist/datas.xls'
webdriverLocation = './dist/chromedriver.exe'

websites = [
	{ 'name': 'freshworld', 'url': 'https://www.freshworld.com.tr/' },
	{'name': 'tazedirekt', 'url': 'https://www.tazedirekt.com/'},
	{'name': 'misbahcem', 'url': 'https://www.misbahcem.com/'},
	{'name': 'tazemasa', 'url': 'https://www.tazemasa.com/'},
	{'name': 'hasanbey', 'url': 'https://www.hasanbey.com/'},
	{'name': 'greenada', 'url': 'https://www.greenada.com/'},
	{'name': 'sebzemeyvedunyasi', 'url': 'https://www.sebzemeyvedunyasi.com/'},
]

def getProductNames():
	_array = []
	wb = xlrd.open_workbook(excel_path)
	sheet = wb.sheet_by_index(0)
	for row in sheet.get_rows():
		x = str(row[3]).replace('text:\'', '').replace('\'', '')
		if not x.__contains__('empty'):
			_array.append(x)
	return _array

def getSiteUrl(sitename):
	for website in websites:
		if website['name'] == sitename:
			_siteUrl = website['url']
	return _siteUrl

def getResultFromFreshWorld(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	#options.add_argument('--headless')
	#options.add_argument('--disable-gpu')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('freshworld'))
	sleep(1)

	try:
		driver.find_element_by_css_selector('#onesignal-slidedown-cancel-button').click()
		sleep(1)
		searchbar = driver.find_element_by_id('woocommerce-product-search-field-0')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_css_selector(
			'#masthead > div.main-header.col-full > div.site-search > div > form > button').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		ul = driver.find_element_by_css_selector('#main > div.columns-4 > ul')
		lis = ul.find_elements_by_tag_name('li')
		for _li in lis:
			productName = _li.find_element_by_css_selector(
				'div.woocommerce-card__header > div.woocommerce-loop-product__title > a').text
			productPrice = _li.find_element_by_css_selector('div.woocommerce-card__header > span').text
			productPrice = productPrice.replace(' ₺', '')
			if ' ' in productPrice:
				productPrice = productPrice.split(' ')[1]
			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getResultFromTazeDirekt(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('tazedirekt'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('product-search-combobox--trigger')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_css_selector('#product-search-combobox--trigger').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		productsMainDiv = driver.find_element_by_css_selector(
			'body > app-root > app-product > mat-sidenav-container > mat-sidenav-content > main > td-product-search > div.search-page > fe-product-list > div')
		productsDiv = productsMainDiv.find_elements_by_tag_name('fe-product-card')
		for productDiv in productsDiv:
			productName = productDiv.find_element_by_tag_name('fe-product-name').find_element_by_tag_name(
				'h1').find_element_by_tag_name('a').text
			productPrice = productDiv.find_element_by_tag_name('fe-product-price').find_element_by_tag_name(
				'div').find_element_by_tag_name('div').find_element_by_tag_name('span').text.split(' ')[0]
			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getResultFromMisBahcem(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('misbahcem'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('txtbxArama')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_id('txtbxArama').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		productsMainDiv = driver.find_element_by_css_selector(
			'#ProductPageProductList')
		productsDiv = productsMainDiv.find_elements_by_tag_name('div')
		for productDiv in productsDiv:
			#önceden aynı name varsa break at
			productName = productDiv.find_elements_by_tag_name('div')[1].find_elements_by_tag_name('div')[1].find_element_by_tag_name('a').text
			print(productName)
			products.append({'name': productName})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getResultFromTazeMasa(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('tazemasa'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('txtbxArama')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_id('txtbxArama').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		productsMainDiv = driver.find_element_by_id('ProductPageProductList')
		productsDiv = productsMainDiv.find_elements_by_class_name('ItemOrj')
		for productDiv in productsDiv:
			productName = productDiv.find_element_by_tag_name('div')
			productName = productName.find_element_by_class_name('productDetail').find_element_by_class_name('productName').find_element_by_tag_name('a').text

			productPrice = productDiv.find_element_by_tag_name('div')
			productPrice = productPrice.find_element_by_class_name('productDetail').find_element_by_class_name('productPrice ').find_element_by_tag_name('div').find_element_by_tag_name('span').text.split(' TL')[0]
			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getResultFromHasanbey(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('hasanbey'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('txtbxArama')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_id('txtbxArama').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		productsMainDiv = driver.find_element_by_id('ProductPageProductList')
		productsDiv = productsMainDiv.find_elements_by_class_name('ItemOrj')
		for productDiv in productsDiv:
			productName = productDiv.find_element_by_tag_name('div')
			productName = productName.find_element_by_class_name('productDetail').find_element_by_class_name('productName').find_element_by_tag_name('a').text

			productPrice = productDiv.find_element_by_tag_name('div')
			productPrice = productPrice.find_element_by_class_name('productDetail').find_element_by_class_name('productPrice ').find_element_by_tag_name('div').find_element_by_tag_name('span').text.split(' TL')[0]

			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	if len(products) == 0:
		return None
	else:
		return products

def getResultFromGreenada(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('greenada'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('txtbxArama')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_id('txtbxArama').send_keys(Keys.ENTER)
		sleep(2)
		products = []
		productsMainDiv = driver.find_element_by_id('ProductPageProductList')
		productsDiv = productsMainDiv.find_elements_by_class_name('ItemOrj')
		for productDiv in productsDiv:
			productName = productDiv.find_element_by_tag_name('div')
			productName = productName.find_element_by_class_name('productDetail').find_element_by_class_name('productName').find_element_by_tag_name('a').text

			productPrice = productDiv.find_element_by_tag_name('div')
			productPrice = productPrice.find_element_by_class_name('productDetail').find_element_by_class_name('productPrice ').find_element_by_tag_name('div').find_element_by_tag_name('span').text.split(' TRY')[0]
			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getResultFromSebzeMeyveDunyasi(product):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	driver = webdriver.Chrome(options=options, executable_path=webdriverLocation)
	driver.get(getSiteUrl('sebzemeyvedunyasi'))
	sleep(1)
	try:
		searchbar = driver.find_element_by_id('txtbxArama')
		searchbar.send_keys(product)
		sleep(1)
		driver.find_element_by_id('txtbxArama').send_keys(Keys.ENTER)
		sleep(6)
		products = []
		productsMainDiv = driver.find_element_by_id('ProductPageProductList')
		productsDiv = productsMainDiv.find_elements_by_class_name('ItemOrj')
		for productDiv in productsDiv:
			productName = productDiv.find_element_by_tag_name('div')
			productName = productName.find_element_by_class_name('productDetail').find_element_by_class_name('productName').find_element_by_tag_name('a').text

			productPrice = productDiv.find_element_by_tag_name('div')
			productPrice = productPrice.find_element_by_class_name('productDetail').find_element_by_class_name('productPrice ').find_element_by_tag_name('div').find_element_by_tag_name('span').text.split(' TL')[0]
			products.append({'name': productName, 'price': productPrice})
	except NoSuchElementException:
		driver.close()
		return None
	driver.close()
	return products

def getProductFromAllSites(products):
	result = []
	for product in products:
		_arr = []
		freshworld = getResultFromFreshWorld(product)
		if freshworld is not None:
			_arr.append({"siteName": "freshworld", "values": freshworld})
		else:
			_arr.append({"siteName": "freshworld", "values": {'error': 'Stokta bulunamadı!'}})

		tazedirekt = getResultFromTazeDirekt(product)
		if tazedirekt is not None:
			_arr.append({"siteName": "tazedirekt", "values": tazedirekt})
		else:
			_arr.append({"siteName": "tazedirekt", "values": {'error': 'Stokta bulunamadı!'}})

		"""
		misbahcem = getResultFromMisBahcem(product)
		if misbahcem is not None:
			_arr['misbahcem'] = misbahcem
		else:
			_arr['misbahcem'] = {'error': 'Stokta bulunamadı!'}
		"""

		tazemasa = getResultFromTazeMasa(product)
		if tazemasa is not None:
			_arr.append({"siteName": "tazemasa", "values": tazemasa})
		else:
			_arr.append({"siteName": "tazemasa", "values": {'error': 'Stokta bulunamadı!'}})

		hasanbey = getResultFromHasanbey(product)
		if hasanbey is not None:
			_arr.append({"siteName": "hasanbey", "values": hasanbey})
		else:
			_arr.append({"siteName": "hasanbey", "values": {'error': 'Stokta bulunamadı!'}})

		greenada = getResultFromGreenada(product)
		if greenada is not None:
			_arr.append({"siteName": "greenada", "values": greenada})
		else:
			_arr.append({"siteName": "greenada", "values": {'error': 'Stokta bulunamadı!'}})

		sebzemeyvedunyasi = getResultFromSebzeMeyveDunyasi(product)
		if sebzemeyvedunyasi is not None:
			_arr.append({"siteName": "sebzemeyvedunyasi", "values": sebzemeyvedunyasi})
		else:
			_arr.append({"siteName": "sebzemeyvedunyasi", "values": {'error': 'Stokta bulunamadı!'}})

		result.append({"productName": product, "values": _arr})
	print(result)
	return result


def writeToExcel(x, y, content):
	try:
		wb = xlrd.open_workbook(excel_path)
		_copy = copy(wb)
		s = _copy.get_sheet(0)
		s.write(x, y, content)
		_copy.save('output.xls')
		return True
	except:
		return False


@app.route('/getProductNames')
def ProductNames():
	products = getProductNames()
	return jsonify(products)


@app.route('/getProductData/<product>')
def ProductData(product):
	data = getProductFromAllSites([product])
	return jsonify(data)


if __name__ == '__main__':
	app.run('0.0.0.0', 5000, debug=True)
