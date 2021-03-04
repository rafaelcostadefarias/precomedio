#!/usr/bin/env python
# coding: utf-8

# In[42]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader.data as web
import yfinance as yf
import datetime
import streamlit as st


# In[19]:


#Dependendo do ambiente, a atribuição de arrays nos dataframes gera muitos warnings. Com esse comando podemos ignorar.
import warnings
warnings.filterwarnings('ignore')


# In[20]:


yf.pdr_override()


# In[43]:


#Input da ação a ser estudada
symbol = st.text_input("Ativo", "PETR4")

#Valor do aporte
aporte = st.number_input("Aporte", 100)

#Início da simulação
inicio = st.date_input("Início",datetime.date(2000, 1, 1))


# In[32]:


#Download dados
symbol = symbol + ".SA"


# In[33]:


#Download da base de dados
ativo = symbol
df = web.get_data_yahoo(ativo,start=inicio,end='2021-12-01', interval='1mo', period='1mo')


# In[34]:


df = df.dropna(axis = 0) 


# In[37]:


#Faz a compra sempre no inicio do mes - Aporte X reais
df['Aporte'] = aporte

df['Acoes'] = aporte / df['Adj Close']

df['AcoessemDiv'] = ((aporte) / df['Close'])

df['Caixa'] = (aporte - (df['Acoes']*df['Adj Close']))


# In[38]:


#Acoes acumuladas
df['Total_Acoes'] = df['Acoes'].cumsum()
df['Total_Acoes_sem'] = df['AcoessemDiv'].cumsum()


# In[39]:


df['Capital_Acumulado'] = (df['Total_Acoes'] * df['Adj Close'])
df['Sem_Dividendo'] = (df['Total_Acoes_sem'] * df['Close'])
df['Aporte_Acumulado'] = df['Aporte'].cumsum()


# In[40]:


df['Data'] = df.index


# In[41]:


import plotly.express as px

fig = px.line(df, x=df['Data'], y=df['Capital_Acumulado'])
fig.add_scatter(x=df['Data'], y=df['Sem_Dividendo'],name='Sem Dividendos') 
fig.add_scatter(x=df['Data'], y=df['Aporte_Acumulado'],name='Aportes') 

st.plotly_chart(fig)


# In[ ]:


st.write("Capital acumulado: R$",round(df.iloc[-1]['Capital_Acumulado'],2))
st.write("Total de aportes: R$", round((df.count()[0] * aporte),2))
st.write("Lucro:", round(((df.iloc[-1]['Capital_Acumulado'] / (df.count()[0] * aporte)) - 1) * 100,2),'%')
st.write("Meses:", df.count()[0])
st.write("Média mensal:", round(round(((df.iloc[-1]['Capital_Acumulado'] / (df.count()[0] * aporte)) - 1) * 100,2) / df.count()[0],2),'%')

