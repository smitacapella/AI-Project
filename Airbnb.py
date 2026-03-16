''' pip install pandas 
pip install numpy streamlit matplotlib seaborn pandasql scikit-learn
pip install openai '''

import pandas as pd
import numpy as np
import pandasql as ps
from sqlalchemy import text 
from openai import OpenAI
import requests
#import streamlit as st


'''Data Cleaning'''
def file_clean(file):
    df=pd.read_csv(file)
    df = df.drop_duplicates()
    df= df.dropna(subset =['price'])
    #print(df.head())
    df['price'] = df['price'].astype(float)
    # print(df['price'])
    # print(df.count())
    # print(df.describe())
    # print(df.columns)
    df = df.fillna('0')
    return df

#file_clean('listings.csv')

'''Data Analysis'''
def avg_price_by_neighbourhood(df):
    #df=pd.read_csv(file)
    #print('neighbourhood')
    price_by_neighbourhood_mean=df.groupby('neighbourhood')['price'].mean()
    price_by_neighbourhood_median=df.groupby('neighbourhood')['price'].median()
    #print(price_by_neighbourhood_mean)
    return price_by_neighbourhood_mean
#avg_price_by_neighbourhood('listings.csv')

def avg_price_by_room_type(df):
    #df= pd.read_csv(file)
    #print('room type')
    # price_by_room_type= df.groupby(['room_type','neighbourhood'])['price'].mean()
    price_by_room_type= df.groupby(['room_type'])['price'].mean()
    #print(price_by_room_type)
    #print('room type cnt mean')
    price_by_room_typecnt_mean= df.groupby(['room_type'])['price'].agg("mean").reset_index()
    return price_by_room_typecnt_mean
#avg_price_by_room_type('listings.csv')

def top_prices_by_neighbourhood(df):
    #df = pd.read_csv(file)
    #print('top prices by neighbourhood')
    top_prices_by_neighbourhood = df.groupby('neighbourhood')['price'].max()
    return top_prices_by_neighbourhood
#top_prices_by_neighbourhood('listings.csv')

def top_revenue_by_room_type(df):
    #df = pd.read_csv(file)
    #print('max revenue by room type')
    df['revenue']= df['price'] * df['availability_365']
    top_revenue_by_room_type = df.groupby('room_type')['revenue'].max()
    top_revenue_by_room_type = df.groupby(['room_type','neighbourhood'])['revenue'].agg(["max","count"]).reset_index()
    return top_revenue_by_room_type.sort_values(by ='max',ascending=False)
#top_revenue_by_room_type('listings.csv')


df = file_clean('listings.csv')
unique_neighbourhood = df["neighbourhood"].unique()
print(unique_neighbourhood)
for i,n in enumerate(unique_neighbourhood): #enumerate will provide index and value of the unique neighbourhoods
    print(n)
    if i ==2: # 0, 1, 2
        break

unique_neighbourhood_s = pd.DataFrame(unique_neighbourhood)
#print(unique_neighbourhood_s.iloc[3,0])
#print(df.loc[5,'price'])



'''sql queries'''
def run_query(query, df):
    result = ps.sqldf(query, {"df": df})
    return result

# query = """
# SELECT neighbourhood, AVG(price) AS avgprice
# FROM df
# GROUP BY neighbourhood
# """
# df=pd.read_csv('listings.csv')
# print(run_query(query,df) )


#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

#client = OpenAI(api_key="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")
def generate_sql_query(question):
    prompt = f"""
    Convert the question into a SQL query.

    IMPORTANT:
    Return ONLY the SQL query.
    Do NOT include explanation.
    Do NOT include markdown.
    Do NOT include text.
    
    table : df 
    # columns:
    # price
    # neighbourhood
    # room_type
    # number_of_reviews
    # availability_365
    question = {question}
    """
 
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream":False
        }
    )
    
    #return response.choices[0].messages.content
    #return response.json()['choices'][0]['message']['content']
    data = response.json()
    return data["response"]
    #return response.json()
    
def generate_python_code(question):
    prompt = f"""
    Convert the question into a python code.

    IMPORTANT:
    Return ONLY the python code.
    Do NOT include explanation.
    Do NOT include markdown.
    Do NOT include text.
    
    table : df 
    # columns:
    # price
    # neighbourhood
    # room_type
    # number_of_reviews
    # availability_365
    question = {question}
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream":False
        }
    )
    
    #return response.choices[0].messages.content
    #return response.json()['choices'][0]['message']['content']
    data = response.json()
    return data["response"]
    #return response.json()

#print(generate_sql_query("What is top neigbourhood by price group by aggregation?"))

