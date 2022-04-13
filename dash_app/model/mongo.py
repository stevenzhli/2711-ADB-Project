import pymongo
import pandas as pd

def get_mongo_data():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    dbname = "2711project"
    dblist = myclient.list_database_names()
    mydb = myclient[dbname]

    df_s = pd.DataFrame(list(mydb["time_state_view"].find()))
    df_s.drop('_id',axis=1,inplace=True)
    df_s.month = df_s.month.str[0:10]
    df_s = df_s.astype({'population':'float','case_total':'float','out_death':'int','out_severe':'int','out_total':'int'})
    df_s['pop_infect_rate'] = df_s.case_total/df_s.population
    df_s['case_death_rate'] = df_s.out_death/df_s.out_total
    df_s['case_severe_rate'] = df_s.out_severe/df_s.out_total
    df_s['case_death_rate'] = df_s.out_death/df_s.out_severe

    df_c = pd.DataFrame(list(mydb["time_county_view"].find()))
    df_c.drop('_id',axis=1,inplace=True)
    df_c.month = df_c.month.str[0:10]
    df_c['county_id'] = df_c.state_id.str.zfill(2) + df_c.county_id.str.zfill(3)
    df_c = df_c.astype({'population':'float','case_total':'float','out_death':'int','out_severe':'int','out_total':'int'})
    df_c['pop_infect_rate'] = df_c.case_total/df_c.population
    df_c['case_death_rate'] = df_c.out_death/df_c.out_total
    df_c['case_severe_rate'] = df_c.out_severe/df_c.out_total
    df_c['case_death_rate'] = df_c.out_death/df_c.out_severe

    df_d = pd.DataFrame(list(mydb["demo_view"].find()))
    df_d.drop('_id',axis=1,inplace=True)
    df_d = df_d.astype({'case_total':'int','out_death':'int','out_severe':'int','out_total':'int'})
    df_d.race = df_d.race.fillna('Unknown')
    return df_s,df_c,df_d

df_s,df_c,df_d = get_mongo_data()
# df_s.to_hdf("cache/mongo.hdf",key='df_s',mode='a')
# df_c.to_hdf("cache/mongo.hdf",key='df_c',mode='a')
# df_d.to_hdf("cache/mongo.hdf",key='df_d',mode='a')
