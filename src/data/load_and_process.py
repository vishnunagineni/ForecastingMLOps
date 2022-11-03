import pandas as pd
import re
from datetime import datetime
import os
import argparse
from get_data import read_params,get_data


def transform_data(config_path):
    #df=pd.read_excel(path,header=3)
    #replacing the values
    df = get_data(config_path)
    df = df.replace(['Saturday','Sunday','Holiday',"A",'E1', 'E2', 'F2', 'F1','F3', 'G1', 'G2', 'I0', 'G0', 'N0', 'M0', 'M3B', 'S0', 'R0','IT'],0)
    df = df.replace(['P','B2', 'B1', 'C1', 'D2', 'C2', 'D1','A2','A1'],1)
    df = df.replace(["OA ","AO "],1)
    
    #Work Location Tagging
    for i in range(len(work_tag)):
        df=df.replace(work_tag.loc[i,"Work location"],work_tag.loc[i,"Tag"])
    
    #Department Tagging
    for i in range(len(dep_tag)):
        df=df.replace(dep_tag.loc[i,"Department"],dep_tag.loc[i,"Tag"])
    
    #Changing Date format
    for col in df.columns:
        date = re.search(r'\d{4}-\d{2}-\d{2}', str(col))
        if date:
            res = datetime.strptime(date.group(), '%Y-%m-%d').date()
            month = res.strftime("%b-%d")
            df.rename(columns={col:month},inplace=True)
    #Dropping unnecessary columns
    df=df.drop(["Employee ID","Employee Name","Designation","No. of Days Work from Office","No. of Days Work from Anywhere/Home","Grade"],axis=1)
    
    #Aggregating the rows
    new_df = pd.DataFrame(df.groupby(["Work location","Department"]).agg("sum")).reset_index()
    date_cols=new_df.columns[2:].tolist()
    #Unpivoting the columns into rows
    final_df = pd.melt(new_df,id_vars=["Work location","Department"],value_vars=[i for i in date_cols],var_name='Date',value_name='No.of Presents')
    return final_df