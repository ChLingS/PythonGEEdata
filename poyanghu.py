import requests
import concurrent.futures

headers = {
    'Token':'Bearer eyJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJlY2hpc2FuIiwic3ViIjoiYWRtaW4iLCJpYXQiOjE3MDUzMDQwMzgsImV4cCI6MTcwNzg5NjAzOH0.pzjZCyIJGoVxDPMePU36uOIThMGnhMnzuGtadCnqLuMRr_vbSM_LD9UfbtRurvaTicnHmWxwYa6rIfEQlxDTKA'
}
url = r"http://171.34.76.171:8880/zhsd-merge-pyh/" \
      r"pyh-station/monitorVideoRecord/queryAllVideoRecordByType?" \
      r"timeS=2023-10-01%2000%3A00%3A00&timeE=2024-01-15%2023%3A59%3A59&recordType=0" \
      r"&id=2&start=1&limit=100"
response = requests.get(url, headers=headers)
res = response.json()['data']


def datadown(i):
    downurl = res[i]['recordPath']
    response = requests.get(downurl)
    print(res[i]['name'])
    with open(r"F:/东鄱阳湖资料/" + res[i]['name'], 'wb') as file:
        file.write(response.content)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(datadown, i): i for i in range(0, 101)}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))