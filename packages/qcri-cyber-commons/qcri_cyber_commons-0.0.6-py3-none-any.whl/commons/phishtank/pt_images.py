import sys
import os

def download(url, phishid, folder):
    os.system("mkdir -p {}".format(folder))
    os.system("curl -O {}".format(url))
    os.system("mv {}.jpg {}".format(phishid, folder))

def download_file(filename, folder):
    f = open(filename, encoding = 'utf-8')
    for line in f:
        try:
            arr = line.split("#####")
            if arr == 0:
                continue
            download("https://d1750zhbc38ec0.cloudfront.net/{}.jpg".format(arr[0].strip()), arr[0].strip(), folder)
        except:
            print("Download error {}".format(line))
            pass

download_file(sys.argv[1], sys.argv[2])
