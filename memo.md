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
