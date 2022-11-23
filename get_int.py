#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
def get_internships(field, degree, region):
    df = pd.read_excel('data.xlsx', sheet_name=field)
    if field == 'school':
        return df
    else:
        return df.loc[(df['region'] == region) & (df['degree'].str.contains(degree))]