import os
import sys

import argparse
import requests
import subprocess
from xml.etree import ElementTree
import urllib
import shutil
from contextlib import closing

# ENCODE
def encode(path):
    DIR = path + 'encode/'
    subprocess.run(['mkdir', DIR])

    for i in range(12, 13):
        r = requests.get(f"https://www.encodeproject.org/report/?type=File&file_format_type=bed{i}&format=json")
        r = r.json()
        entries = r['@graph']
        for entry in entries:
            url = "https://www.encodeproject.org" + entry['href']
            i = entry['href'].rfind('/')
            filename = entry['href'][i+1:]
            bed_file = requests.get(url, allow_redirects=True)
            length = float(bed_file.headers.get('content-length', None))
            if length and length <= 1e5:
                open(DIR + filename, 'wb').write(bed_file.content)
                print(filename)
                front , extension = os.path.splitext(filename)
                if extension == '.gz':
                    subprocess.call(['gzip', '-d', DIR + filename])
                elif extension == '.bigBed' or extension == '.bb':
                    subprocess.call(['bigBedToBed', DIR + filename, DIR + front + '.bed'])

# UCSC

def ucsc(path):
    DIR = path + 'ucsc/'
    subprocess.run(['mkdir', DIR])

    names = open('list.txt')
    for url in names.readlines():
        url = url.strip()
        r = requests.get(url)
        i = url.rfind('/')
        title = url[i+1:]
        i = url.find('gbdb/')
        j = url.find('/', i + 5)
        build = url[i+5:j]
        filename = DIR + build + title
        open(filename, 'wb').write(r.content)
        front, extension = os.path.splitext(filename)
        subprocess.call(['bigBedToBed', filename, front + '.bed'])
        sys.stderr.write(f"Downloaded {title}\n")
        subprocess.call(['rm', '-f', filename])

# NCBI GEO
def ncbi(path):
    DIR = path + 'ncbi/'
    subprocess.run(['mkdir', DIR])

    r = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gds&term=BED[suppFile]&retMax=1000')
    tree = ElementTree.fromstring(r.content)
    count = int(tree[0].text)
    sys.stderr.write(f"{count} Ids found\n")
    for i in range(200, 1000):
        Id = tree[3][i].text
        # Get each result from a query
        s = requests.get('https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gds&id=' + Id)
        id_tree = ElementTree.fromstring(s.content)
        url = id_tree[0][-2].text + 'suppl/'
        output = subprocess.run(['curl', url], capture_output=True, text=True)
        files = output.stdout.split('\n')
        for file in files[:-1]:
            file_data = file.split()
            filename = file_data[-1]
            filesize = int(file_data[4])
            if filesize > 1000000:
                continue
            if filename.endswith('.bed.gz') or filename.endswith('.bed')  \
                or filename.endswith('.bb') or filename.endswith('.bigBed'):
                with closing(urllib.request.urlopen(url + filename)) as t:
                    with open(DIR + filename, 'wb') as f:
                        shutil.copyfileobj(t, f)
                if filename.endswith('.gz'):
                    subprocess.call(['gzip', '-d', DIR + filename])
                    subprocess.call(['rm', '-f', DIR + filename])
                elif filename.endswith('.bigBed'):
                    subprocess.call(['bigBedToBed', DIR + filename, DIR + filename[:-6] + 'bed'])
                    subprocess.call(['rm', '-f', DIR + filename])
                elif filename.endswith('.bb'):
                    subprocess.call(['bigBedToBed', DIR + filename, DIR + filename[:-2] + 'bed'])
                    subprocess.call(['rm', '-f', DIR + filename])
                sys.stderr.write(f'{filename} downloaded\n')

# Zenodo
def zenodo(path):
    DIR = path + '/zenodo/'
    subprocess.run(['mkdir', DIR])

    r = requests.get("https://zenodo.org/api/records/?q=filetype:bed")
    r = r.json()
    hits = r['hits']['hits']
    for hit in hits:
        files = hit['files']
        for file in files:
            filename = file['key']
            if filename.endswith('bed'):
                s = requests.get(file['links']['self'])
                length = int(s.headers.get('content-length', None))
                if length and length <= 1e5: open(DIR + filename, 'wb').write(s.content)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Download BED files from one or more of NCBI GEO Datasets," +
        " Zenodo, UCSC Track Hubs, and ENCODE. By default, all will be downloaded."
    )
    parser.add_argument("-E", action='store_true', help="Download from ENCODE")
    parser.add_argument("-Z", action='store_true', help="Download from Zenodo")
    parser.add_argument("-U", action='store_true', help="Download from UCSC")
    parser.add_argument("-N", action='store_true', help="Download from NCBI GEO")
    parser.add_argument("-o", "--out", help="Directory to store downloaded files. Default is ./data/")

    args = parser.parse_args()
    if args.out is None:
        path = './data/'
    else:
        path = args.out
    if not (args.E or args.Z or args.U or args.N):
        encode(path)
        zenodo(path)
        ucsc(path)
        ncbi(path)
    else:
        if args.E:
            encode(path)
        if args.Z:
            zenodo(path)
        if args.U:
            zenodo(path)
        if args.N:
            zenodo(path)
    