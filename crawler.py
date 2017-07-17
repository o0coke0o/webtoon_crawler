import os

import requests
from bs4 import BeautifulSoup


def get_page_address(title, n):
	return 'http://comic.naver.com/webtoon/detail.nhn?titleId={}&no={}'.format(title, n)

def get_page_content(url):
	r = requests.get(url)
	return r.text

def get_page_images(content):
	images = []
	soup = BeautifulSoup(content, 'html.parser')
	for img in soup.find_all('img'):
		src = img.get('src')
		if src is None:
			continue
		if 'imgcomic.naver.net' in src:
			images.append(src)
	return images

def download_images(images, page_url, title, n):
	title_directory = str(title)
	if not os.path.exists(title_directory):
		os.makedirs(title_directory)

	directory = '{}/{}화'.format(title_directory, n)
	if not os.path.exists(directory):
		os.makedirs(directory)

	for url in images:
		headers = {'referer': page_url}
		r = requests.get(url, headers=headers)
		
		name = directory + '/' + url.split('/')[-1]
		f = open(name, 'wb')
		f.write(r.content)
		f.close()



title = 20853

for i in range (1, 11):
	print('{}화를 다운로드하는 중입니다...'.format(i))
	url = get_page_address(title, i)
	content = get_page_content(url)
	images = get_page_images(content)

	download_images(images, url, title, i)


