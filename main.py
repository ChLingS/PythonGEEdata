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

def get_files_with_size(directory, size_kb):
    files_with_size = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            size = os.path.getsize(filepath) / 1024  # convert bytes to kilobytes
            print(size)
            if size <= size_kb:
                files_with_size.append(filename.split('.')[0])
                os.remove(filepath)
    return files_with_size


# 打开文件
zhibiao = ['dewpoint_temperature_2m', 'temperature_2m',
              'surface_solar_radiation_downwards_sum', 'surface_runoff_sum',
              'total_evaporation_sum', 'u_component_of_wind_10m', 'v_component_of_wind_10m',
              'surface_pressure', 'total_precipitation_sum','surface_sensible_heat_flux_sum','surface_latent_heat_flux_sum']
zhibiaosim = ['wd', 'ldwd', 'fs', 'qz', 'zz', 'Uf', 'Vf', 'qy', 'js','gr','qr']

# mark = 2
for mark in range(0,len(zhibiao)):
    biaoshi = zhibiaosim[mark]

    namelist = []

    new_folder = biaoshi+'_2'
    path = "./"
    if os.path.exists(new_folder):
        print("文件夹已经存在")
        # continue
    # 使用os模块创建新文件夹
    else:
        os.mkdir(os.path.join(path, new_folder))

    num = 0

    for i in range(1980,1999):
        # print(i)
        for j in range(1,13):
            # print(str(i)+'_'+str(j)+"_"+biaoshi)
            namelist.append(str(i)+'_'+str(j)+"_"+biaoshi+'.tif')
    # print(len(namelist))
    error_count = 0
    error_log = []
    error_name = []
    print(zhibiao[mark]+'.csv')
    with open(zhibiao[mark]+'.csv', 'r') as csvfile:
        # 创建csv阅读器
        csvreader = csv.reader(csvfile)
        # 逐行读取
        for row in csvreader:
            url = row[1]
            if (url[0] != 'n'):
                try:
                    if (num > 227):
                        continue
                    elif find_string_in_filenames(biaoshi+'_2', namelist[num]):
                        num+=1
                        continue
                    else:
                        response = requests.get(url)
                        with open(biaoshi+'_2/' + namelist[num], 'wb') as file:
                            file.write(response.content)
                        print(namelist[num])
                    print(num)
                except ProxyError:
                    print(f"Failed to download from {url}")
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
        error_name2 = error_name.copy()
        error_log2 = error_log.copy()
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
                with open(biaoshi+'_2/' + name, 'wb') as file:
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
    directory = biaoshi+'_2'  # replace with your directory
    size_kb = 1
    files = get_files_with_size(directory, size_kb)
    print(files)





