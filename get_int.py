#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from parse import update_deadline

def get_internships(field, degree, region):
    df = pd.read_excel('data.xlsx', sheet_name=field)
    df.loc[ df["name"] == "Undergraduate Summer Research Fellowships (UGSRF) by APS", "end"] = update_deadline()
    if field == 'school':
        return df
    else:
        return df.loc[(df['region'] == region) & (df['degree'].str.contains(degree))]