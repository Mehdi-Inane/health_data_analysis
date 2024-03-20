import pandas as pd



def count_variable(df,target_name,group = None):
    """
    df : Dataframe
    group : dictionary of variable names (keys) and desired values value {col_name : [value]}, if list contains
            more than one element then it is treated as an or statement
    target_name : name of column to count (render)
    Returns the count for the different non Nan values of target_name for the defined group in the dataframe + the average count for each value
    """
    sub_df = df.copy()
    if group : 
        for key in group.keys():
            sub_df = sub_df[sub_df[key].isin(group[key])]
    counts = sub_df[target_name].value_counts().to_dict()
    values = df[target_name].dropna().unique()
    #Computing averages
    for value in values:
        counts[str(value) + ' Average'] = counts[value] / len(sub_df)
    return counts

def get_groups(df,target_name,groups):
    """
    df : Dataframe
    groups : list of dicts where each dict is variable names (keys) and desired values value {col_name : [value]}, if list contains
            more than one element then it is treated as an or statement
    target_name : name of columns to count (render)
    Returns a dataframe with values for each group in a row
    """
    list_of_dicts = []
    for group in groups : 
        list_of_dicts.append(count_variable(df,target_name,group))
    return list_dict_to_df(list_of_dicts)

def list_dict_to_df(list_of_dicts):
    return pd.DataFrame(list_of_dicts)

def types_to_ints(primitive_df_types,column,values):
    d_type = primitive_df_types[column]
    if d_type == 'int64' or 'object':
        app = int
    else:
        app == float
    
    return [app(value) for value in values]





def main():
    filename = 'ALLPOURTALEAUCROISE2.xlsx'
    path = 'data/'
    df = pd.read_excel(path +filename)
    target_name = 'Dermatite atopique / Eczema'
    group = {'SEXE':[1]}
    print(count_variable(df,target_name,group))


if __name__ == "__main__":
    main()