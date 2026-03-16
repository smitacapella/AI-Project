import streamlit as st
import pandas as pd
from Airbnb import file_clean
from Airbnb import run_query
from Airbnb import generate_sql_query
from Airbnb import generate_python_code
from Airbnb import avg_price_by_neighbourhood
from Airbnb import avg_price_by_room_type
from Airbnb import top_prices_by_neighbourhood
from Airbnb import top_revenue_by_room_type
import matplotlib.pyplot as plt

st.markdown("""
<div style="
background-color:#1f77b4;
padding:10px;
border-radius:8px;
">
<h2 style="color:white; text-align:center;">
Airbnb AI & Data Analysis
</h2>
</div>
""", unsafe_allow_html=True)
#st.title('Airbnb AI & Data Analysis')

upload_file = st.file_uploader("Upload the file",type=['csv'])

#df = file_clean("listings.csv")
df = pd.read_csv(upload_file)
question = st.text_input('Ask a question about the Airbnb dataset:')
if question:
    sql_query= generate_sql_query(question)
    st.write('Generated SQL Query:')
    st.code(sql_query)
    
    python_code= generate_python_code(question)
    python_code = python_code.replace("```python", "").replace("```", "").strip()
    python_code = python_code.replace("...", "")
    st.write('Generated Python Code:')
    st.code(python_code)
    #result1= eval(python_code)
    #st.write('Python Code Result:')
    #st.dataframe(result1)
    local_vars={'df': df,
                'plt': plt
                }
    exec(python_code, {}, local_vars)

    result= run_query(sql_query, df)
    st.write('Query Result:')
    st.dataframe(result)
    #result1 =st.dataframe(result)
    #st.bar_chart(result1, x=result1.columns[0], y=result1.columns[0])
    numeric_cols = result.select_dtypes(include='number').columns

    if len(numeric_cols) > 1:
        st.bar_chart(result, x=result.columns[0], y=numeric_cols[1])
    else:
        st.bar_chart(result, x=result.columns[0], y=numeric_cols[0])
    
    
'''     col1, col2,col3 = st.columns(3)
    with col1:
        st.subheader("Top Revenue per room type")
        st.sidebar.header("Filters")
        selected_room_type =st.sidebar.selectbox("Room type",df['room_type'].unique())
        filterred_df = df[df['room_type']==selected_room_type]
        st.dataframe(top_revenue_by_room_type(filterred_df))
    with col2:
        st.subheader("Top Prices per Neighbourhood")
        st.dataframe(top_prices_by_neighbourhood(df))
    with col3:
        st.subheader("Average Price by Room Type")
        avg_price = avg_price_by_room_type(df)
        #print(avg_price.columns[1])
        st.dataframe(avg_price)
        st.bar_chart(data=avg_price,x=avg_price.columns[0],y=avg_price.columns[1]) '''