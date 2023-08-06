#!/usr/bin/env python
# coding: utf-8

# In[1]:


import re,os,json
import chardet
from subfunc import *


# In[2]:


'''
Author: pgh268400 (https://pgh268400.tistory.com/)
Version: 1.0
License: MIT License
'''

#raw_data => 자막 파일 텍스트 데이터
def parse_smi(path):
    raw_data = read_file(path)
    
    result = {}
    td,text = [], []
    p = re.compile("<SYNC Start=[0-9]+><P Class=KRCC>", re.MULTILINE) #타임라인만 매칭시킨다.
    time_line = p.findall(raw_data)
    replaced = p.sub('@', raw_data).split("@")[1:] #타임라인 문자 전부 @로 치환 후 split로 쪼갠다.
    
    for i in range(len(time_line)):
        td.append([time_line[i], replaced[i]]) #[타임라인, 대사] 로 저장한다.
        
    for element in replaced:
        line = remove_tag(element).strip().replace("&nbsp;", "")
        if line : text.append(line)

    #데이터 정리
    result['main'] = td
    result['raw'] = raw_data
    result['text'] = text
    result['line'] = len(td)
    
    return result


#텍스트로 파싱된 라인 찾기
def find_line_by_text(parsed_data, target):
    parsed_data = parsed_data['main']
    j = -1
    for element in parsed_data:
        j+= 1
        for i in range(len(element)):
            if target in element[i]:
                return j
    return j

#정규식으로 파싱된 라인 찾기
def find_line_by_regex(parsed_data, regex):
    parsed_data = parsed_data['main']
    
    j = -1
    for element in parsed_data:
        j+= 1
        for i in range(len(element)):
            m = re.search(regex, element[i])
            if m : return j
    return j
    
#parsed_data => parse_smi 의 output으로 나온 리스트 데이터
#start_line => 몇번째 항목부터 옮길 것인지. (0번째부터 시작)
#shift_amount => 얼마만큼 싱크 조절할 것인지. (-1000 -> 1초 빨리 나오게 하기, 10000 -> 10초 늦게 나오게 하기)
def sync_shift(parsed_data, start_line, shift_amount): 
    i = 0
    for element in parsed_data['main']:
        if i >= start_line:
            sync = element[0]
            p = re.compile("[0-9]+", re.MULTILINE)
            sync_time = int(p.search(sync).group())
            element[0] = sync.replace(str(sync_time), str(sync_time + shift_amount))
        i+=1
    return parsed_data

#path => 파일 저장 경로
#shifted_data => 덮어 씌울 싱크 작업된 parsed_data
def file_save(path, shifted_data):
    raw = shifted_data['raw']
    try:
        pos = raw.find('<SYNC Start=')
        splited_data = raw[:pos] #자막 SYNC 시작 뒤부분을 전부 짜른다.

        #싱크 작업된 데이터(리스트)를 문자열로 변환한다.
        shifted_raw = ""
        for data in shifted_data['main']:
            for element in data:
                shifted_raw += element

        #원본에 합친다.
        output = splited_data + shifted_raw

        #파일로 저장한다.
        f = open(path, "w", encoding='utf-8')
        f.write(output)
        f.close()
        print(path, "작업이 완료되었습니다.")
    except Exception as e:
        print(e)


# In[3]:


#단일 파일 처리

folder = 'C:/Users/File/자막/'
filename = '[SubsPlease] Tokyo Revengers - 02 (1080p) [B66CEAA7].smi'

p = parse_smi(folder + filename)
search_line = find_line_by_text(p, "sub by")

if search_line != -1:
    s = sync_shift(p, search_line, -10000)
    s = sync_shift(s, 0, 1300)
    
    make_dirs(folder + 'output') #make output folder
    new_path = folder + "output/" + filename
    file_save(new_path, s)
else:
    print("cannot find item")


# In[ ]:


#폴더안에 있는 것 일괄 처리
folder = 'C:/Users/File/자막/'
file_list = os.listdir(folder)

for filename in file_list:
    if filename.endswith('.smi'):
        p = parse_smi(folder + filename)
        search_line = find_line_by_text(p, "sub by")
        if search_line != -1:
            s = sync_shift(p, search_line, -10000)

            make_dirs(folder + 'output') #make output folder
            new_path = folder + "output/" + filename
            file_save(new_path, s)
        else:
            print("cannot find item")


# In[ ]:


folder = 'C:/Users/File/자막/'
filename = '[SubsPlease] Tokyo Revengers - 02 (1080p) [B66CEAA7].smi'

p = parse_smi(folder + filename)
print(p['line'])
search_line = find_line_by_text(p, "sub by")
print(search_line)


# In[ ]:


len([[],[],[]])


# In[ ]:




