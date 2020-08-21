# xray-awvs
## 介绍
 awvs+xray结合扫描的小脚本，简单实用，可能是目前最方便的扫描脚本了，适用于批量扫描，考虑到同一台vps部署的awvs即使是进行crawl only 扫描也会相当吃资源，所以限定同时最多能进行6个目标同时crawl，当然如果是本地机器运行可以自行调整参数，如果各位大大愿意点个start，我会尽快更新自动登录、自动获取api_key的功能



## 用法：
自行安装好awvs，并生成apikey，填写到host_api.txt中,
xray需要手动设置被动扫描的监听模式：

    ./xray webscan --listen 0.0.0.0:8888 --html-output test.html

代理IP地址跟端口要对应awvs，然后运行脚本:

    pyhton3 xray-awvs13.py -f url.txt 127.0.0.1:8888

扫描结束，自行ctrl+C 结束xray的扫描，就可以得到扫描结果
