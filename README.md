# GDUT_database_course_design
广东工业大学数据库课程设计（番剧管理系统）

## 环境配置
### mysql安装
```docker
#安装mysql8.0（在含有docker-compose.yml的父目录下）
docker-compose up -d
#查看运行状态
docker-compose ps
```
或者在window安装mysql，本文不再赘述，goole或者bing一下就好
### python环境安装
```bash
# 假如有anaconda就用下面的conda
conda create -n sql python=3.7
conda activate sql
pip install pymysql pyqt5 cryptography
```
### 数据库初始化
```mysql
--建立数据库，并运行anime.sql文件初始化基本表和触发器，指令参照如下
CREATE DATABASE 数据库名;
mysql -u 用户名 -p 数据库名 < /path/to/files.sql
```
### 运行
```python
#运行(在运行前记得去sql_manager.py 的DatabaseManager.open_db_connection修改自己对应的数据库信息（密码端口等）)
python Run_mainUI.py
```
