import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import csv
import pydeck as pdk
import datetime as dt
from datetime import date
import altair as alt
import mapbox as mb
import os

def load_data():
    database = os.path.join(os.getcwd(),"BosAirBnB2021.csv")
    df = pd.read_csv(database)
    #df = pd.read_csv("BosAirBnB2021.csv")
    df = df.drop(columns = "neighbourhood_group")
    df ["estimated_income"] = df["price"]*df["minimum_nights"]
    return df

def date_difference(dataframe):
    recent_list = []
    for i in dataframe.values:
        str_date=date(int(i.split("/")[2]),int(i.split("/")[0]),int(i.split("/")[1]))
        today=dt.date.today()
        days_between = (today-str_date).days  # references: https://stackoverflow.com/questions/8419564/difference-between-two-dates-in-python

        if days_between <614:
            recent_list.append(i)
    return recent_list

def neighborhood_pdframe(previousdf,filterstr):
    if filterstr == "Boston":
        afterdf = previousdf
    else:
        afterdf = previousdf[previousdf['neighbourhood']== filterstr ]
    return afterdf

def roomtype_pdframe(previousdf,filterstr):
    afterdf = previousdf[ previousdf['room_type']== filterstr ]
    return afterdf

def filter_list(filtername,dataframe):
    listname=[]
    for i in dataframe[filtername]:
        if i not in listname:
            listname.append(i)
    return listname

def simple_barh(dictionary,yticks):
    fig,ax =plt.subplots()
    ax.barh(yticks,dictionary.values(),height=0.5,color=['blue','green','darkorange','silver'])

    ax.set_xlabel("listings")
    ax.grid(color='gainsboro',lw=0.25)
    plt.yticks(rotation=90)
    return fig

def main():
# read files
    df = load_data()
    print(df.columns)

# create queries
# classidied by neighborhood
    neighborhood = ["Boston"] + filter_list("neighbourhood",df)

    st.header('**Boston AirBnb Analysis** \n :female-student: ')
    st.markdown("""<style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 600px;}
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 600px;margin-left: -600px;}
        </style>""",
        unsafe_allow_html=True)                 # reference: https://github.com/streamlit/streamlit/issues/2058
    st.write('AirBnb **_Roomtype, Activity, Availability, Host Analysis_** based on neighborhoods.')

#####################################################################
    st.sidebar.markdown("""<style>
    .font1{font-size : 40px;}
    .font2{font-size : 25px;}
    .font3{color:gray; font-size : 17px;}
    .font4{color: black; font-size : 13px;} 
    </style>""",unsafe_allow_html=True)   # reference: https://discuss.streamlit.io/t/change-font-size-in-st-write/7606/2
                                        # reference: https://github.github.com/gfm/#example-141
#############################################################################

    st.sidebar.markdown('<p class="font1"> Boston </p>', unsafe_allow_html=True)
    col1,col2 = st.sidebar.beta_columns([20,17])
    st.sidebar.write("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
    #col3 = st.sidebar.markdown(' <hr />', unsafe_allow_html=True)
    st.sidebar.markdown(" ")

########################################################################
    col3,col4 = st.sidebar.beta_columns([1,1])
    st.sidebar.markdown(' <hr />', unsafe_allow_html=True)
    #st.sidebar.write("There are four types of room type. Depending on the room type, "
    #                 "a preference of host to list their rooms can be discovered.")
    st.sidebar.markdown('<p class="font3">There are four types of room type. Depending on the room type. A preference of host to list their rooms can be discovered.</p>',unsafe_allow_html=True)
    col5, col6 = st.sidebar.beta_columns([2,3])
    st.sidebar.write("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
###########################################################
    col7,col8 = st.sidebar.beta_columns([8,9])
    st.sidebar.markdown(' <hr />', unsafe_allow_html=True)
    col9, col16,col10 = st.sidebar.beta_columns([12,2,7])
    st.sidebar.write("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
#######################################################################
    col11, col12 = st.sidebar.beta_columns([11,6])
    st.sidebar.markdown(' <hr />', unsafe_allow_html=True)
    col13,col14,col15 = st.sidebar.beta_columns([12,2,7])
    st.sidebar.markdown(" ")
    col27,col17,col18 = st.sidebar.beta_columns((1,11,1))
    st.sidebar.write("￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣￣")
######################################################
    col19, col20 = st.sidebar.beta_columns([21,11])
    st.sidebar.markdown(' <hr />', unsafe_allow_html=True)
    col21,col22,col23 = st.sidebar.beta_columns([12,2,7])
    col24,col25 = st.sidebar.beta_columns([1,30])
    col26 = st.sidebar.beta_expander("Top Hosts")
##########################################################
    with col3:
        st.markdown('<p class="font2"> Room Type </p>', unsafe_allow_html=True)
        #st.subheader("Room Type")
    with col7:
        st.markdown('<p class="font2"> Activity </p>', unsafe_allow_html=True)
    with col9:
        st.markdown('<p class="font3">The minimum stay and price can be used to estimate the occupancy rate and estimated income per month. </p>', unsafe_allow_html=True)
        st.markdown('<p class="font3">The number of reviews indicates the active activitity extent. The higher the reviews per listins, the more active this lising (or this area) is.</p>', unsafe_allow_html=True)
        st.markdown('<p class="font3">RECENT means there was a review in the last 6 months for the listins we choose. </p>', unsafe_allow_html=True)
        st.markdown('<p class="font3">FREQUENTLY means listings with the minimum booking nights per year over 60 days</p>', unsafe_allow_html=True)
    with col11:
        st.markdown('<p class="font2"> Availability </p>', unsafe_allow_html=True)
    with col19:
        st.markdown('<p class="font2"> Lisings per Host </p>', unsafe_allow_html=True)
    with col21:
        st.markdown('<p class="font3">A host may list seperate rooms in the same apartment or multiple apartment.</p>', unsafe_allow_html=True)
        st.markdown('<p class="font3">Hosts with many multiple listings are more likely to be running a business.</p>', unsafe_allow_html=True)
        st.markdown('<p class="font3">The estimated income for each listing can be used to estimate the income for each host. </p>', unsafe_allow_html=True)
########################################################################################
# FILTERING TO GET FINAL DATAFRAME
# Neighborhood filter

    with col1:
        neighborhood_option = st.selectbox("Filter by:",neighborhood)
        afterdf1 = neighborhood_pdframe(df,neighborhood_option)

# Room typr filter
    with col4:
        st.markdown(" ")
        roomtype_option = st.checkbox("Only entire homes/ apartments")
        if roomtype_option:
            afterdf2 = afterdf1[afterdf1['room_type']== "Entire home/apt"]
        else:
            afterdf2 = afterdf1

# Activity filter
    with col8:
        st.markdown(" ")
        activity_option = st.checkbox("Only recent and frequently booked")
        if activity_option:
            # frequently: Listings with an minimum booking nights per year of > 60 nights
            draft1_afterdf3 = afterdf2[afterdf2["minimum_nights"] > 60]
            # rencent: Listings with a review in the last 614 days
                # Remove the rows whose "last_reviews" has NA values in the BosAirBnB2021.csv
            draft2_afterdf3 = draft1_afterdf3.dropna(subset=["last_review"])
            recent_list = date_difference(draft2_afterdf3.last_review)
            afterdf3 = draft2_afterdf3[draft2_afterdf3["last_review"].isin (recent_list)]   # references: https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isin.html
        else:
            afterdf3 = afterdf2

# Availibility filter
    with col12:
        st.markdown(" ")
        availablity_option = st.checkbox("Only highly available")
        if availablity_option:
            afterdf4  = afterdf3[afterdf3["availability_365"] > 60 ]
        else:
            afterdf4 = afterdf3

# Host filter
    with col20:
        st.markdown(" ")
        listings_option = st.checkbox("Only multi-listings")
        if listings_option:
            finaldataframe  = afterdf4[afterdf4["calculated_host_listings_count"] > 1 ]
        else:
            finaldataframe = afterdf4                                        # FINAL DATASET

# Check Final dataset
    if finaldataframe.empty:
        st.markdown('<p class="font1">There is no data in this filter.</p>', unsafe_allow_html=True)
    else:

################################################################

        mapdataframe = finaldataframe.dropna(subset=list(df.columns))
        view_state = pdk.ViewState(
            latitude=mapdataframe["latitude"].mean(),
            longitude=mapdataframe["longitude"].mean(),
            zoom=11,
            pitch=0)
        layer1 = pdk.Layer('ScatterplotLayer',
                  data=mapdataframe,
                  get_position='[longitude, latitude]',
                  get_radius=100,
                  get_color=[0,0,255],
                  pickable=True
                  )
        tool_tip = {"html": "Host Name:<br/> <b>{host_name}</b> <br/>listing ID: <b>{id}</b> <br/>Listing Name:<br/><b>{name}</b><br/><b>{neighbourhood}</b><br/><b>{room_type}</b>",
            "style": { "backgroundColor": "steelblue",
                        "color": "white"}}
        map = pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=view_state,
            layers=[layer1],
            tooltip= tool_tip
            )
        st.pydeck_chart(map)

########################################################################################
# CALCULATE STUFF:
        with col2:     # out of listings

            numbers_of_listings_in_df = len(finaldataframe)
            numbers_of_listings_in_chosen_neighborhood = len(afterdf1)
            percentage_of_listings = numbers_of_listings_in_df/numbers_of_listings_in_chosen_neighborhood

            st.title(f'**{numbers_of_listings_in_df:>,d}**')
            #st.markdown(f'<h1>{numbers_of_listings_in_df:>,d}</h1>', unsafe_allow_html=True)
            st.markdown(f'out of **{numbers_of_listings_in_chosen_neighborhood:>,d}** listings ({percentage_of_listings:.1%})')

        with col6:        # room type graph
            st.markdown(" ")
            st.markdown(" ")
            roomtype_count= finaldataframe.groupby(by="room_type").count().id.sort_values(ascending = False)

            roomtype_list = ["Entire home/apt","Private room","Hotel room","Shared room"]
            roomtype_dic ={}
            for i in roomtype_list:
                if i in roomtype_count.index:
                    roomtype_dic[i] = roomtype_count[i]
                else:
                    roomtype_dic[i] = 0

            st.pyplot(simple_barh(roomtype_dic,roomtype_list))

        with col5:      # room type calculation

            percentage_of_entireRoomType = roomtype_dic["Entire home/apt"]/numbers_of_listings_in_df
            st.markdown('<p class="font4"> entire homes/apartments:</p>', unsafe_allow_html=True)
            st.markdown(f'**{percentage_of_entireRoomType:>.1%}**')

            avgprice_pernight = finaldataframe.price.mean()
            st.markdown('<p class="font4"> price/night:</p>', unsafe_allow_html=True)
            st.markdown(f'$**{avgprice_pernight:>.0f}**')

            st.markdown('<p class="font4"> entire homes/apartments:</p>', unsafe_allow_html=True)
            st.markdown(f'**{roomtype_dic["Entire home/apt"]:>,d}** ({percentage_of_entireRoomType:>.1%})')

            st.markdown('<p class="font4">private room:', unsafe_allow_html=True)
            st.markdown(f'**{roomtype_dic["Private room"]:>,d}** /'
                    f'({roomtype_dic["Private room"]/numbers_of_listings_in_df:>.1%})')

            st.markdown('<p class="font4"> Shared room:', unsafe_allow_html=True)
            st.markdown(f'**{roomtype_dic["Shared room"]:>,d}** /'
                    f'({roomtype_dic["Shared room"]/numbers_of_listings_in_df:>.1%})')

        with col10:  # Activity Calculation

            st.markdown('<p class="font4">occupied nights/year:</p>', unsafe_allow_html=True)
            avgmin_nights = finaldataframe.minimum_nights.mean()
            st.markdown(f'**{avgmin_nights:>.0f}**')

            st.markdown('<p class="font4">reviews/listing/month:</p>', unsafe_allow_html=True)
            # Remove the row whose "reviews per month" has NA value in BosAirBnB2021.csv
            draft1_finaldataframe = finaldataframe.dropna(subset=["reviews_per_month"])
            sumreviews_permonth = draft1_finaldataframe.reviews_per_month.sum()
            avgreviews_permonth = sumreviews_permonth/finaldataframe.id.count()
            st.markdown(f'**{avgreviews_permonth:>,.1f}**')

            st.markdown('<p class="font4">reviews:</p>', unsafe_allow_html=True)
            sumreviews = finaldataframe.number_of_reviews.sum()
            st.markdown(f'**{sumreviews:>,d}**')

            st.markdown('<p class="font4">estimated occupancy:</p>', unsafe_allow_html=True)
            estimated_occupancy = avgmin_nights/365
            st.markdown(f'**{estimated_occupancy:>.1%}**')

            st.markdown('<p class="font4">estimated income/month:</p>', unsafe_allow_html=True)
            estimated_income = finaldataframe.estimated_income.mean()
            st.markdown(f'$**{estimated_income:>,.0f}**')

        with col15:   # Availablility Calculation

            st.markdown(" ")
            st.markdown(" ")
            st.markdown(" ")

            st.markdown('<p class="font4">high_ availability</p>', unsafe_allow_html=True)
            highavailability = finaldataframe[finaldataframe["availability_365"]>60].availability_365.count()
            percentage_of_highavailability = highavailability/numbers_of_listings_in_df
            st.markdown(f'**{percentage_of_highavailability:>.1%}**')

            st.markdown('<p class="font4">listings with _high_ availablity</p>', unsafe_allow_html=True)
            st.markdown(f'**{highavailability:>,d}** ({percentage_of_highavailability:>.1%})')

            st.markdown('<p class="font4">listings with _low_ availablity</p>', unsafe_allow_html=True)
            lowavailability = finaldataframe[finaldataframe["availability_365"]<=60].availability_365.count()
            st.markdown(f'**{lowavailability:>,d}** ({(lowavailability/numbers_of_listings_in_df):>.1%})')

            st.markdown('<p class="font4">days/year</p>', unsafe_allow_html=True)
            avgavailability = finaldataframe.availability_365.mean()
            st.markdown(f'**{avgavailability:>.1f}** ({(avgavailability/365):>.1%})')

        with col17:   # Availability scatter plot

            availability_num = finaldataframe.groupby(by ="availability_365").count().id

            availabilitydate_list = [i for i in range(1,366)]
            availability_dic ={}
            availability_list = []
            for i in availabilitydate_list:
                if i in availability_num.index:
                    availability_list.append(availability_num[i])
                else:
                    availability_list.append(0)
            availability_dic['number of days available in year'] = availabilitydate_list
            availability_dic['listings'] = availability_list
            availability_pd = pd.DataFrame(availability_dic)

            chart1 = alt.Chart(availability_pd).mark_circle().encode(
                x ='number of days available in year',
                y ='listings',
                tooltip = ['number of days available in year','listings']).interactive()
            st.altair_chart(chart1,use_container_width=True)        # references: https://docs.streamlit.io/en/stable/api.html#display-charts
                                                                # references: https://github.com/streamlit/streamlit/issues/1129

        with col13:         # availability pie chart

            st.markdown('<p class="font3">HIGHLY AVAILABILITY means listings with more than 60 days availability.</p>', unsafe_allow_html=True)
            st.markdown('<p class="font3">A higher availability indicates these listins are high profitable and are in higher demand.</p>', unsafe_allow_html=True)

            fig,ax = plt.subplots()
            ax.axis('equal')
            label = ['low','high']
            pie_list = [lowavailability,highavailability]
            ax.pie(pie_list,labels = label, autopct='%1.2f%%')
            st.pyplot(fig)

        with col23:  # Listings per Host Calculation

            multiListings_df = finaldataframe[finaldataframe["calculated_host_listings_count"] > 1]
            multiListings_count = multiListings_df.id.count()
            singleListings_df = finaldataframe[finaldataframe["calculated_host_listings_count"] == 1]
            singleListings_count = singleListings_df.id.count()
            percentage_of_multiListings = multiListings_count/numbers_of_listings_in_df
            percentage_of_singleListings = singleListings_count/numbers_of_listings_in_df

            st.markdown('multi-listings:')
            st.markdown(f'**{percentage_of_multiListings:>.1%}**')
            st.markdown('single listings:')
            st.markdown(f'**{singleListings_count:>d}** ({(percentage_of_singleListings):>.1%})')
            st.markdown('multi-listings:')
            st.markdown(f'**{multiListings_count:>d}** ({(percentage_of_multiListings):>.1%})')

        with col25:
            st.markdown(" ")
            listingsPerHost_count = {"listings per host":[],"listings":[]}
            for i in finaldataframe["calculated_host_listings_count"]:
                if i not in listingsPerHost_count["listings per host"]:
                    listingsPerHost_count["listings per host"].append(i)
                    listingsPerHost_count["listings"].append(1)
                else:
                    index1 = listingsPerHost_count["listings per host"].index(i)
                    listingsPerHost_count["listings"][index1] += 1

            listingsPerHost_countdf = pd.DataFrame(listingsPerHost_count)
            listingsPerHost_countdf = listingsPerHost_countdf.sort_values(by=["listings per host"],ascending=True)

            #st.bar_chart(listingsPerHost_countdf)  # there is no labels, so use the following
            bar_chart = alt.Chart(listingsPerHost_countdf).mark_bar().encode(
                alt.X("listings per host",bin=True),
                alt.Y('listings')).interactive()                      # references: https://discuss.streamlit.io/t/st-bar-chart/4922/4
            st.altair_chart(bar_chart)

        with col26:

            host_dictionary={"host id":[],"name": [],"listings count":[],"estimated income":[]}
            df1 = finaldataframe.groupby(by = 'host_id').count()
            df2 = finaldataframe.groupby(by = 'host_id').sum()
            host_idlist = df1.index.tolist()      # references:https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.to_list.html

            for i in range(0,len(host_idlist)):
                host_id = host_idlist[i]
                host_dictionary["host id"].append(host_id)
                name = finaldataframe.loc[finaldataframe["host_id"]== host_id, "host_name"].values[0]
                host_dictionary["name"].append(name)
                calculated_host_listings_count = df1.loc[host_id]["calculated_host_listings_count"]
                host_dictionary["listings count"].append(calculated_host_listings_count)
                host_estimated_income = df2.loc[host_id]["estimated_income"]
                host_dictionary["estimated income"].append(host_estimated_income)

            host_dataframe = pd.DataFrame(host_dictionary)
            host_dataframe = host_dataframe.sort_values(by="listings count",ascending=False)

            num1 = min(len(host_idlist),20)
            st.table(host_dataframe[["name","listings count","estimated income"]].head(num1))

main()











