class DevelopmentConfig:

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8".format(**{
        "user": "test",
        "password": "test",
        "host": "db",
        "db_name": "test"
    })
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


Config = DevelopmentConfig
