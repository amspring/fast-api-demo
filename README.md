基于 FastApi 研发的一个基础Demo Api架构, 带验证Token信息 

#### 相关知识
```text
框架: FastApi 
缓存: Redis, 
数据库: Mysql, 
Token: Jwt

```

#### 已开发功能
> 登录验证
> > 账户登录  ->  获取 access_token <br>
> > 密码修改 <br>
> > 添加登录 <br>
> > 删除登录 <br>

> 用户
> > 用户列表<br>
> > 添加用户<br>
> > 编辑用户<br>
> > 删除用户

> 轮播图
> > 轮播图列表<br>
> > 添加轮播图<br>
> > 编辑轮播图<br>
> > 删除轮播图

#### 软件架构
```text


app                 -- 代码
    endpoints       -- 路由, 接收参数
        __init__.py -- 每增加一个模块, 需要这里注册
    repositories    -- DB, 与数据库交互, 每增加一个模块, 需要注册 __init__.py
        __init__.py -- 每增加一个模块, 需要这里注册
    services        -- 业务处理, 每增加一个模块, 需要注册 __init__.py
        __init__.py -- 每增加一个模块, 需要这里注册
    __init__.py     -- 注册
    conf.py         -- 读取config.yml
    containers.py   -- 依赖注入
    db.py           -- 数据库配置
    exceptions.py   -- 异常
    logger.py       -- 日志
    models.py       -- models
    redis.py        -- redis
    resp.py         -- 返回初始化
    schemas.py      -- 参数验证, 如果参数过多, 建议拆分, 继承公告参数
    security.py     -- 加密解密, token
    utils.py        -- 公共方法
config              -- 配置
    api.ini         --supversior 配置
    config.dev.yml  --测试开发配置文件
    config.prod.yml --生产环境配置文件
logs                --日志
.gitignore          --git 忽略文件
boot.sh             --生产环境部署脚本
cmd.py              --启动文件
config.py           --生产环境配置
config.yml          --配置文件
docker-compose.yml  --docker compose
Dockerfile          --dockerfile
README.md           --文档
requirements.txt    --依赖包

```


#### 版本, 当前版本为3.10.x
```shell
python 3.10.x
mysql 8.x
```

#### 依赖环境安装
```shell
pip install -r requirements.txt
```

#### 配置复制
```shell
cp config/config.dev.yml config.yml
```

#### 修改配置
```text
新建数据库, 配置信息填充
```

#### 数据库初始化
```shell
    0. 开发环境下, config.yml 的 app.debug: True的话, 启动时候数据库没表的自动建表
    
    1. 初始化数据库
    # 生成初始化数据配置, 生成后会生成一个aerich.ini文件和一个migrations文件夹
    aerich init -t app.db.TORTOISE_ORM
    # 初始化数据库
    aerich init-db
    
    2. 已经初始化过的, 修改迁移
    # 修改数据模型后生成迁移文件, 在后面加 --name=xxx, 可以指定文件名
    aerich migrate
    # 执行迁移
    aerich upgrade
    # 回到上一个版本
    aerich downgrade
    # 查看历史迁移记录
    aerich history
    # 查看形成当前版本的迁移记录文件
    aerich heads
```

#### 开发环境
```shell
python cmd.py 
or 
uvicorn cmd:app --reload --host 0.0.0.0 --port 8888
```

####  生产环境
```text
cd /path/demo
touch .env
echo "PROJECT_ENV=\"dev\"" > .env
chmod +x boot.sh
. boot.sh
```

#### model 相关文档:
```text
https://tortoise-orm.readthedocs.io/en/latest/migration.html#init-db
https://tortoise-orm.readthedocs.io/en/latest/reference.html
```
[tortoise-orm](https://tortoise-orm.readthedocs.io/en/latest/reference.html)

