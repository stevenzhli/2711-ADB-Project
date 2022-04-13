from neo4j import GraphDatabase
import pandas as pd

driver = GraphDatabase.driver(uri="bolt://localhost:7687", auth = ("neo4j", "testpassneo4j"))

session = driver.session()

def Vw_demo_severity():
    query = '''
        MATCH (f:fact), (d:demography{demography_id:f.demography_id})

        RETURN  f.demography_id,
            d.race,
            d.age,
            d.sex,
            sum(f.case_total) as case_total,
            sum(f.out_total) as out_total,
            sum(f.out_severe) as out_servere,
            sum(f.out_death) as out_death
    '''
    results = session.run(query)
    df = pd.DataFrame(results)
    return df

def Vw_time_county():
    query = '''
        MATCH (f:fact), (l:location{location_id:f.location_id})
        RETURN
                f.month,
                l.county_id,
                l.state_id,
                l.county,
                sum(f.case_total) as case_total,
                sum(f.out_total) as out_total,
                sum(f.out_severe) as out_servere,
                sum(f.out_death) as out_death
    '''
    results = session.run(query)
    df = pd.DataFrame(results)
    return df

def Vw_time_state():
    query = '''
        MATCH (f:fact), (l:location{location_id:f.location_id})
        RETURN
                f.month,
                l.state_id,
                l.state,
                sum(f.case_total) as case_total,
                sum(f.out_total) as out_total,
                sum(f.out_severe) as out_servere,
                sum(f.out_death) as out_death
    '''
    results = session.run(query)
    df = pd.DataFrame(results)
    return df

def get_neo4j_data():
    df_s = Vw_time_state()
    df_c = Vw_time_county()
    df_d = Vw_demo_severity()
    return df_s,df_c,df_d

