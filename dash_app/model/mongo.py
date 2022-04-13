import sys
import pymongo
import pandas as pd

def get_mongo_data():
    myclient = pymongo.MongoClient('mongodb://localhost:27017/')
    dbname = "2711project"
    dblist = myclient.list_database_names()
    mydb = myclient[dbname]
    collist = mydb.list_collection_names()
    print(collist)

    inputcol = mydb["time_state_view"]
    df_s=[]
    for item in inputcol.find():
        row=[]
        case_total=item["case_total"]
        out_death=item["out_death"]
        out_severe=item["out_severe"]
        out_total=item["out_total"]
        population=item["population"]
        for x in item:
            row.append(item[x])
        if  population!="NaN":
            row.append(int(case_total)/(int(population)*1.0))
        else:
            row.append(0)
        if int(out_total)>0:
            row.append(int(out_death)/(int(out_total)*1.0))
        else:
            row.append(0)
        if int(out_total)>0:
            row.append(int(out_severe) / (int(out_total) * 1.0))
        else:
            row.append(0)
        if int(out_severe)>0:
            row.append(int(out_death) / (int(out_severe) * 1.0))
        else:
            row.append(0)
        df_s.append(row)
    df_s_dataframe=pd.DataFrame(list(df_s),columns=["_id" , "case_total" , "month","out_death","out_severe","out_total","population","state","state_id","pop_infect_rate_100","case_death_rate_100","case_severe_rate","severe_death_rate"]).to_string(index=False)


    inputcol = mydb["time_county_view"]
    df_c = []
    for item in inputcol.find():
        row = []
        case_total = item["case_total"]
        out_death = item["out_death"]
        out_severe = item["out_severe"]
        out_total = item["out_total"]
        population = item["population"]
        for x in item:
            row.append(item[x])
        if population != "NaN":
            row.append(int(case_total) / (int(population) * 1.0))
        else:
            row.append(0)
        if int(out_total) > 0:
            row.append(int(out_death) / (int(out_total) * 1.0))
        else:
            row.append(0)
        if int(out_total) > 0:
            row.append(int(out_severe) / (int(out_total) * 1.0))
        else:
            row.append(0)
        if int(out_severe) > 0:
            row.append(int(out_death) / (int(out_severe) * 1.0))
        else:
            row.append(0)
        df_c.append(row)
    df_c_dataframe = pd.DataFrame(list(df_c),
                                  columns=["_id", "case_total", "county","county_id","month", "out_death", "out_severe", "out_total",
                                           "population", "state", "state_id", "pop_infect_rate_100",
                                           "case_death_rate_100", "case_severe_rate", "severe_death_rate"]).to_string(
        index=False)

    inputcol = mydb["demo_view"]
    df_d = []
    for item in inputcol.find():
        row = []

        for x in item:
            row.append(item[x])

        df_d.append(row)
    df_d_dataframe = pd.DataFrame(list(df_d),
                                  columns=["_id", "age","case_total",  "out_death", "out_severe", "out_total",
                                           "race", "sex"]).to_string(
        index=False)

    return df_s_dataframe,df_c_dataframe,df_d_dataframe

df_s,df_c,df_d=get_mongo_data()

