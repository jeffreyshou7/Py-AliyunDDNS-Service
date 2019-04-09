# 基于Python3.X/阿里云云解析API运用于树梅派做家庭服务器的DDNS服务
## 加入配置管理/日志管理/外网出口IP模块
## 本项目主要用于学习研究Python在linux下定时任务及将脚本注册成系统服务
## 本项目将呈现开箱即用的程度，满足广大树梅派爱好者基本所需
## 本项目依赖的库请自行安装
sudo pip3 install aliyun-python-sdk-core
sudo pip3 install aliyun-python-sdk-alidns
sudo pip3 install bs4

若运行报缺少其他库，请自行sudo pip3 install [包]
## 配置文件说明
本程序启动后会自行添加一个模板空配置文件，定义如下：
{
    "interval": "60", //轮询之间间隔，单位秒，建议900，即15分钟
    "last_ip": "",
    "last_update":"",
    "record_id":"",
    "domain":"",//需要动态解析的域名值
    "rr":"",//需要动态解析的记录（二级域名）
    "switch":0,
    "access_key_id":"", 您的阿里云api接入id
    "access_Key_secret":"",您的阿里云api接入密钥
    "region_id":"",
    "access_token":""
}

## app.log为本软件日志记录 在程序运行后会自动添加，建议先对软件运行目录进行写权限赋予