# sqlAlchemy-migrate → ridgepole 移行について - 20180614
`COMMIT:42b231b`時点（sqlalchemy）で作ったDBスキーマと同じものをridgepoleで作ろうとしてもなぜか無理。どうせスキーマ定義刷新のつもりだったので諦める

# MySQLで新db作ったときに確認すること- 20180614
- `mysql> SHOW GLOBAL VARIABLES LIKE 'chara%';`
- `mysql> SHOW VARIABLES LIKE 'chara%';`
- `alter database sanakin_develop default character set utf8;`
- `ALTER DATABASE (db_name) DEFAULT CHARACTER SET UTF8;`

# DB作成コマンド - 20180614
- `mysql> CREATE DATABASE (db_name) DEFAULT CHARACTER SET utf8;`

# DATABASEの作り方
```python
'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
      user_name,
      password,
      host_ip,
      db_name
)
```

# create_engineの使い方
```python
from sqlalchemy import create_engine
ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)
```

# session_makerの使い方
```python
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
session = Session()
```
