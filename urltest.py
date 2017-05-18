import os
import sys
import queue
import urllib.request
import threading
# target = 'http://127.0.0.1/phpmyadmin'
# pathd = "/var/www/html/phpmyadmin"
filter_d = [".html",".php"]
files_list = queue.Queue()
try:
	target = sys.argv[1]
	pathd = sys.argv[2]
except:
	print("please check the syntax!\n")
	exit()

try:
	filters = [sys.argv[3]]+filter_d
except:
	filters = filter_d

threads = 10
def search_files(path):
	os.chdir(pathd)
	for r,d,f in os.walk("."):
		# print(r,f)
		for files in f:
			pathc = "%s/%s"%(r,files)
			# print(pathc)
			if pathc.startswith("."):
				pathc = pathc[1:]
				# print(pathc)
			if os.path.splitext(files)[1]   in filters:
				files_list.put(pathc)
				# print(files_list.get())
	return	files_list




def test_target(files_list,target):
	while not files_list.empty():
		path = files_list.get()
		url = "%s%s"%(target,path)
		try:
			 res=urllib.request.urlopen(url)
			 print(res.getcode())
			 print("found==>"+url)
		except urllib.error.HTTPError as error:
			print(error,url)


a = search_files(pathd)

# test_target(a,target)


for i in range(threads):
	t = threading.Thread(target=test_target(a,target))
	t.start()