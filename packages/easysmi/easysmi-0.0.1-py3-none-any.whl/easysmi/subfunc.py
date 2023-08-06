import os, re
import chardet

def make_dirs(path): 
    try:
        os.makedirs(path) 
    except OSError: 
        if not os.path.isdir(path): 
            raise

def remove_tag(content):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', content)
    return cleantext

def read_file(path):
    #파일 열어서 인코딩 확인
    rawdata = open(path, 'rb').read()
    result = chardet.detect(rawdata)
    enc = result['encoding']
    
    #인코딩 맞게 열기
    f = open(path, "r", encoding = enc)
    line = f.readline()

    data = ""
    while line:
        data += line
        line = f.readline()
    f.close()
    return data




