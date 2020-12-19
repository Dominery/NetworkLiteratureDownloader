import os
import re

def merge_files(dictionary_path):
    try:
        filelist=os.listdir(dictionary_path)
        num=len(filelist)
    except:
        print('can not find the path of dictionary')
        return
    if dictionary_path[-1:]=='/':
        pass
    else:
        path=dictionary_path+'/'
    count=0
    target_filenames=['作者相关.txt','牧神记.txt']
    for f in filelist:
        target_path=target_filenames[decide_target(f)]
        write(path+f,target_path,os.path.splitext(f)[0])
        count+=1
        print('\r已完成{:.2f}%'.format(count/num*100),end='')

def write(file_path,target_path,file_name):
    if os.path.exists(target_path):
        pattern='a'
    else:
        pattern='w'
    with open(file_path,'r',encoding='utf-8')as f:
        with open(target_path,pattern,encoding='utf-8')as g:
            g.writelines('\n'+file_name.center(50,' ')+'\n')
            g.writelines(f.readlines())

def decide_target(file_name):
    result = re.match("第(\d{4})章", file_name)
    if result:
        return True
    else:
        return False
