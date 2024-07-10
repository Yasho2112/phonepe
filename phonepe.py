import streamlit as st
from PIL import Image 
from streamlit_option_menu import option_menu
from PIL import Image
import os
import json
import subprocess
import plotly.express as px
import pandas as pd
import streamlit_option_menu
import sqlite3
import requests
import mysql.connector


st.set_page_config(layout="wide")
st.title(":green[PHONEPE PULSE SECURE AND DATA VISUALIZATION]")

# SQL Connection:
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='12345678',
    port='3307',
    database='phonepe'
)
mycursor = mydb.cursor()

#with st.sidebar: 
SELECT = option_menu(
    menu_title = None,
    options = ["VISUALIZATION","Search","Basic insights","Contact"],
    icons =["bar-chart","search","house","toggles","at"],
    default_index=2,
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "white","size":"cover"},
        "icon": {"color": "black", "font-size": "20px"},
        "nav-link": {"font-size": "20px", "text-align": "center", "margin": "-2px", "--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"},}
    )


if SELECT == "VISUALIZATION":
#Step 1:Load the GeoJSON data from the provided URL
    geojson_url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(geojson_url)
    geojson_data=response.json()
    data=pd.DataFrame({
        'State':[   
            'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana','Himachal Pradesh',
            'Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland',
            'Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura','Uttar Pradesh','Uttarkhand',
            'West Bengal','Andaman and Nicobar islands','chandigarh','Dadra and Nagar Haveli and Daman and Diu','Lakshwadeep','Delhi',
            'Puducherry','Jammu & Kashmir','Ladakh'],
        'Transaction_amount':[
            60790077.57437308,1845307.4673655091,4936862.200688562,33999413.87739952,7350624.274461515,520105.642400422,
            6318864759.888066,9745924809.851494,1145307.4473655000,66465337.511485815,1361967204.9193478,45786439.71799916,
            7861967253.9100000,30782831245.6586,232157389.7914803,580648.3434132106,2368711.975892641,299016.7345620737,
            7621288195.565702,83873893.96204324,342809667.5935513,4823943.542263939,456157389.7914946,357356020.669816,
            6080959.882836086,489890.3434132234,787157123.7914908,4327784678.7808099,927250.7143707818,258257612.7914389,
            10767803.999610368,2417434.2729015187,127324.6279709443,7726519.367758205,113767.09768193656,992737.2376073576]
})

     
#Step 2: create the chloropleth map
    fig_choropleth=px.choropleth(
        data,
        geojson=geojson_data,
        featureidkey='properties.ST_NM',    
        locations='State',
        color='Transaction_amount',
        hover_name='State',
        color_continuous_scale='turbo',
        title='Total Transaction Amount by State',
        labels={'Transaction_amount':'Transaction Amount'}
)
#Update goes to fit bounds and make geo elements invisible
    fig_choropleth.update_geos(fitbounds="locations",visible=False)
#Show the figure
    fig_choropleth.show()

if SELECT == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--","Top 10 states based on year and amount of transaction","Least 10 states based on type and amount of transaction",
               "Top 10 mobile brands based on percentage of transaction","Top 10 Registered-users based on States and District(pincode)",
               "Top 10 Districts based on states and amount of transaction","Least 10 Districts based on states and amount of transaction",
               "Least 10 registered-users based on Districts and states","Top 10 transactions_type based on states and transaction_amount"]
    select = st.selectbox("Select the option",options)
    if select=="Top 10 states based on year and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,transaction_amount,Year,Quarter FROM top_trans GROUP BY State,transaction_amount,Year,Quarter ORDER BY transaction_amount DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','transaction_amount','Year','Quarter'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="State",y="transaction_amount")
    elif select=="Least 10 states based on type and amount of transaction":
        mycursor.execute("SELECT DISTINCT State,transaction_amount,Year,Quarter FROM Top_trans GROUP BY State,transaction_amount,Year,Quarter ORDER BY transaction_amount ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','transaction_amount','Year','Quater'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 states based on type and amount of transaction")
            st.bar_chart(data=df,x="State",y="transaction_amount")
    elif select=="Top 10 mobile brands based on percentage of transaction":
        mycursor.execute("SELECT DISTINCT brands,Percentage FROM Aggre_user GROUP BY brands,Percentage ORDER BY Percentage DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['brands','Percentage'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 mobile brands based on percentage of transaction")
            st.bar_chart(data=df,x="brands",y="Percentage")
    elif select=="Top 10 Registered-users based on States and District(pincode)":
        mycursor.execute("SELECT DISTINCT State,District,RegisteredUser FROM top_user GROUP BY State,District,RegisteredUser ORDER BY RegisteredUser DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','RegisteredUser'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Registered-users based on States and District(pincode)")
            st.bar_chart(data=df,x="State",y="RegisteredUser")
    elif select=="Top 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT state,map_district,map_amount FROM  Map_trans GROUP BY state,map_district,map_amount ORDER BY map_amount DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['state','map_district','map_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,x="state",y="map_amount")
    elif select=="Least 10 Districts based on states and amount of transaction":
        mycursor.execute("SELECT DISTINCT state,map_district,map_amount FROM  Map_trans GROUP BY state,map_district,map_amount ORDER BY map_amount ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['state','map_district','map_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 Districts based on states and amount of transaction")
            st.bar_chart(data=df,x="state",y="map_amount")
    elif select=="Least 10 registered-users based on Districts and states":
        mycursor.execute("SELECT DISTINCT State,District,RegisteredUser FROM top_user GROUP BY State,District,RegisteredUser ORDER BY RegisteredUser ASC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['State','District','RegisteredUser'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Least 10 registered-users based on Districts and states")
            st.bar_chart(data=df,x="State",y="RegisteredUser")
    elif select=="Top 10 transactions_type based on states and transaction_amount":
        mycursor.execute("SELECT DISTINCT state,trans_type,trans_amount FROM Aggre_trans GROUP BY state,trans_type,trans_amount ORDER BY trans_amount DESC LIMIT 10");
        df = pd.DataFrame(mycursor.fetchall(),columns=['state','trans_type','trans_amount'])
        col1,col2 = st.columns(2)
        with col1:
            st.write(df)
        with col2:
            st.title("Top 10 transactions_type based on states and transaction_amount")
            st.bar_chart(data=df,x="state",y="trans_amount")

if SELECT == "Home":  
    col1,col2, = st.columns(2)
    #col1.image(Image.open("images/phonepe.png"),width = 500)
    with col1:
        st.subheader("PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.video("https://www.google.co.in/search?q=phone+pe+pulse-video.mp4&sca_esv=334a9bda33585e15&sxsrf=ADLYWILZk9fWWjUFOafevOW0rnS_rgfc_g%3A1719553466483&ei=uk1-ZoCGHYibseMPkayf6A0&ved=0ahUKEwiAy6rsy_2GAxWITWwGHRHWB90Q4dUDCA8&uact=5&oq=phone+pe+pulse-video.mp4&gs_lp=Egxnd3Mtd2l6LXNlcnAiGHBob25lIHBlIHB1bHNlLXZpZGVvLm1wNEjOmwFQs3dY5JUBcAR4AJABAJgBtgKgAfoOqgEHMC45LjEuMbgBA8gBAPgBAZgCAqACwwLCAgcQIxiwAhgnwgIIEAAYgAQYogSYAwCIBgGSBwMwLjKgB50P&sclient=gws-wiz-serp#fpstate=ive&vld=cid:dfb9756c,vid:c_1H6vivsiA,st:0")



if SELECT == "Contact":
    name = "YASHODHA.M"
    mail = (f'{"Mail :"}  {"yashodha.mohanakannan@gmail.com"}')
    description = "An Aspiring DATA-SCIENTIST..!"
    social_media = {
        "GITHUB": "https://github.com/Yasho2112/yasho2112",
        "LINKEDIN": "https://www.linkedin.com/in/yashodha-mohanakannan-702361119/",
        

    }
    col1, col2, col3 = st.columns(3)
    #col2.image(Image.open("images/my.png"), width=350)
    with col3:
        st.title(name)
        st.write(description)
        st.write("---")
        st.subheader(mail)
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")

if SELECT =="Search":
    Topic = ["","Transaction-Type","District","Brand","Top-Transactions","Registered-users"]
    choice_topic = st.selectbox("Search by",Topic)

#creating functions for query search in sql to get the data
    def type_(type):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,trans_type,trans_count,trans_amount FROM Aggre_trans WHERE trans_type = '{type}' ORDER BY state,quarter,year");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state','year', 'quarter', 'trans_type','trans_count', 'trans_amount'])
        return df
    def type_year(year,type):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,trans_type,trans_amount FROM Aggre_trans WHERE Year = '{year}' AND trans_type = '{type}' ORDER BY state,quarter,year");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'trans_type', 'trans_amount'])
        return df
    def type_state(state,year,type):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,trans_type,trans_amount FROM Aggre_trans WHERE State = '{state}' AND trans_type = '{type}' And year = '{year}' ORDER BY state,quarter,year");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'trans_type', 'trans_amount'])
        return df
    def district_choice_state(_state):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,map_district,map_amount FROM Map_trans WHERE state = '{_state}' ORDER BY state,year,quarter,map_district");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'map_district', 'map_amount'])
        return df
    def dist_year_state(year,_state):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,map_district,map_amount FROM Map_trans WHERE Year = '{year}' AND State = '{_state}' ORDER BY state,year,quarter,map_district");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'map_district', 'map_amount'])
        return df
    def district_year_state(_dist,year,_state):
        mycursor.execute(f"SELECT DISTINCT state,year,quarter,map_district,map_amount FROM Map_trans WHERE map_district = '{_dist}' AND state = '{_state}' AND year = '{year}' ORDER BY state,year,quarter,map_district");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'map_district', 'map_amount'])
        return df
    def brand_(brand_type):
        mycursor.execute(f"SELECT state,year,quarter,brands,Percentage FROM Aggre_user WHERE brands='{brand_type}' ORDER BY state,year,quarter,brands,Percentage DESC");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'brands', 'Percentage'])
        return df
    def brand_year(brand_type,year):
        mycursor.execute(f"SELECT state,year,quarter,brands,Percentage FROM Aggre_user WHERE year = '{year}' AND brands='{brand_type}' ORDER BY state,year,quarter,brands,Percentage DESC");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'brands', 'Percentage'])
        return df
    def brand_state(state,brand_type,year):
        mycursor.execute(f"SELECT state,year,quarter,brands,Percentage FROM Aggre_user WHERE state = '{state}' AND brands='{brand_type}' AND year = '{year}' ORDER BY state,year,quarter,brands,Percentage DESC");
        df = pd.DataFrame(mycursor.fetchall(), columns=['state', 'year',"quarter", 'brands', 'Percentage'])
        return df
    def transaction_state(_state):
        mycursor.execute(f"SELECT State,Year,Quarter,District,transaction_count,transaction_amount FROM top_trans WHERE State = '{_state}' GROUP BY State,Year,Quarter,District,transaction_count,transaction_amount")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quarter", 'District', 'transaction_count', 'transaction_amount'])
        return df
    def transaction_year(_state,_year):
        mycursor.execute(f"SELECT State,Year,Quarter,District,transaction_count,transaction_amount FROM top_trans WHERE Year = '{_year}' AND State = '{_state}' GROUP BY State,Year,Quarter,District,transaction_count,transaction_amount")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quarter", 'District', 'transaction_count', 'transaction_amount'])
        return df
    def transaction_quater(_state,_year,_quater):
        mycursor.execute(f"SELECT State,Year,Quarter,District,transaction_count,transaction_amount FROM top_trans WHERE Year = '{_year}' AND Quarter = '{_quater}' AND State = '{_state}' GROUP BY State,Year,Quarter,District,transaction_count,transaction_amount")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quater", 'District', 'transaction_count', 'transaction_amount'])
        return df
    def registered_user_state(_state):
        mycursor.execute(f"SELECT State,Year,Quarter,District,RegisteredUser FROM map_user WHERE State = '{_state}' ORDER BY State,Year,Quarter,District")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quater", 'District', 'RegisteredUser'])
        return df
    def registered_user_year(_state,_year):
        mycursor.execute(f"SELECT State,Year,Quarter,District,RegisteredUser FROM Map_user WHERE Year = '{_year}' AND State = '{_state}' ORDER BY State,Year,Quarter,District")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quarter", 'District', 'RegisteredUser'])
        return df
    def registered_user_district(_state,_year,_dist):
        mycursor.execute(f"SELECT State,Year,Quarter,District,RegisteredUser FROM Map_user WHERE Year = '{_year}' AND State = '{_state}' AND District = '{_dist}' ORDER BY State,Year,Quarter,District")
        df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Year',"Quarter", 'District', 'RegisteredUser'])
        return df


    if choice_topic=="Transaction-Type":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("-- 5 TYPES OF TRANSACTION --")
            transaction_type = st.selectbox("search by", ["Choose an option", "Peer-to-peer payments",
                                                          "Merchant payments", "Financial Services",
                                                          "Recharge & bill payments", "Others"], 0)
        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2020", "2021", "2022", "2023", "2024"], 0)
        with col3:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("State", menu_state, 0)

        if transaction_type:
            col1,col2,col3, = st.columns(3)
            with col1:
                st.subheader(f'{transaction_type}')
                st.write(type_(transaction_type))
        if transaction_type and choice_year:
            with col2:
                st.subheader(f' in {choice_year}')
                st.write(type_year(choice_year,transaction_type))
        if transaction_type and choice_state and choice_year:
            with col3:
                st.subheader(f' in {choice_state}')
                st.write(type_state(choice_state,choice_year,transaction_type))

    if choice_topic=="District":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("State", menu_state, 0)
        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2020", "2021", "2022", "2023", "2024"], 0)
        with col3:
            st.subheader("-- SELECT DISTRICTS --")
            district = st.selectbox("search by", Map_Transaction["District"].unique().tolist())
        if choice_state:
            col1,col2,col3 = st.columns(3)
            with col1:
                st.subheader(f'{choice_state}')
                st.write(district_choice_state(choice_state))
        if choice_year and choice_state:
            with col2:
                st.subheader(f'in {choice_year} ')
                st.write(dist_year_state(choice_year,choice_state))
        if district and choice_state and choice_year:
            with col3:
                st.subheader(f'in {district} ')
                st.write(district_year_state(district,choice_year,choice_state))

    if choice_topic=="Brand":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("-- TYPES OF BRANDS --")
            mobiles = ["",'Xiaomi', 'Vivo', 'Samsung', 'Oppo', 'Realme', 'Apple', 'Huawei', 'Motorola', 'Tecno', 'Infinix',
                       'Lenovo', 'Lava', 'OnePlus', 'Micromax', 'Asus', 'Gionee', 'HMD Global', 'COOLPAD', 'Lyf',
                       'Others']
            brand_type = st.selectbox("search by",mobiles, 0)
        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2020", "2021", "2022", "2023", "2024"], 0)
        with col3:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("State", menu_state, 0)

        if brand_type:
            col1,col2,col3, = st.columns(3)
            with col1:
                st.subheader(f'{brand_type}')
                st.write(brand_(brand_type))
        if brand_type and choice_year:
            with col2:
                st.subheader(f' in {choice_year}')
                st.write(brand_year(brand_type,choice_year))
        if brand_type and choice_state and choice_year:
            with col3:
                st.subheader(f' in {choice_state}')
                st.write(brand_state(choice_state,brand_type,choice_year))

    if choice_topic=="Top-Transactions":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("State", menu_state, 0)
        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2020", "2021", "2022", "2023", "2024"], 0)
        with col3:
            st.subheader("--4 Quaters --")
            menu_quater = ["", "1", "2", "3", "4"]
            choice_quater = st.selectbox("Quater", menu_quater, 0)

        if choice_state:
            with col1:
                st.subheader(f'{choice_state}')
                st.write(transaction_state(choice_state))
        if choice_state and choice_year:
            with col2:
                st.subheader(f'{choice_year}')
                st.write(transaction_year(choice_state,choice_year))
        if choice_state and choice_quater:
            with col3:
                st.subheader(f'{choice_quater}')
                st.write(transaction_quater(choice_state,choice_year,choice_quater))

    if choice_topic=="Registered-users":
        col1,col2,col3 = st.columns(3)
        with col1:
            st.subheader("-- 36 STATES --")
            menu_state = ["", 'uttar-pradesh', 'jharkhand', 'puducherry', 'rajasthan', 'odisha', 'nagaland',
                          'chandigarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'assam', 'haryana', 'jammu-&-kashmir',
                          'tamil-nadu', 'himachal-pradesh', 'ladakh', 'bihar', 'maharashtra', 'uttarakhand',
                          'karnataka', 'lakshadweep', 'andhra-pradesh', 'sikkim', 'madhya-pradesh', 'mizoram',
                          'kerala', 'manipur', 'arunachal-pradesh', 'andaman-&-nicobar-islands', 'delhi', 'tripura',
                          'chhattisgarh', 'meghalaya', 'goa', 'west-bengal', 'telangana', 'gujarat', 'punjab']
            choice_state = st.selectbox("State", menu_state, 0)
        with col2:
            st.subheader("-- 5 YEARS --")
            choice_year = st.selectbox("Year", ["", "2020", "2021", "2022", "2023", "2024"], 0)
        with col3:
            st.subheader("-- SELECT DISTRICTS --")
            district = st.selectbox("search by", Map_Transaction["District"].unique().tolist())

        if choice_state:
            with col1:
                st.subheader(f'{choice_state}')
                st.write(registered_user_state(choice_state))
        if choice_state and choice_year:
            with col2:
                st.subheader(f'{choice_year}')
                st.write(registered_user_year(choice_state,choice_year))
        if choice_state and choice_year and district:
            with col3:
                st.subheader(f'{district}')
                st.write(registered_user_district(choice_state,choice_year,district))

# df = pd.read_csv("https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/active_cases_2020-07-17_0800.csv")

# fig = px.choropleth(
#     df,
#     geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
#     featureidkey='properties.ST_NM',
#     locations='state',
#     color='active cases',
#     color_continuous_scale='Reds'
# )

# fig.update_geos(fitbounds="locations", visible=False)

# fig.show()
