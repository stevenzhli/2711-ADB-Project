def extract_unique(df,field_name):
    """
    extract unique values in a dataframe field to a sorted list
    """
    out = df[field_name].unique().tolist()
    out.sort()
    return out