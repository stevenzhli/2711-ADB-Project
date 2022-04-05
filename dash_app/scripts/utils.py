def extract_unique(df,field_name):
    '''
    extract unique values in a dataframe field to a sorted list
    '''
    out = df[field_name].unique().tolist()
    out.sort()
    return out

def extract_dict(df,field_names):
    '''
    extract paired values in a data frame to a map into dict
    '''
    return dict(zip(df[field_names[0]],df[field_names[1]]))

def calc_upper(number):
    '''
    find an upper upper bound for plotting
    '''