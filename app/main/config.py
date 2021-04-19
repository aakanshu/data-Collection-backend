import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dfsvsjnaklvrejnksx32543fcz 3c csd")
    DEBUG = False
    RESTX_VALIDATE = True
    PERSIST_AUTHORIZATION = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES = {
        "user": os.getenv("DB_USERNAME"),
        "pw": os.getenv("DB_PASSWORD"),
        "db": os.getenv("DB_NAME"),
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
    }

    DB_CONNECTION_URI = (
        "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
    )

class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = Config.DB_CONNECTION_URI
    ISSUER = os.getenv("ISSUER")
    ALG = os.getenv("ALG")
    AUDIENCE = os.getenv("AUDIENCE")

class LocalConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    POSTGRES = {
        "user": "dcappadmin",
        "pw": "eb77060df9537c485852a79e",
        "db": "dcapppostgres",
        "host": "10.12.170.197",
        "port": 5432,
    }
    SQLALCHEMY_DATABASE_URI = (
        # "postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s" % POSTGRES
        "postgresql://localhost/collection"  # Config.DB_CONNECTION_URI
    )
    ISSUER = os.getenv("ISSUER")
    ALG = os.getenv("ALG")
    AUDIENCE = os.getenv("AUDIENCE")

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://localhost/ds-marketplace-test"  # Config.DB_CONNECTION_URI
    )

class StageConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        Config.DB_CONNECTION_URI
        + "?sslmode=verify-ca&sslrootcert=certs/rds-ca-2019-root.pem"
    )
    ISSUER = os.getenv("ISSUER")
    ALG = os.getenv("ALG")
    AUDIENCE = os.getenv("AUDIENCE")

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = (
        Config.DB_CONNECTION_URI
        + "?sslmode=verify-ca&sslrootcert=certs/rds-ca-2019-root.pem"
    )
    ISSUER = os.getenv("ISSUER")
    ALG = os.getenv("ALG")
    AUDIENCE = os.getenv("AUDIENCE")


config_by_name = dict(
    dev=DevConfig,
    development=LocalConfig,
    test=TestingConfig,
    stage=StageConfig,
    prod=ProdConfig,
    local=LocalConfig,
)

key = Config.SECRET_KEY
token_expiry = 3600
