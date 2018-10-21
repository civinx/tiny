# tiny

## 设计思路
长网址的数量远远多于5位数字+字母的短链接

所以长网址->短链接的映射会有碰撞

考虑直接把长网址存入数据库中获得一个自增主键

将主键转化为[0-9 a-z A-Z]的62进制5位数，并存入数据库短网址字段

由于主键是唯一的，所以不同的长网址对应的短网址都是不同的

生成前在数据库中查找长网址是否已经存在，如果存在就不再予以生成短网址，而是返回之前保存的短网址记录

这样可以保证同一个长网址生成短网址的幂等性

当获取短网址,如域名/[0-9 a-z A-Z]{5}的格式时，提取短网址部分的参数，查找数据库对应的长网址，进行转跳。

后端采用 Django REST framework 在 8000 端口上提供API

前端采用 Angular6 向后端提交POST，并获取JSON中的短网址
## 数据库
![](http://oj8wl05o7.bkt.clouddn.com/api_record500.png)
## API
```
POST /tiny/
```

接收:

```
{
	"old_url": ""
}
```
old_url: string(500) # 长网址

正常返回:

```
{
	"tiny_url": "",
	"old_url": ""
}
```
tiny_url: string(5) # 生成的短网址

old_url: string(500) # 将转换的长网址

异常返回:

```
{
    "detail": ""
}
```

detail: string() # 错误信息

当请求的长网址是当前域名本身的子域名时

```
{
    "old_url": [
        "Cannot convert the url under the domain itself!"
    ]
}
```

## 运行方法
* 安装 npm 和 Angular
* 详见 https://angular.io/guide/quickstart
* 修改 front/src/record.service.ts中的recordUrl 为服务器的域名:8000/tiny/
* 使用ng build 将 Angular项目打包为 dist
* 将dist文件和后台tiny转移到服务器
* 在服务器安装python3.6以及pipenv
* 切换到Django目录下（有Pipfile和Pipfile.lock）的地方
* pipenv install 以安装需要的包
* pipenv shell 进入虚拟环境
* 配置uwsgi，新建mysite_uwsgi.ini比如

# 测试
* 使用Postman编写请求和查看返回的Json
* GET http://localhost:8000/tiny 使用Django REST framework自带的图形界面测试

 ```
[uwsgi]
socket = :8001
chdir = /home/tiny/tiny 
module = tiny.wsgi 
processes = 4  
threads = 2 
virtualenv = /root/.local/share/virtualenvs/rango_website-e68KS5mW/
 ```
virtualenv路径可以通过 pipenv --venv 获得
* 配置Nginx，使80端口指向dist目录中的index.html
* 配置Nginx，使8000端口指向uwsgi的8001端口
* Nginx service start 启动Nginx
* screen uwsgi path/mysite_uwsgi.ini 启动uwsgi并挂起
## 运行实例
http://47.100.57.37