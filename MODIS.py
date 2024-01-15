import csv
import requests
from requests.exceptions import ProxyError
import os

def find_string_in_filenames(directory, string_to_find):
    # 使用os.listdir获取文件夹中的所有文件名
    filenames = os.listdir(directory)

    # 遍历文件名，检查字符串是否在文件名中
    for filename in filenames:
        if string_to_find in filename:
            return True
    return False
error_count = 0
error_log = []
error_name = []

# namelist = []
# for year in range(2003,2019):
#     for month in range(1,13):
#         namelist.append(str(year)+'_'+str(month)+'.tif')
namelist = ['2003_12', '2003_2', '2003_3', '2004_10', '2004_2', '2004_4', '2004_5',
            '2004_6', '2004_7', '2004_8', '2005_1', '2005_12', '2005_2', '2005_5',
            '2005_8', '2006_10', '2006_5', '2006_6', '2007_11', '2007_6', '2007_7',
            '2007_9', '2009_1', '2009_10', '2009_2', '2009_6', '2009_7', '2010_2',
            '2010_3', '2010_4', '2010_5', '2010_8', '2011_8', '2012_10', '2012_4',
            '2012_5', '2012_9', '2016_12', '2016_2', '2017_11', '2017_3', '2017_5', '2017_8']

num = 0
with open(r"C:\Users\changlishu\Downloads\MODIS_xiubu.csv", 'r') as csvfile:
    # 创建csv阅读器
    csvreader = csv.reader(csvfile)
    # 逐行读取
    for row in csvreader:
        url = row[1]
        if (url[0] != 'n'):
            try:
                if find_string_in_filenames(r'E:\\python\\GEEpython\\MODIS', namelist[num]+'.tif'):
                    num+=1
                    continue
                print(namelist[num])
                print(url)
                response = requests.get(url)
                # with open('MODIS/' + namelist[num], 'wb') as file:
                with open('MODIS/' + namelist[num] + '.tif', 'wb') as file:
                    file.write(response.content)
            except ProxyError:
                print(f"ProxyError")
                error_count += 1
                error_log.append(url)
                error_name.append(namelist[num])
            except requests.exceptions.SSLError:
                print(f"SSLError")
                error_count += 1
                error_log.append(url)
                error_name.append(namelist[num])
            num += 1
print(f"Download finished with {error_count} errors.")
error_name2 = []
error_log2 = []
while error_count > 0:
    error_name2 =  error_name.copy()
    error_log2 =  error_log.copy()
    error_name.clear()
    error_log.clear()
    a = error_count
    error_count = 0
    print("Failed URLs:")
    for i in range(0, a):
        url = error_log2[i]
        name = error_name2[i]
        try:
            print(name)
            print(url)
            response = requests.get(error_log2[i])
            with open('MODIS/' + name + '.tif', 'wb') as file:
                file.write(response.content)
        except ProxyError:
            print(name)
            print(f"ProxyError {url}")
            error_count += 1
            error_log.append(url)
            error_name.append(name)
        except requests.exceptions.SSLError:
            print(f"SSLError {url}")
            print(name)
            error_count += 1
            error_log.append(url)
            error_name.append(name)
    print(error_count)

    error_name2.clear()
    error_log2.clear()

def get_files_with_size(directory, size_kb):
    files_with_size = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath) / 1024  # convert bytes to kilobytes
            print(size)
            if size <= size_kb:
                files_with_size.append(filename.split('.')[0])
    return files_with_size

directory = r'E:\\python\\GEEpython\\MODIS'  # replace with your directory
size_kb = 1
files = get_files_with_size(directory, size_kb)
print(files)