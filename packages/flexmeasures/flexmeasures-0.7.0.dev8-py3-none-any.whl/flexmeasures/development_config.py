import pandas as pd

pd.set_option('display.max_columns', None)

SECURITY_PASSWORD_SALT = '$2b$1327VlhOJrcPjFYdxWix07pNO'
# SECURITY_PASSWORD_SALT = "10b$1927Vc3OJrCnjFYdw0ixs7pEO"

# SQLALCHEMY_DATABASE_URI = "postgresql://a1:testtest@127.0.0.1/a1_demo"
SQLALCHEMY_DATABASE_URI = "postgresql://flexmeasures:flexmeasures@127.0.0.1/flexmeasures"
# SQLALCHEMY_ECHO = True

MAIL_SERVER = "w01a109a.kasserver.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = "felix@seita.nl"
MAIL_DEFAULT_SENDER = ("FlexMeasures", "no-reply@seita.nl")
MAIL_PASSWORD = "pce,18,WM"
DARK_SKY_API_KEY = "38d0bf8e538f023f053f42fc16638daa"
FLEX_MEASURES_MODE = "demo"
FLEX_MEASURES_PUBLIC_DEMO = True
FLEX_MEASURES_TASK_CHECK_AUTH_TOKEN = "dev-token"
LOGGING_LEVEL = "INFO"

# Staging: 0
# Demo: 1
# Live: 2
# Play: 3
# Nic dev: 10
# Felix dev: 11
FLEX_MEASURES_REDIS_URL = "52.144.45.80"
FLEX_MEASURES_REDIS_PORT = 6379
FLEX_MEASURES_REDIS_DB_NR = 11  # Redis per default has 16 databases, [0-15]
FLEX_MEASURES_REDIS_PASSWORD = "D0lEyyf4QCKZ"
RQ_DASHBOARD_POLL_INTERVAL = 10000

PA_API_TOKEN = "a408def6b1a34d64e0eeb9cd0039b28af9c143b5"
