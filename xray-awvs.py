#coding:utf-8
#coding by able403@163.com 
#暂不支持转载，如有需要请联系本人
import requests
import json
import time
import tableprint
import queue
import os
import sys
import openpyxl as ws
requests.packages.urllib3.disable_warnings()

use = '''
    use:
       pyhton3 xray-awvs13.py -f url.txt 127.0.0.1:8080
    Options:
        -f  filename     add the target to the awvs from file
    '''

class Awvs:
    def __init__(self, host, api_key,xray_proxy_ip,xray_proxy_port):
        self.host = host
        self.api_key = api_key
        self.api_header = {'X-Auth':api_key,'content-type':'application/json'}
        self.xray_proxy_ip = xray_proxy_ip
        self.xray_proxy_port = xray_proxy_port

    def add(self,url):
        data ={"targets":[{"address":url,"description":""}],"groups":[]}
        try:
            response = requests.post(self.host+"api/v1/targets/add",data=json.dumps(data),headers=self.api_header,timeout=30,verify=False)
            result = json.loads(response.content)
            target_id= result['targets'][0]['target_id']
            awvs.set_proxy(target_id)
            return target_id
        except Exception as e:
            print(str(e))
            return

    def set_proxy(self,target_id):
        url = self.host + 'api/v1/targets/'+target_id+'/configuration'
        data ={
            "scan_speed":"moderate",
            "user_agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.21 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.21",
            "case_sensitive":"auto",
            "limit_crawler_scope":"true",
            "authentication":{"enabled":"false"},
            "proxy":{"enabled":"true","protocol":"http","address":self.xray_proxy_ip,"port":self.xray_proxy_port},
            "technologies":[],
            "custom_headers":[],
            "custom_cookies":[],
         }
        try:
            #print("url: "+url)
            res = requests.patch(url, timeout=30, verify=False, headers=self.api_header,data=json.dumps(data))
            if(res.status_code == 204):
                print("proxy set success")
            else:
                print(res.status_code)
        except Exception as e:
            print (e)

    def single_scan(self,target_id):
        data = {'target_id':target_id,'profile_id':"11111111-1111-1111-1111-111111111117", 'incremental':False, 'schedule':{'disable':False,'start_date':None, 'time_sensitive':False}}
        try:
            r = requests.post(url=self.host + 'api/v1/scans', timeout=30, verify=False, headers=self.api_header, data=json.dumps(data))
            if r.status_code == 201:
                print( f' {url}scanning starting ')
        except Exception as e:
            print (e)
    def get_status(self):
        try:
            result = requests.get(self.host+"/api/v1/scans?l=20",headers=self.api_header,timeout=30,verify=False)
            results = json.loads(result.text)
            status={'processing':0,'completed':0,'in_progress':0,'Failed':0}
            for s in results["scans"]:
                if s['current_session']['status'] =='processing':
                    status['processing'] += 1
                elif s['current_session']['status'] =='completed':
                    status['completed'] += 1
                elif s['current_session']['status'] =='in progress':
                    status['in_progress'] += 1
                elif s['current_session']['status'] =='Failed':
                    status['Failed'] += 1
            return status
        except Exception as e:
            print (e)
            return False

q = queue.Queue()
def task(files):
    urls = open(files).read().splitlines()
    for url in urls:
        q.put(url)

if __name__ == '__main__':
    if len(sys.argv) < 5:
        try:
            task(str(sys.argv[2]))
            xray_proxy = sys.argv[3]
            xray_proxy_ip = xray_proxy.split(":")[0]
            xray_proxy_port = xray_proxy.split(":")[1]
            while not q.empty():
                url = q.get()
                hosts = open("hosts_api.txt").readline().strip()
                host = hosts.split(",")[0]
                api = hosts.split(",")[1]
                try:
                    awvs = Awvs(host,api,xray_proxy_ip,xray_proxy_port)
                    num_scan=int(awvs.get_status()['processing'])
                    target_id=awvs.add(url)
                    awvs.single_scan(target_id)
                    if(num_scan<6):
                        with open("add_result.txt","a+") as f:
                            f.write(url+"\n")
                        time.sleep(5)
                        continue;
                    else:
                        print('host: {}  processing: {}  completed: {}  in_progress: {}  Failed: {}  '.format(host,awvs.get_status()['processing'],awvs.get_status()['completed'],awvs.get_status()['in_progress'],awvs.get_status()['Failed']))
                        q.put(url)
                        time.sleep(300)
                except Exception as e:
                    print (e)
            print("add complete")
        except Exception as e:
            print (e)
    else:
        print(use)

