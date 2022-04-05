def extract_unique(df,field_name):
    '''
    extract unique values in a dataframe field to a list
    '''
    out = df[field_name].unique().tolist()
    return out

def extract_dict(df,field_names):
    '''
    extract paired values in a data frame to a map into dict
    '''
    return dict(zip(df[field_names[0]],df[field_names[1]]))

def slice_dict_n(dict,n):
    '''select every nth element from a dictionary'''
    i = 1
    out = {}
    for k in dict.keys():
        if i%n == 1:
            out[dict[k]] = dict.get(k)
        i+=1
    return out