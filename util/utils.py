import pandas as pd
import sqlalchemy as sql

def extract_unique(df,field_name):
    """
    extract unique values in a dataframe field to a sorted list
    """
    out = df[field_name].unique().tolist()
    out.sort()
    return out

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
        df_c = pd.read_sql("SELECT * FROM vw_time_county_rates", dbConn)
        df_d = pd.read_sql("SELECT * FROM vw_demo_severity",dbConn)
    except Exception as ex:
        print(ex)
    dbConn.close()

    return df_s,df_c,df_d
