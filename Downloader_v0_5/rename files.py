import os
import re

# def prefix_change(prefix_name):
#     dict={'一':'1','二':'2','三':'3',
#           '四':'4','五':'5','六':'6',
#           '七':'7','九':'9','百':'','八':'8',
#           '千':'','零':'0','十':''}
#     dict2={'百':'00', '千':'000','十':'0'}
#     if prefix_name.strip()[:1]=='第':
#         if prefix_name[-2] in dict2.keys():
#             prefix_name=prefix_name.replace(prefix_name[-2],dict2[prefix_name[-2]])
#         for i in dict.keys():
#             try:
#                 prefix_name=prefix_name.replace(i,dict[i])
#             except:
#                 continue
#         n=len(prefix_name)
#         if n <6:
#             prefix_name=prefix_name.replace('第','第'+'0'*(6-n))
#
#     return prefix_name

def rename_file(dictionary_path):
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
    for f in filelist:
        new_name=prefix_change(f)
        old_path=path+f
        new_path=path+new_name
        os.rename(old_path,new_path)
        count+=1
        print('\r已完成{:.2f}%'.format(count/num*100),end='')


# def prefix_change(prefix_name):
#     num_string='零一二三四五六七八九十百千'
#     num_list=[]
#     if '第'in prefix_name.strip() and '章' in prefix_name.strip():
#         stock=prefix_name.split('章')
#         for i in stock[0]:
#             num_list.append(i)
#         set_list=['0','0','0','0']
#         dict = {'百': 1, '千': 0, '十': 2}
#         for i in range(len(num_list)):
#             if num_list[i] in dict.keys():
#                 set_list[dict[num_list[i]]]=str(num_string.index(num_list[i-1]))
#         if num_list[-1] not in dict.keys():
#             set_list[3]=str(num_string.index(num_list[-1]))
#         return '第'+''.join(set_list)+'章'+stock[1]
#     else:
#         return prefix_name

def prefix_change(full_name):
    '''num_string='零一二三四五六七八九十百千'
    num_list=[]
    if '第'in prefix_name.strip() and '章' in prefix_name.strip():
        stock=prefix_name.split('章')
        for i in stock[0]:
            num_list.append(i)
        set_list=['0','0','0','0']
        dict = {'百': 1, '千': 0, '十': 2}
        for i in range(len(num_list)):
            if num_list[i] in dict.keys():
                set_list[dict[num_list[i]]]=str(num_string.index(num_list[i-1]))
        if num_list[-1] not in dict.keys():
            set_list[3]=str(num_string.index(num_list[-1]))
        return '第'+''.join(set_list)+'章'+stock[1]
    else:
        return prefix_name'''
    num_string = '零一二三四五六七八九十百千'
    result=re.search("第(['零一二三四五六七八九十百千']*?)章(.*?).txt",full_name)
    if result:
        num_list = []
        stock = result.group(1)
        for i in stock:
            num_list.append(i)
        set_list = ['0', '0', '0', '0']
        if re.search('["十百千"]',result.group(1)):
            dict = {'百': 1, '千': 0, '十': 2}
            for i in range(len(num_list)):
                if num_list[i] in dict.keys():
                    if i==0:
                        set_list[dict[num_list[i]]]='1'
                    else:
                        set_list[dict[num_list[i]]] = str(num_string.index(num_list[i - 1]))
            if num_list[-1] not in dict.keys():
                set_list[3] = str(num_string.index(num_list[-1]))
        else:
            # to format the title which doesn't have characters like '十百千'
            num_list.reverse() # process the situation that the num doesn't have thousand position
            for i in range(len(num_list)):
                set_list[3-i]=str(num_string.index(num_list[i]))
        return '第' + ''.join(set_list) + '章' + result.group(2)
    else:
        return full_name



