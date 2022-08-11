class Config:
    SECRET_KEY = 'jefferson30302220'


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'jefferson'
    MYSQL_PASSWORD = '30302220'
    MYSQL_DB = 'companydb'


config = {
    'development': DevelopmentConfig
}
