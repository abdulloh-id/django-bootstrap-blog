import pymysql

pymysql.install_as_MySQLdb()
pymysql.connections.Connection.default_auth_plugin = 'caching_sha2_password'