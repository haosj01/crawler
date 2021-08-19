# 安装&升级openssl
下载编译安装
```
# wget https://www.openssl.org/source/openssl-1.1.1a.tar.gz

# tar -zxvf openssl-1.1.1a.tar.gz

# cd openssl-1.1.1a 
# ./config --prefix=/usr/local/openssl no-zlib

# echo $?
0
# make && make install
```
备份原配置文件
```
# mv /usr/bin/openssl /usr/bin/openssl.bak
# mv /usr/include/openssl/ /usr/include/openssl.bak
```
新版设置
```
# ln -s /usr/local/openssl/include/openssl /usr/include/openssl
# ln -s /usr/local/openssl/lib/libssl.so.1.1 /usr/local/lib64/libssl.so (可能没有)
# ln -s  /usr/local/openssl/bin/openssl /usr/bin/openssl
```
修改系统配置，写入openssl库文件的搜索路径
```
# echo '/usr/local/openssl/lib' >> /etc/ld.so.conf
```
使修改后的/etc/ld.so.conf生效
```
# ldconfig -v
```
查看版本
```
# openssl version
OpenSSL 1.1.1a  20 Nov 2018
```

#liunx环境 python3部署
下载python3安装包
```
在Linux下新建一个目录，用于存放下载的安装包，接着进入python37目录下，再通过 wget 命令下载。
wget https://www.python.org/ftp/python/3.9.0/Python-3.9.0.tgz
```
解压
```
tar -zxvf Python-3.9.0.tgz
```
安装相关依赖centos
```
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel 
libdb4-devel libpcap-devel xz-devel libffi-devel
```
进入解压目录，进行编译和安装(根据需要自定义目录)
```
cd Python-3.9.0
./configure --prefix=/usr/local/bin/python3 --with-openssl=/usr/local/openssl 或者
./configure --prefix=/usr/local/bin/python3 --with-ssl
make&&make install
```
删除原先的命令，并建立新的软连接
```
rm -rf /usr/bin/python3
ln -s /usr/local/bin/python3/bin/python3.9 /usr/bin/python3
```
配置PATH环境变量
```
 vim /etc/profile不是root用户加sudo 
 加入export PATH=$PATH:/usr/local/bin/python3/bin
 激活source /etc/profile
```
检查并验证
```
 python3 -V
```
Pip源设置（使用清华源）
```
pip install pip -U
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```
使用requirements.txt恢复环境
```
pip3 install -r requirements.txt
```
线上后台执行程序
```
启动
nohup python3 run.py prod > run.log 2>&1 &
查看端口
```
