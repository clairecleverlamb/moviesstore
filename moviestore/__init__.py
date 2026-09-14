try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    # SQLite does not need PyMySQL; install it on PythonAnywhere when using MySQL.
    pass