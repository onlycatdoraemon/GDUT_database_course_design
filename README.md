# GDUT_database_course_design
广东工业大学数据库课程设计（番剧管理系统）

## 环境配置
```docker
#安装mysql8.0（在含有docker-compose.yml的父目录下）
docker-compose up -d
#查看运行状态
docker-compose ps
```
或者在window安装mysql，本文不再赘述，goole或者bing一下就好

```bash
# 假如有anaconda就用下面的conda
conda create -n sql python=3.7
conda activate sql
pip install pymysql pyqt5 cryptography
```

```python
#运行(在运行前记得去sql_manager.py 的DatabaseManager.open_db_connection修改自己对应的数据库信息（密码端口等）)
python Run_mainUI.py
```
