from tqdm import tqdm
import requests
def download_file(url, filename=''):
    try:
        if filename:
            pass            
        else:
            req = requests.get(url)
            filename = requests.url[downloadUrl.rfind('/')+1:]

        with requests.get(url) as req:
            with open(filename, 'wb') as f:
                for chunk in req.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            return filename
    except Exception as e:
        print(e)
 
 
def help():
	print("Use This Syntax")
	print(">>> from py_loader import download_file")
	print(">>> download_file('https://www.example.com/','name.html')")
	print()

def download_file_pg(url):
	response = requests.get(url, stream=True)
	total_size_in_bytes= int(response.headers.get('content-length', 0))
	block_size = 1024 
	progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
	with open('test.dat', 'wb') as file:
		for data in response.iter_content(block_size):
			progress_bar.update(len(data))
			file.write(data)
	progress_bar.close()
	if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
			print("ERROR, File size is less tan 10mb")
			download_file(url)
download_file_pg:('https://f-droid.org/repo/com.termux_117.apk')