import configparser


class MySQLConfig(object):
    host: str
    user: str
    password: str
    database: str

    def __init__(self, mysql_host: str, mysql_user: str, mysql_password: str, mysql_database: str):
        self.host = mysql_host
        self.user = mysql_user
        self.password = mysql_password
        self.database = mysql_database


class Config(object):
    token: str
    secret: str
    address: str
    game: str
    mysql: MySQLConfig
    support_guild: int

    def __init__(self, address: str, game: str, token: str, secret: str, mysql_host: str, mysql_user: str,
                 mysql_password: str,
                 mysql_database: str, support_guild: int):
        self.token = token
        self.address = address
        self.secret = secret
        self.game = game
        self.support_guild = support_guild
        self.mysql = MySQLConfig(mysql_host, mysql_user, mysql_password, mysql_database)


def parse_config(file_name: str) -> Config:
    config = configparser.ConfigParser()

    config.read(file_name)

    general = config['general']
    discord = config['discord']
    mysql = config['mysql']
    print(file_name)

    return Config(general['address'], discord['game'], discord['TOKEN'], discord['SECRET'], mysql['host'],
                  mysql['user'], mysql['password'], mysql['database'], int(discord['support_guild']))
