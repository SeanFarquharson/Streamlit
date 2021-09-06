#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt


# In[2]:


draft_data = pd.read_csv (r'C:\Users\seanf\OneDrive\Documents\SUMMER RESEARCH PROJECT\data\playerstats.csv')


# In[3]:


#convert GP_greater_than_0 to binary 0-No 1-Yes
draft_data_1=pd.get_dummies(draft_data["GP_greater_than_0"])
draft_data_2=pd.concat((draft_data_1, draft_data), axis=1)
draft_data_2=draft_data_2.drop(["GP_greater_than_0"], axis=1)
draft_data_2=draft_data_2.drop(["no"], axis=1)
draft_data_v=draft_data_2.rename(columns={"yes": "GP_greater_than_0"})


# In[4]:


#convert po_GP to binary 1-played in at least one playoff game 0-did not play in the playoffs
dr=pd.get_dummies(draft_data_v["po_GP"])
dr2=pd.concat((dr, draft_data_v), axis=1)
dr2=dr2.drop(["po_GP","po_G","po_A","po_P","po_PIM"], axis=1)
dr2=dr2.drop(dr2.columns[[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,
                                    16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]], axis=1)
dr3=dr2.rename(columns={0: "po_GP_greater_than_0"})


# In[5]:


#flip binary outcome

dr4=pd.get_dummies(dr3["po_GP_greater_than_0"])
dr5=pd.concat((dr4, dr3), axis=1)
dr5=dr5.drop(["po_GP_greater_than_0"], axis=1)
dr5=dr5.drop(dr5.columns[[1]], axis=1)
dr6=dr5.rename(columns={0: "po_GP_greater_than_0"})


# In[6]:


dr7=dr6.drop(['PlayerName','Country','DraftYear',
                           'DraftAge','Height','Weight','rs_GP',
                           'rs_G','rs_A','rs_P','rs_PlusMinus','rs_PIM',
                           'CSS_rank','Position'], axis=1)


# In[7]:


dr8=(dr7.groupby('country_group').agg({'id':'count', 'GP_greater_than_0': 'sum', 'sum_7yr_TOI': 'sum', 'sum_7yr_GP': 'sum','Overall': 'sum'})
 .reset_index()
 .rename(columns={'id':'Player Count'}))


# In[8]:


dr8["Average draft selection overall"] = (dr8["Overall"] / dr8['Player Count'])


# In[9]:


dr9 = dr8.drop(['sum_7yr_TOI','sum_7yr_GP','Overall'], axis=1)


# In[10]:


dr10 = dr9.rename(columns={"GP_greater_than_0": "played in NHL"})


# In[11]:


st.sidebar.checkbox("Show Analysis by Country Group", True, key=1)
select = st.sidebar.selectbox('Select a Country Group',dr10['country_group'])

#get the country group selected in the selectbox
CG_data = dr10[dr10['country_group'] == select]
select_status = st.sidebar.radio("Option", ('Player Count',
'played in NHL','Average draft selection overall'))


# In[13]:


def get_total_dataframe(dataset):
    total_dataframe = pd.DataFrame({
    'Option':['Player Count', 'played in NHL','Average draft selection overall'],
    'Number of players':(dataset.iloc[0]['Player Count'],
    dataset.iloc[0]['played in NHL'],
    dataset.iloc[0]['Average draft selection overall'])})
    return total_dataframe

CG_total = get_total_dataframe(CG_data)

if st.sidebar.checkbox("Show Analysis by Country Group", True, key=2):
    st.markdown("## **Country Group level analysis**")
    st.markdown("### Draft Selections who go on to " +
    "playing in the NHL and their average draft selection overall for %s players" % (select))
    if not st.checkbox('Hide Graph', False, key=3):
        CG_total_graph = px.bar(
        CG_total, 
        x='Option',
        y='Number of players',
        labels={'Number of players':'Count'},
        color='Option')
        st.plotly_chart(CG_total_graph)


# In[ ]:




