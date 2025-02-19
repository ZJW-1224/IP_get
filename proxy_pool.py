import requests
from bs4 import BeautifulSoup
import pymysql

# create database sql
'''
    CREATE DATABASE Proxy_pool01;
'''

#create table sql
''' USE Proxy_pool01;
    CREATE TABLE ip_addresses (
  id INT(11) NOT NULL AUTO_INCREMENT,
  ip_address VARCHAR(255) NOT NULL,
  port INT(11) NOT NULL,
  PRIMARY KEY (id)
);'''

#check data
'''
USE DATABASE Proxytest;
SELECT * FROM ip_addresses;
'''
#del data from table
'''
TRUNCATE TABLE ip_addresses;
'''

class proxy_pool:
    
    def crawl_proxy():
        # Connect to MySQL database
        mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="Proxy_pool01"
        )

        # Make HTTP request and extract data
        for i in range(0,3):
            i = i+2
            # url = "https://www.89ip.cn/index_%s.html" % i
            url = "http://www.ip3366.net/?stype=1&page=%s" % i
            # url = "https://www.kuaidaili.com/free/intr/%s/" % i
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            table = soup.find("table", attrs={"class": "table table-bordered table-striped"})
            # print(soup)
            # Store data in MySQL database
            for row in table.tbody.find_all("tr"):
                cells = row.find_all("td")
                ip = cells[0].text.strip()
                port = cells[1].text.strip()
                
                # Insert data into MySQL database
                cursor = mydb.cursor()
                sql = "INSERT INTO ip_addresses (ip_address, port) VALUES (%s, %s)"
                val = (ip, port)
                cursor.execute(sql, val)
                mydb.commit()
                print(f"Inserted {ip}:{port} into MySQL database")
            
    def get_proxy():
        # Connect to MySQL database
        mydb = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="Proxy_pool01"
        )

        # Retrieve data from MySQL database
        cursor = mydb.cursor()
        sql = "SELECT ip_address, port FROM ip_addresses"
        cursor.execute(sql)
        results = cursor.fetchall()

        # Format data as list of proxies
        proxies = []
        for result in results:
            proxy = f"{result[0]}:{result[1]}"
            proxies.append(proxy)

        return proxies
    
    def check_proxy():
        # 从get_proxy()函数获取代理IP列表
        proxies = proxy_pool.get_proxy()
        # print(proxies)
        # 设置请求头信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }

        # 遍历代理IP列表，测试可用性
        for proxy in proxies:
            try:
                # 设置代理IP和端口号
                proxies = {
                    "http": "http://" + proxy,
                }
                # print(proxies)
                # 发送请求
                response = requests.get("https://proxy.ip3366.net/free/", proxies=proxies, headers=headers, timeout=10)
                print(response)

                # 输出响应状态码
                print(proxy, response.status_code)
                
            except:
                # 输出异常信息
                print(proxy, "failed")
                
if __name__ == "__main__":
    proxy_pool.crawl_proxy()
    proxy_pool.check_proxy()