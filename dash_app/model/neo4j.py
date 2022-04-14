import pandas as pd
from py2neo import Graph

def Vw_time_state(session):
    query = '''MATCH(n:vw_time_state) RETURN *'''
    result = session.run(query).data()
    df = pd.DataFrame.from_dict(dict(session.run(query).to_data_frame().n),orient='index')
    return df

def Vw_time_county(session):
    query = '''MATCH(n:vw_time_county) RETURN *'''
    result = session.run(query).data
    df = pd.DataFrame.from_dict(dict(session.run(query).to_data_frame().n),orient='index')
    return df

def Vw_demo_severity(session):
    query = '''MATCH(n:vw_demo_severity) RETURN *'''
    result = session.run(query).data
    df = pd.DataFrame.from_dict(dict(session.run(query).to_data_frame().n),orient='index')
    return df

def get_neo4j_data():

    session = Graph(uri="bolt://localhost:7687", auth = ("neo4j", "testpassneo4j"))

    df_s = Vw_time_state(session)
    df_c = Vw_time_county(session)
    df_d = Vw_demo_severity(session)

    df_s.month = df_s.month.str[0:10]
    df_s = df_s.astype({'population':'float','case_total':'float','out_death':'int','out_severe':'int','out_total':'int'})
    df_s['pop_infect_rate'] = df_s.case_total/df_s.population
    df_s['case_death_rate'] = df_s.out_death/df_s.out_total
    df_s['case_severe_rate'] = df_s.out_severe/df_s.out_total
    df_s['case_death_rate'] = df_s.out_death/df_s.out_severe

    df_c.month = df_c.month.str[0:10]
    df_c = df_c.astype({'population':'float','case_total':'float','out_death':'int','out_severe':'int','out_total':'int'})
    df_c['pop_infect_rate'] = df_c.case_total/df_c.population
    df_c['case_death_rate'] = df_c.out_death/df_c.out_total
    df_c['case_severe_rate'] = df_c.out_severe/df_c.out_total
    df_c['case_death_rate'] = df_c.out_death/df_c.out_severe
    df_c.county_id = df_c.state_id.str.zfill(2) + df_c.county_id.str.zfill(3)

    df_d = df_d.astype({'case_total':'int','out_death':'int','out_severe':'int','out_total':'int'})
    df_d.race = df_d.race.fillna('Unknown')

    return df_s,df_c,df_d