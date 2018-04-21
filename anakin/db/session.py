from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from anakin.constants import DATABASE

ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=True
)

Session = sessionmaker(bind=ENGINE)
