import os
import pymysql
from typing import List, Tuple
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DatabaseManager:
    @staticmethod
    def open_db_connection():
        """
        创建并返回数据库连接
        """
        try:
            connection = pymysql.connect(
                host="localhost",        # 数据库主机地址
                user="root",             # 数据库用户名
                password="your_password",   # 数据库密码
                database="your_database_name",        # 数据库名称
                port=3306,               # MySQL 端口（默认3306）
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # 返回字典格式
            )
            logging.info("数据库连接成功")
            return connection
        except pymysql.MySQLError as e:
            logging.error(f"数据库连接失败: {e}")
            raise

    @staticmethod
    def execute_query(query: str, params: Tuple = ()) -> List[dict]:
        """
        执行查询并返回结果
        """
        try:
            with DatabaseManager.open_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    results = cursor.fetchall()
                    logging.info(f"查询成功，返回{len(results)}条记录")
                    return results
        except pymysql.MySQLError as e:
            logging.error(f"查询失败: {e}")
            return []

    @staticmethod
    def execute_modify(query: str, params: Tuple = ()) -> bool:
        """
        执行插入、更新、删除操作
        """
        try:
            with DatabaseManager.open_db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                connection.commit()
                logging.info(f"操作成功，影响{cursor.rowcount}行")
                return True
        except pymysql.MySQLError as e:
            logging.error(f"操作失败: {e}")
            return False

    @staticmethod
    def init_data(sql_file_path: str) -> bool:
        """
        通过 SQL 文件初始化数据库（逐行读取并执行）
        :param sql_file_path: SQL 文件的路径
        :return: 是否成功
        """
        # 检查文件是否存在
        if not os.path.exists(sql_file_path):
            logging.error(f"SQL文件 {sql_file_path} 不存在")
            return False

        try:
            # 打开 SQL 文件
            with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
                # 连接到数据库
                connection = DatabaseManager.open_db_connection()
                cursor = connection.cursor()

                # 逐行读取 SQL 文件
                sql_statement = ""
                for line in sql_file:
                    # 跳过注释行和空行
                    line = line.strip()
                    if line.startswith("--") or not line:
                        continue

                    # 拼接 SQL 语句
                    sql_statement += line + " "

                    # 如果遇到分号，表示一个完整的 SQL 语句
                    if ";" in line:
                        try:
                            # 执行 SQL 语句
                            cursor.execute(sql_statement)
                            logging.info(f"执行成功: {sql_statement}")
                        except pymysql.MySQLError as e:
                            logging.error(f"执行失败: {sql_statement}，错误: {e}")
                            connection.rollback()
                            return False

                        # 重置 SQL 语句
                        sql_statement = ""

                # 提交事务
                connection.commit()
                logging.info("数据库初始化成功")
                return True

        except Exception as e:
            logging.error(f"执行SQL文件时出错: {e}")
            return False
        finally:
            # 关闭数据库连接
            if 'connection' in locals() and connection:
                connection.close()

    @staticmethod
    def delete_all() -> bool:
        """
        清空数据库中所有表的数据，按照外键约束的顺序删除
        :return: 是否成功
        """
        try:
            connection = DatabaseManager.open_db_connection()
            # 获取游标
            with connection.cursor() as cursor:
                # 禁用外键检查
                cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")

                # 按照从子表到父表的顺序删除数据
                tables = [
                    "UserFollowing5058",  # 最底层的子表
                    "PlatformPurchase5058",
                    "User5058",
                    "Anime5058",
                    "Platform5058",
                    "Publisher5058"  # 最顶层的父表
                ]
                for table in tables:
                    cursor.execute(f"DELETE FROM {table};")
                    logging.info(f"已清空表 {table} 的数据")
                # 启用外键检查
                cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
            # 提交事务
            connection.commit()
            logging.info("所有表的数据已清空")
            return True
        except pymysql.MySQLError as e:
            logging.error(f"清空数据时出错: {e}")
            return False
        finally:
            # 关闭数据库连接
            if 'connection' in locals() and connection:
                connection.close()

class PublisherManager:
    @staticmethod
    def add_publisher(publisher_id: str, name: str) -> bool:
        """
        添加出版社
        """
        query = """
            INSERT INTO Publisher5058 (PublisherID, Name)
            VALUES (%s, %s)
        """
        return DatabaseManager.execute_modify(query, (publisher_id, name))

    @staticmethod
    def delete_publisher_by_id(publisher_id: str) -> bool:
        """
        根据ID删除出版社
        """
        query = "DELETE FROM Publisher5058 WHERE PublisherID = %s"
        return DatabaseManager.execute_modify(query, (publisher_id,))

    @staticmethod
    def delete_publisher_by_name(publisher_name: str) -> bool:
        """
        根据名称删除出版社
        """
        query = "DELETE FROM Publisher5058 WHERE Name = %s"
        return DatabaseManager.execute_modify(query, (publisher_name,))

    @staticmethod
    def update_publisher(publisher_id: str, name: str = None) -> bool:
        """
        更新出版社信息
        """
        updates = []
        params = []
        if name:
            updates.append("Name = %s")
            params.append(name)

        if not updates:
            return False

        query = f"UPDATE Publisher5058 SET {', '.join(updates)} WHERE PublisherID = %s"
        params.append(publisher_id)
        return DatabaseManager.execute_modify(query, tuple(params))

    @staticmethod
    def get_all_publishers() -> List[dict]:
        """
        获取所有出版社
        """
        query = "SELECT * FROM Publisher5058"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def get_publisher_by_id(publisher_id: str) -> List[dict]:
        """
        根据ID查询出版社
        """
        query = "SELECT * FROM Publisher5058 WHERE PublisherID = %s"
        return DatabaseManager.execute_query(query, (publisher_id,))

    @staticmethod
    def get_publishers_by_name(name_keyword: str) -> List[dict]:
        """
        根据出版社名称进行模糊搜索
        """
        query = "SELECT * FROM Publisher5058 WHERE Name LIKE %s"
        # 使用通配符 % 进行模糊匹配
        keyword = f"%{name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

class AnimeManager:
    @staticmethod
    def add_anime(anime_id: str, name: str, genre: str, publisher_id: str, year_quarter: str) -> bool:
        """
        添加番剧
        """
        query = """
            INSERT INTO Anime5058 (AnimeID, Name, Genre, PublisherID, YearQuarter)
            VALUES (%s, %s, %s, %s, %s)
        """
        return DatabaseManager.execute_modify(query, (anime_id, name, genre, publisher_id, year_quarter))

    @staticmethod
    def delete_anime_id(anime_id: str) -> bool:
        """
        删除番剧
        """
        query = "DELETE FROM Anime5058 WHERE AnimeID = %s"
        return DatabaseManager.execute_modify(query, (anime_id,))

    @staticmethod
    def delete_anime_name(anime_name: str) -> bool:
        """
        删除番剧
        """
        query = "DELETE FROM Anime5058 WHERE Name = %s"
        return DatabaseManager.execute_modify(query, (anime_name,))
    @staticmethod
    def update_anime(anime_id: str, name: str = None, genre: str = None, publisher_id: str = None, year_quarter: str = None) -> bool:
        """
        更新番剧信息
        """
        updates = []
        params = []
        if name:
            updates.append("Name = %s")
            params.append(name)
        if genre:
            updates.append("Genre = %s")
            params.append(genre)
        if publisher_id:
            updates.append("PublisherID = %s")
            params.append(publisher_id)
        if year_quarter:
            updates.append("YearQuarter = %s")
            params.append(year_quarter)

        if not updates:
            return False

        query = f"UPDATE Anime5058 SET {', '.join(updates)} WHERE AnimeID = %s"
        params.append(anime_id)
        return DatabaseManager.execute_modify(query, tuple(params))

    @staticmethod
    def get_all_animes() -> List[dict]:
        """
        获取所有番剧
        """
        query = "SELECT * FROM Anime5058"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def get_anime_by_id(anime_id: str) -> List[dict]:
        """
        根据ID查询番剧
        """
        query = "SELECT * FROM Anime5058 WHERE AnimeID = %s"
        return DatabaseManager.execute_query(query, (anime_id,))

    @staticmethod
    def get_anime_by_name(name_keyword: str) -> List[dict]:
        """
        根据番剧名称进行模糊搜索
        """
        query = "SELECT * FROM Anime5058 WHERE Name LIKE %s"
        # 使用通配符 % 进行模糊匹配
        keyword = f"%{name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

class PlatformManager:
    @staticmethod
    def add_platform(platform_id: str, name: str) -> bool:
        """
        添加平台
        """
        query = """
            INSERT INTO Platform5058 (PlatformID, Name)
            VALUES (%s, %s)
        """
        return DatabaseManager.execute_modify(query, (platform_id, name))

    @staticmethod
    def delete_platform_by_id(platform_id: str) -> bool:
        """
        根据ID删除平台
        """
        query = "DELETE FROM Platform5058 WHERE PlatformID = %s"
        return DatabaseManager.execute_modify(query, (platform_id,))

    @staticmethod
    def delete_platform_by_name(platform_name: str) -> bool:
        """
        根据名称删除平台
        """
        query = "DELETE FROM Platform5058 WHERE Name = %s"
        return DatabaseManager.execute_modify(query, (platform_name,))

    @staticmethod
    def update_platform(platform_id: str, name: str = None) -> bool:
        """
        更新平台信息
        """
        updates = []
        params = []
        if name:
            updates.append("Name = %s")
            params.append(name)

        if not updates:
            return False  # 如果没有需要更新的字段，返回 False

        query = f"UPDATE Platform5058 SET {', '.join(updates)} WHERE PlatformID = %s"
        params.append(platform_id)
        return DatabaseManager.execute_modify(query, tuple(params))

    @staticmethod
    def get_all_platforms() -> List[dict]:
        """
        获取所有平台
        """
        query = "SELECT * FROM Platform5058"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def get_platform_by_id(platform_id: str) -> List[dict]:
        """
        根据ID查询平台
        """
        query = "SELECT * FROM Platform5058 WHERE PlatformID = %s"
        return DatabaseManager.execute_query(query, (platform_id,))

    @staticmethod
    def get_platforms_by_name(name_keyword: str) -> List[dict]:
        """
        根据平台名称进行模糊搜索
        """
        query = "SELECT * FROM Platform5058 WHERE Name LIKE %s"
        keyword = f"%{name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

class UserManager:
    @staticmethod
    def add_user(user_id: str, username: str, platform_id: str) -> bool:
        """
        添加用户
        """
        query = """
            INSERT INTO User5058 (UserID, Username, PlatformID)
            VALUES (%s, %s, %s)
        """
        return DatabaseManager.execute_modify(query, (user_id, username, platform_id))

    @staticmethod
    def delete_user_by_id(user_id: str) -> bool:
        """
        删除用户
        """
        query = "DELETE FROM User5058 WHERE UserID = %s"
        return DatabaseManager.execute_modify(query, (user_id,))

    @staticmethod
    def delete_user_by_name(user_name: str) -> bool:
        """
        删除用户
        """
        query = "DELETE FROM User5058 WHERE Username = %s"
        return DatabaseManager.execute_modify(query, (user_name,))

    @staticmethod
    def update_user(user_id: str, username: str = None, platform_id: str = None) -> bool:
        """
        更新用户信息
        """
        updates = []
        params = []
        if username:
            updates.append("Username = %s")
            params.append(username)
        if platform_id is not None:
            updates.append("PlatformID = %s")
            params.append(platform_id)

        if not updates:
            return False

        query = f"UPDATE User5058 SET {', '.join(updates)} WHERE UserID = %s"
        params.append(user_id)
        return DatabaseManager.execute_modify(query, tuple(params))

    @staticmethod
    def get_user_by_id(user_id: str) -> List[dict]:
        """
        根据用户ID查询用户信息
        """
        query = "SELECT * FROM User5058 WHERE UserID = %s"
        return DatabaseManager.execute_query(query, (user_id,))

    @staticmethod
    def get_users_by_platform(platform_id: str) -> List[dict]:
        """
        根据平台ID查询用户
        """
        query = "SELECT * FROM User5058 WHERE PlatformID = %s"
        return DatabaseManager.execute_query(query, (platform_id,))

    @staticmethod
    def get_users_by_username(username_keyword: str) -> List[dict]:
        """
        根据用户名进行模糊搜索
        """
        query = "SELECT * FROM User5058 WHERE Username LIKE %s"
        keyword = f"%{username_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

    @staticmethod
    def get_all_users() -> List[dict]:
        """
        获取所有用户
        """
        query = "SELECT * FROM User5058"
        return DatabaseManager.execute_query(query)

    @staticmethod
    def get_user_by_username(username_keyword: str) -> List[dict]:
        """
        根据用户名进行搜索
        """
        query = "SELECT * FROM User5058 WHERE Username = %s"
        keyword = f"%{username_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

class PlatformPurchaseManager:
    @staticmethod
    def add_purchase(platform_id: str, anime_id: str) -> bool:
        """
        添加平台购入记录
        """
        query = """
            INSERT INTO PlatformPurchase5058 (PlatformID, AnimeID)
            VALUES (%s, %s)
        """
        return DatabaseManager.execute_modify(query, (platform_id, anime_id))

    @staticmethod
    def delete_purchase(platform_id: str, anime_id: str) -> bool:
        """
        删除平台购入记录
        """
        query = """
            DELETE FROM PlatformPurchase5058
            WHERE PlatformID = %s AND AnimeID = %s
        """
        return DatabaseManager.execute_modify(query, (platform_id, anime_id))

    @staticmethod
    def get_purchases_by_platform_name(platform_name_keyword: str) -> List[dict]:
        """
        根据平台名字的部分关键字查询购入的番剧记录
        返回结果包含平台名字和番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, Anime5058.Name AS AnimeName, Anime5058.YearQuarter AS YearQuarter
            FROM PlatformPurchase5058
            JOIN Platform5058 ON PlatformPurchase5058.PlatformID = Platform5058.PlatformID
            JOIN Anime5058 ON PlatformPurchase5058.AnimeID = Anime5058.AnimeID
            WHERE Platform5058.Name LIKE %s
        """
        keyword = f"%{platform_name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))
    @staticmethod
    def get_purchases_by_anime_name(anime_name_keyword: str) -> List[dict]:
        """
        根据番剧名字的部分关键字查询在哪些平台被购入
        返回结果包含平台名字和番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, Anime5058.Name AS AnimeName, Anime5058.YearQuarter AS YearQuarter
            FROM PlatformPurchase5058
            JOIN Platform5058 ON PlatformPurchase5058.PlatformID = Platform5058.PlatformID
            JOIN Anime5058 ON PlatformPurchase5058.AnimeID = Anime5058.AnimeID
            WHERE Anime5058.Name LIKE %s
        """
        keyword = f"%{anime_name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

    @staticmethod
    def get_all_purchases() -> List[dict]:
        """
        获取所有平台购入记录
        返回结果包含平台名字和番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, Anime5058.Name AS AnimeName, Anime5058.YearQuarter AS YearQuarter
            FROM PlatformPurchase5058
            JOIN Platform5058 ON PlatformPurchase5058.PlatformID = Platform5058.PlatformID
            JOIN Anime5058 ON PlatformPurchase5058.AnimeID = Anime5058.AnimeID
        """
        return DatabaseManager.execute_query(query)
    @staticmethod
    def get_records(platform_id: str, anime_id: str) -> List[dict]:
        """
        根据平台ID和番剧ID查询记录
        """
        query = """
            SELECT *
            FROM PlatformPurchase5058
            WHERE PlatformID = %s AND AnimeID = %s
        """
        return DatabaseManager.execute_query(query, (platform_id, anime_id,))

class UserFollowingManager:
    @staticmethod
    def add_following(anime_platform_id: str, user_id: str, anime_id: str) -> bool:
        """
        添加用户追番记录
        """
        query = """
            INSERT INTO UserFollowing5058 (AnimePlatformID, UserID, AnimeID)
            VALUES (%s, %s, %s)
        """
        return DatabaseManager.execute_modify(query, (anime_platform_id, user_id, anime_id))

    @staticmethod
    def delete_following(user_id: str, anime_id: str) -> bool:
        """
        删除用户追番记录
        """
        query = """
            DELETE FROM UserFollowing5058
            WHERE UserID = %s AND AnimeID = %s
        """
        return DatabaseManager.execute_modify(query, (user_id, anime_id))

    @staticmethod
    def get_followings_by_platform_name(platform_name_keyword: str) -> List[dict]:
        """
        根据平台名字的部分关键字查询用户追番记录
        返回结果包含平台名字、用户名字、番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, User5058.UserID AS UserID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, User5058.Username AS UserName, Anime5058.Name AS AnimeName
            FROM UserFollowing5058
            JOIN Platform5058 ON UserFollowing5058.AnimePlatformID = Platform5058.PlatformID
            JOIN User5058 ON UserFollowing5058.UserID = User5058.UserID
            JOIN Anime5058 ON UserFollowing5058.AnimeID = Anime5058.AnimeID
            WHERE Platform5058.Name LIKE %s
        """
        keyword = f"%{platform_name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

    @staticmethod
    def get_followings_by_anime_name(anime_name_keyword: str) -> List[dict]:
        """
        根据番剧名字的部分关键字查询用户追番记录
        返回结果包含平台名字、用户名字、番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, User5058.UserID AS UserID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, User5058.Username AS UserName, Anime5058.Name AS AnimeName
            FROM UserFollowing5058
            JOIN Platform5058 ON UserFollowing5058.AnimePlatformID = Platform5058.PlatformID
            JOIN User5058 ON UserFollowing5058.UserID = User5058.UserID
            JOIN Anime5058 ON UserFollowing5058.AnimeID = Anime5058.AnimeID
            WHERE Anime5058.Name LIKE %s
        """
        keyword = f"%{anime_name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

    @staticmethod
    def get_followings_by_user_name(user_name_keyword: str) -> List[dict]:
        """
        根据用户名的部分关键字查询用户追番记录
        返回结果包含平台名字、用户名字、番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, User5058.UserID AS UserID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, User5058.Username AS UserName, Anime5058.Name AS AnimeName
            FROM UserFollowing5058
            JOIN Platform5058 ON UserFollowing5058.AnimePlatformID = Platform5058.PlatformID
            JOIN User5058 ON UserFollowing5058.UserID = User5058.UserID
            JOIN Anime5058 ON UserFollowing5058.AnimeID = Anime5058.AnimeID
            WHERE User5058.Username LIKE %s
        """
        keyword = f"%{user_name_keyword}%"
        return DatabaseManager.execute_query(query, (keyword,))

    @staticmethod
    def find_following(user_id: str, anime_id: str) -> bool:
        """
        删除用户追番记录
        """
        query = """
            SELECT * FROM UserFollowing5058
            WHERE UserID = %s AND AnimeID = %s
        """
        return DatabaseManager.execute_query(query, (user_id, anime_id))

    @staticmethod
    def get_all_followings() -> List[dict]:
        """
        查询全部用户追番记录
        返回结果包含平台名字、用户名字、番剧名字
        """
        query = """
            SELECT Platform5058.PlatformID AS PlatformID, User5058.UserID AS UserID, Anime5058.AnimeID AS AnimeID, Platform5058.Name AS PlatformName, User5058.Username AS UserName, Anime5058.Name AS AnimeName
            FROM UserFollowing5058
            JOIN Platform5058 ON UserFollowing5058.AnimePlatformID = Platform5058.PlatformID
            JOIN User5058 ON UserFollowing5058.UserID = User5058.UserID
            JOIN Anime5058 ON UserFollowing5058.AnimeID = Anime5058.AnimeID
        """
        return DatabaseManager.execute_query(query)


