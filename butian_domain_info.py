import requests
import re
import tldextract

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
    'Cookie': "your butian' Cookie",
}

# 功能：针对不同的方法，获取网页内容并返回结果
def get_body_info(method, url, data):
    if method == 'GET':
        response = requests.get(url, headers=headers)
        return response.text
    elif method == 'POST':
        response = requests.post(url, headers=headers, data=data)
        return response.json()
    else:
        print('method error')

# 功能：针对POST请求获取的json数据，获取page_total,company_id,company_name并返回结果
def get_company_info(body_info):
    company_info = {}
    page_total = body_info['data']['count']
    for item in body_info['data']['list']:
        company_id = item['company_id']
        company_name = item['company_name']
        company_info[company_id] = company_name
    return page_total, company_info

# 功能：针对company_id进行GET请求,获取对应的域名并返回结果
def get_domain(company_id):
    url = "https://www.butian.net/Loo/submit?cid={}".format(company_id)
    body_info = get_body_info("GET", url, "")
    result = re.findall('分隔" value="(.*?)"', body_info)
    if len(result) == 0:
        return "", ""
    else:
        subdomain = result[0]
        domain = tldextract.extract(subdomain).registered_domain
        return subdomain, domain

# 功能：针对页数，获取公司相关信息
def get_company_list(page):
    url = "https://www.butian.net/Reward/pub"
    data = {
        's': '1',
        'p': page,
        'token': '',
    }
    body_info = get_body_info("POST", url, data)
    page_total, company_info = get_company_info(body_info)
    for cid in company_info:
        subdomain, domain = get_domain(cid)
        company_name = company_info[cid]
        butian_info = "{},{},{},{}".format(cid, company_name, subdomain, domain)
        print(butian_info)
        save_company_info(butian_info)
    return page_total

# 功能：保存爬取的公司信息
def save_company_info(info):
    with open('butian_info.csv', 'a+', encoding='utf-8') as f:
        f.writelines(info + '\n')

if __name__ == '__main__':
    print('[+] Get page:', 1)
    page_total = get_company_list(1)
    for page in range(2, page_total+1):
        print('[+] Get page:--------------------------------', page)
        get_company_list(page)

