-- 文件名: anime.sql

-- 1. 出版社表
CREATE TABLE Publisher5058 (
    PublisherID VARCHAR(50) PRIMARY KEY, -- 出版社的唯一编号，支持任意字符
    Name VARCHAR(255) NOT NULL, -- 出版社名称
    ProductionCount INT DEFAULT 0 -- 该出版社制作的番剧数量
);

-- 2. 番剧表
CREATE TABLE Anime5058 (
    AnimeID VARCHAR(50) PRIMARY KEY, -- 番剧的唯一编号，支持任意字符
    Name VARCHAR(255) NOT NULL, -- 番剧名称
    Genre VARCHAR(50), -- 番剧类型
    PublisherID VARCHAR(50), -- 外键，关联到出版社表
    YearQuarter VARCHAR(20), -- 番剧的发行年份和季度
    FOREIGN KEY (PublisherID) REFERENCES Publisher5058(PublisherID) ON DELETE CASCADE -- 当删除出版社时，自动删除其关联的番剧
);

-- 3. 平台表
CREATE TABLE Platform5058 (
    PlatformID VARCHAR(50) PRIMARY KEY, -- 平台的唯一编号，支持任意字符
    Name VARCHAR(255) NOT NULL, -- 平台名称
    PurchasedAnimeCount INT DEFAULT 0, -- 平台购入的番剧数量
    UserCount INT DEFAULT 0 -- 平台的用户数量
);

-- 4. 用户表
CREATE TABLE User5058 (
    UserID VARCHAR(50) PRIMARY KEY, -- 用户的唯一编号，支持任意字符
    Username VARCHAR(225) NOT NULL, -- 用户名
    PlatformID VARCHAR(50), -- 外键，关联到平台表，表示用户所在的平台
    FollowingAnimeCount INT DEFAULT 0, -- 用户追番数量
    FOREIGN KEY (PlatformID) REFERENCES Platform5058(PlatformID) ON DELETE CASCADE -- 当删除平台时，自动删除其关联的用户
);

-- 5. 平台购入表
CREATE TABLE PlatformPurchase5058 (
    PlatformID VARCHAR(50), -- 外键，关联到平台表
    AnimeID VARCHAR(50), -- 外键，关联到番剧表
    PRIMARY KEY (PlatformID, AnimeID), -- 复合主键，确保每个平台和番剧的关系唯一
    FOREIGN KEY (PlatformID) REFERENCES Platform5058(PlatformID) ON DELETE CASCADE, -- 当删除平台时，自动删除其关联的购入记录
    FOREIGN KEY (AnimeID) REFERENCES Anime5058(AnimeID) ON DELETE CASCADE -- 当删除番剧时，自动删除其关联的购入记录
);

-- 6. 用户追番表
CREATE TABLE UserFollowing5058 (
    AnimePlatformID VARCHAR(50), -- 外键，关联到平台表，表示番剧所在的平台
    UserID VARCHAR(50), -- 外键，关联到用户表
    AnimeID VARCHAR(50), -- 外键，关联到番剧表
    PRIMARY KEY (AnimeID, UserID), -- 复合主键，确保每个用户追番的记录唯一
    FOREIGN KEY (AnimePlatformID, AnimeID) REFERENCES PlatformPurchase5058(PlatformID, AnimeID) ON DELETE CASCADE, -- 当删除平台购入番剧时，自动删除其关联的追番记录
    FOREIGN KEY (AnimeID) REFERENCES Anime5058(AnimeID) ON DELETE CASCADE, -- 当删除番剧时，自动删除其关联的追番记录
    FOREIGN KEY (UserID) REFERENCES User5058(UserID) ON DELETE CASCADE, -- 当删除用户时，自动删除其追番记录
    FOREIGN KEY (AnimePlatformID) REFERENCES Platform5058(PlatformID) ON DELETE CASCADE -- 当删除平台时，自动删除其关联的追番记录
);

-- 触发器部分
DELIMITER //

-- 动态更新 Publisher 的 ProductionCount
CREATE TRIGGER UpdateProductionCount
AFTER INSERT ON Anime5058
FOR EACH ROW
BEGIN
    UPDATE Publisher5058
    SET ProductionCount = ProductionCount + 1
    WHERE PublisherID = NEW.PublisherID;
END;
//

CREATE TRIGGER ReduceProductionCount
AFTER DELETE ON Anime5058
FOR EACH ROW
BEGIN
    UPDATE Publisher5058
    SET ProductionCount = ProductionCount - 1
    WHERE PublisherID = OLD.PublisherID;
END;
//

-- 动态更新 Platform 的 PurchasedAnimeCount
CREATE TRIGGER UpdatePurchasedAnimeCount
AFTER INSERT ON PlatformPurchase5058
FOR EACH ROW
BEGIN
    UPDATE Platform5058
    SET PurchasedAnimeCount = PurchasedAnimeCount + 1
    WHERE PlatformID = NEW.PlatformID;
END;
//

CREATE TRIGGER ReducePurchasedAnimeCount
AFTER DELETE ON PlatformPurchase5058
FOR EACH ROW
BEGIN
    UPDATE Platform5058
    SET PurchasedAnimeCount = PurchasedAnimeCount - 1
    WHERE PlatformID = OLD.PlatformID;
END;
//

-- 动态更新 platform 的UserCount
CREATE TRIGGER UpdatePlatFormUserCount
AFTER INSERT ON User5058
FOR EACH ROW
BEGIN
    UPDATE Platform5058
    SET UserCount = UserCount + 1
    WHERE PlatformID = NEW.PlatformID;
END;
//

CREATE TRIGGER ReducePlatFormUserCount
AFTER DELETE ON User5058
FOR EACH ROW
BEGIN
    UPDATE Platform5058
    SET UserCount = UserCount - 1
    WHERE PlatformID = OLD.PlatformID;
END;
//

-- 动态更新 User 的 FollowingAnimeCount
CREATE TRIGGER UpdateFollowingAnimeCount
AFTER INSERT ON UserFollowing5058
FOR EACH ROW
BEGIN
    UPDATE User5058
    SET FollowingAnimeCount = FollowingAnimeCount + 1
    WHERE UserID = NEW.UserID;
END;
//

CREATE TRIGGER ReduceFollowingAnimeCount
AFTER DELETE ON UserFollowing5058
FOR EACH ROW
BEGIN
    UPDATE User5058
    SET FollowingAnimeCount = FollowingAnimeCount - 1
    WHERE UserID = OLD.UserID;
END;
//

DELIMITER ;



-- 视图部分
-- 1. 出版社相关视图
-- 获取所有出版社
CREATE VIEW AllPublishers5058 AS
SELECT * FROM Publisher5058;

-- 获取每个出版社的番剧数量
CREATE VIEW PublisherAnimeCount5058 AS
SELECT PublisherID, COUNT(AnimeID) AS AnimeCount
FROM Anime5058
GROUP BY PublisherID;

-- 2. 番剧相关视图
-- 获取所有番剧的详细信息（包括出版社信息）
CREATE VIEW AllAnimes5058 AS
SELECT a.AnimeID, a.Name AS AnimeName, a.Genre, p.Name AS PublisherName, a.YearQuarter
FROM Anime5058 a
JOIN Publisher5058 p ON a.PublisherID = p.PublisherID;

-- 根据番剧名称模糊搜索番剧的详细信息
CREATE VIEW AnimesByName5058 AS
SELECT a.AnimeID, a.Name AS AnimeName, a.Genre, p.Name AS PublisherName, a.YearQuarter
FROM Anime5058 a
JOIN Publisher5058 p ON a.PublisherID = p.PublisherID
WHERE a.Name LIKE '%{name_keyword}%';

-- 3. 平台相关视图
-- 获取所有平台
CREATE VIEW AllPlatforms5058 AS
SELECT * FROM Platform5058;

-- 获取每个平台的用户数量
CREATE VIEW PlatformUserCount5058 AS
SELECT PlatformID, COUNT(UserID) AS UserCount
FROM User5058
GROUP BY PlatformID;

-- 4. 用户相关视图
-- 获取所有用户
CREATE VIEW AllUsers5058 AS
SELECT * FROM User5058;

-- 根据平台ID查询用户
CREATE VIEW UsersByPlatform5058 AS
SELECT * FROM User5058 WHERE PlatformID = '{platform_id}';

-- 5. 平台购入相关视图
-- 获取所有平台购入记录（包括平台和番剧信息）
CREATE VIEW AllPurchases5058 AS
SELECT pp.PlatformID, pp.AnimeID, pl.Name AS PlatformName, a.Name AS AnimeName, a.YearQuarter
FROM PlatformPurchase5058 pp
JOIN Platform5058 pl ON pp.PlatformID = pl.PlatformID
JOIN Anime5058 a ON pp.AnimeID = a.AnimeID;

-- 根据平台名称模糊搜索购入记录
CREATE VIEW PurchasesByPlatformName5058 AS
SELECT pp.PlatformID, pp.AnimeID, pl.Name AS PlatformName, a.Name AS AnimeName, a.YearQuarter
FROM PlatformPurchase5058 pp
JOIN Platform5058 pl ON pp.PlatformID = pl.PlatformID
JOIN Anime5058 a ON pp.AnimeID = a.AnimeID
WHERE pl.Name LIKE '%{platform_name_keyword}%';

-- 根据番剧名称模糊搜索购入记录
CREATE VIEW PurchasesByAnimeName5058 AS
SELECT pp.PlatformID, pp.AnimeID, pl.Name AS PlatformName, a.Name AS AnimeName, a.YearQuarter
FROM PlatformPurchase5058 pp
JOIN Platform5058 pl ON pp.PlatformID = pl.PlatformID
JOIN Anime5058 a ON pp.AnimeID = a.AnimeID
WHERE a.Name LIKE '%{anime_name_keyword}%';

-- 6. 用户追番相关视图
-- 获取所有用户追番记录（包括平台、用户、番剧信息）
CREATE VIEW AllFollowings5058 AS
SELECT uf.AnimePlatformID, uf.UserID, uf.AnimeID, pl.Name AS PlatformName, u.Username AS UserName, a.Name AS AnimeName
FROM UserFollowing5058 uf
JOIN Platform5058 pl ON uf.AnimePlatformID = pl.PlatformID
JOIN User5058 u ON uf.UserID = u.UserID
JOIN Anime5058 a ON uf.AnimeID = a.AnimeID;

-- 根据平台名称模糊搜索追番记录
CREATE VIEW FollowingsByPlatformName5058 AS
SELECT uf.AnimePlatformID, uf.UserID, uf.AnimeID, pl.Name AS PlatformName, u.Username AS UserName, a.Name AS AnimeName
FROM UserFollowing5058 uf
JOIN Platform5058 pl ON uf.AnimePlatformID = pl.PlatformID
JOIN User5058 u ON uf.UserID = u.UserID
JOIN Anime5058 a ON uf.AnimeID = a.AnimeID
WHERE pl.Name LIKE '%{platform_name_keyword}%';

-- 根据番剧名称模糊搜索追番记录
CREATE VIEW FollowingsByAnimeName5058 AS
SELECT uf.AnimePlatformID, uf.UserID, uf.AnimeID, pl.Name AS PlatformName, u.Username AS UserName, a.Name AS AnimeName
FROM UserFollowing5058 uf
JOIN Platform5058 pl ON uf.AnimePlatformID = pl.PlatformID
JOIN User5058 u ON uf.UserID = u.UserID
JOIN Anime5058 a ON uf.AnimeID = a.AnimeID
WHERE a.Name LIKE '%{anime_name_keyword}%';

-- 根据用户名模糊搜索追番记录
CREATE VIEW FollowingsByUserName5058 AS
SELECT uf.AnimePlatformID, uf.UserID, uf.AnimeID, pl.Name AS PlatformName, u.Username AS UserName, a.Name AS AnimeName
FROM UserFollowing5058 uf
JOIN Platform5058 pl ON uf.AnimePlatformID = pl.PlatformID
JOIN User5058 u ON uf.UserID = u.UserID
JOIN Anime5058 a ON uf.AnimeID = a.AnimeID
WHERE u.Username LIKE '%{user_name_keyword}%';