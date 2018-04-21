from anakin import env

# 書式 → dialect+driver://username:password@host:port/database
# ソース : https://qiita.com/t2kojima/items/5c7f9978f98b1a897d73

DATABASE = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
    env.USER_NAME,
    env.PASSWORD,
    env.HOST_IP,
    env.DB_NAME
)
