import pandas as pd
import sqlalchemy as sql
from scripts import utils

def get_mysql_data(uname,pwd):
    hostname="localhost"
    port="3307" # default 3306, using 3307 for the db hosted in vm
    dbname="covid-dw"
    uname=uname #"root"
    pwd=pwd #"testpassmysql"

    # create mysqlalchemy engine to connect to mysql db
    engine = sql.create_engine(
        "mysql+pymysql://{user}:{pwd}@{host}:{port}/{db}".format(
            host=hostname, db=dbname, port=port, user=uname, pwd=pwd
        )
    )

    # import data from db
    try:
        dbConn = engine.connect()
        df_s = pd.read_sql("SELECT * FROM vw_time_state_rates", dbConn)
        df_s.month = df_s.month.astype(str)
        df_c = pd.read_sql("SELECT * FROM vw_time_county_rates", dbConn)
        df_c.month = df_c.month.astype(str)
        df_d = pd.read_sql("SELECT * FROM vw_demo_severity",dbConn)
    except Exception as ex:
        print(ex)
    finally:
        dbConn.close()

    return df_s,df_c,df_d

# read in the data
df_s,df_c,df_d = get_mysql_data('root','testpassmysql')
