#!/usr/bin/env python
# coding: utf-8

# # Avaliação 2 - Gabriel Lima Novais 

# Data Set Escolhido : Air Quality UCI
# 
# Site/Link : https://archive.ics.uci.edu/ml/datasets/Air+Quality#

# ### Data Set Information:
# 
# The dataset contains 9358 instances of hourly averaged responses from an array of 5 metal oxide chemical sensors embedded in an Air Quality Chemical Multisensor Device. The device was located on the field in a significantly polluted area, at road level,within an Italian city. Data were recorded from March 2004 to February 2005 (one year)representing the longest freely available recordings of on field deployed air quality chemical sensor devices responses. Ground Truth hourly averaged concentrations for CO, Non Metanic Hydrocarbons, Benzene, Total Nitrogen Oxides (NOx) and Nitrogen Dioxide (NO2) and were provided by a co-located reference certified analyzer. Evidences of cross-sensitivities as well as both concept and sensor drifts are present as described in De Vito et al., Sens. And Act. B, Vol. 129,2,2008 eventually affecting sensors concentration estimation capabilities. Missing values are tagged with -200 value. 
# This dataset can be used exclusively for research purposes. Commercial purposes are fully excluded. 
# 
# Source : 
# 
# Saverio De Vito (saverio.devito '@' enea.it), ENEA - National Agency for New Technologies, Energy and Sustainable Economic Development

# ### Attribute Information:
# 
# 0) Date	(DD/MM/YYYY)
# 
# 1) Time	(HH.MM.SS) 
# 
# 2) True hourly averaged concentration CO in mg/m^3 (reference analyzer) 
# 
# 3) PT08.S1 (tin oxide) hourly averaged sensor response (nominally CO targeted)	
# 
# 4) True hourly averaged overall Non Metanic HydroCarbons concentration in microg/m^3 (reference analyzer) 
# 
# 5) True hourly averaged Benzene concentration in microg/m^3 (reference analyzer) 
# 
# 6) PT08.S2 (titania) hourly averaged sensor response (nominally NMHC targeted)	
# 
# 7) True hourly averaged NOx concentration in ppb (reference analyzer) 
# 
# 8) PT08.S3 (tungsten oxide) hourly averaged sensor response (nominally NOx targeted) 
# 
# 9) True hourly averaged NO2 concentration in microg/m^3 (reference analyzer)	
# 
# 10) PT08.S4 (tungsten oxide) hourly averaged sensor response (nominally NO2 targeted)	
# 
# 11) PT08.S5 (indium oxide) hourly averaged sensor response (nominally O3 targeted) 
# 
# 12) Temperature in Â°C	
# 
# 13) Relative Humidity (%) 
# 
# 14) AH Absolute Humidity 
# 

# ## Importando pacotes:

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn import decomposition
from statsmodels.tsa.stattools import adfuller
from scipy.stats import shapiro

get_ipython().run_line_magic('matplotlib', 'inline')


# Links de pacotes (documentation):
# 
# https://www.statsmodels.org/stable/about.html#module-statsmodels
# 
# https://scikit-learn.org/stable/
# 
# https://seaborn.pydata.org/
# 
# https://www.scipy.org/docs.html
# 
# 

# ## Importando a Base de Dados:

# In[2]:


dbName = 'AirQualityUCI.xlsx'
db_raw= pd.read_excel(dbName)
db_raw.head()


# ## Tratando a Base de Dados:

# 1) Verificando a quantidade de missing values e substituindo os mesmos pela interpolação das linhas acima e abaixo da base de dados : 

# In[3]:


db_raw.describe() #antes dos missing values


# In[4]:


db_raw[db_raw==-200]=np.nan
db_raw = db_raw.interpolate()


# In[5]:


db_raw.describe() #depois da interpolação


# 2) Dividindo as bases em (GT) e (PTO8):
# 
# OBS: (GT) Refere-se à concentração média verdadeira horária do componente pelo analisador de referência, enquanto que (PT08) refere-se à resposta média do sensor por hora.

# In[6]:


db_GT = db_raw[['Date','Time','CO(GT)','NMHC(GT)','C6H6(GT)','NOx(GT)','NO2(GT)','T','RH','AH']]
db_PT08 = db_raw[['Date','Time','PT08.S1(CO)','PT08.S2(NMHC)','PT08.S3(NOx)','PT08.S4(NO2)','PT08.S5(O3)','T','RH','AH']]


# In[7]:


db_GT.info()


# In[8]:


db_PT08.info()


# ## Analisando os Dados:

# Vamos analisar a correlação entre as variáveis e verificar graficamente.

# In[9]:


sns.pairplot(db_PT08)
plt.show()


# In[10]:


sns.pairplot(db_GT)
plt.show()


# Como ambos dataframes (GT e PT08) são relativamente iguais, vamos focar apenas no que fornece dados provenientes diretamente do sensor (e provavelmente o mais preciso). É perceptivel a correlação entre determinadas variáveis, porém não sabemos quantificar tais valores. Desta forma, vamos calcular a matriz de covariância.

# In[11]:


Var_Corr = db_PT08.corr()
fig,ax = plt.subplots(figsize = (8,8))
sns.heatmap(Var_Corr, xticklabels=Var_Corr.columns, yticklabels=Var_Corr.columns, annot=True, ax = ax)
plt.show()


# Conforme observamos os valores da matriz de covariância, verificamos que os gráficos iniciais estão de acordo com os valores contidos na matriz elemento a elemento. Logo, entendemos que as principais variáveis que explicam a Temperatura são aquelas que estão mais correlacionadas com ela, ou seja, AH, RH, NO2, NMHC. Vamos então verificar a distribuição de cada uma delas de maneira mais próxima.

# In[12]:


fig, ax = plt.subplots(figsize=(20,10))
_ = plt.hist(db_PT08['PT08.S2(NMHC)'], bins = 200)
plt.title("NMHC - Distribuição")


# In[13]:


fig, ax = plt.subplots(figsize=(20,10))
_ = plt.hist(db_PT08['PT08.S4(NO2)'], bins = 200)
plt.title("NO2 - Distribuição")


# In[14]:


fig, ax = plt.subplots(figsize=(20,10))
_ = plt.hist(db_PT08['T'], bins = 200)
plt.title("T - Distribuição")


# In[15]:


fig, ax = plt.subplots(figsize=(20,10))
_ = plt.hist(db_PT08['AH'], bins = 200)
plt.title("AH - Distribuição")


# In[16]:


fig, ax = plt.subplots(figsize=(20,10))
_ = plt.hist(db_PT08['RH'], bins = 200)
plt.title("RH - Distribuição")


# In[17]:


fig, ax = plt.subplots(figsize=(20,10))
PT08 = db_raw[['PT08.S2(NMHC)','PT08.S4(NO2)']]
PT08.plot.box(ax=ax)


# In[18]:


fig, ax = plt.subplots(figsize=(20,10))
PT08 = db_raw[['T','RH','AH']]
PT08.plot.box(ax=ax)


# Analisaremos agora a evolução dos dados quando agrupados sob uma média diária com respeito as horas da base de dados do PT08.

# In[19]:


type(db_PT08['Time'][0])


# In[20]:


type(db_PT08['Date'][0])


# In[21]:


dia = db_PT08['Date']
dia.head(10)


# In[22]:


hora = db_PT08['Time']
hora.head(10)


# In[23]:


df = db_PT08.groupby('Date').mean() # Obtemos valores médios diários paras as variáveis
df.head(10)


# In[24]:


df.info()


# In[25]:


df_selecionadas = df[['PT08.S2(NMHC)','PT08.S4(NO2)','T','RH','AH']]
df_selecionadas.head(10)


# In[26]:


sns.pairplot(df_selecionadas)
plt.show()


# In[27]:


Var_Corr = df_selecionadas.corr()
fig,ax = plt.subplots(figsize = (8,8))
sns.heatmap(Var_Corr, xticklabels=Var_Corr.columns, yticklabels=Var_Corr.columns, annot=True, ax = ax)
plt.show()


# A partir das quatro variáveis anteriores, temos bastante dados para explicar a temperatura.

# Vejamos a evolução das 4 séries diárias comparadas com as séries por hora.

# In[28]:


def plot_c(serie_diaria, serie_hora):
    ratio = (len(serie_hora))/len(serie_diaria)
    extension = np.zeros(len(serie_hora))
    for index in range(len(serie_diaria)):
        extension[int(np.floor(ratio*index))] = serie_diaria[index]
    extension = [np.nan if x == 0 else x for x in extension]
    fig, ax = plt.subplots(figsize=(20,10))
    plt.plot(serie_hora, alpha = 0.5)
    plt.scatter(np.arange(len(extension)), extension, c = 'red')

    plt.legend()


# In[29]:


hora = db_PT08['PT08.S2(NMHC)']
dia = df_selecionadas['PT08.S2(NMHC)']
plot_c(dia,hora)


# In[30]:


hora = db_PT08['PT08.S4(NO2)']
dia = df_selecionadas['PT08.S4(NO2)']
plot_c(dia,hora)


# In[31]:


hora = db_PT08['AH']
dia = df_selecionadas['AH']
plot_c(dia,hora)


# In[32]:


hora = db_PT08['RH']
dia = df_selecionadas['RH']
plot_c(dia,hora)


# In[33]:


hora = db_PT08['T']
dia = df_selecionadas['T']
plot_c(dia,hora)


# Logo, podemos perceber que as curvas com a mudança de frequência ficam mais suavizadas por conta das médias diárias. Na medida em que utilizamos as médias diárias em vez dos valores por hora, podemos estar perdendo informção ( de 9357 observações para 391), portanto ficou decidido que para as análises posteriores utilizar-se-iam dados com frequência por hora. Prossigamos para a análise da Temperatura como série temporal (observação de tendência, estacionariedade e resíduos)

# In[34]:


decompfreq = 168 # 168 = 24horas*7dias_da_semana/1hora, estamos tentando observar padrões de sazonalidade, 
                 # tendência e ciclos a cada semana. 
    
res = sm.tsa.seasonal_decompose(db_PT08['T'],
                                freq=decompfreq,
                                model='additive')
fig, (ax1,ax2,ax3,ax4) = plt.subplots(4,1, figsize=(15,8))
res.observed.plot(ax=ax1)
res.trend.plot(ax=ax2)
res.seasonal.plot(ax=ax3)
res.resid.plot(ax=ax4)


# Aparentemente, a série é estacionária, pois a tendência tem valores em torno da média e a variância aparenta ser constante. Façamos o teste de raiz unitária.

# In[35]:


result = adfuller(db_PT08['T'])
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
print('Critical Values:')
for key, value in result[4].items():
    print('\t%s: %.3f' % (key, value))


# Logo, concluimos que a série possui evidência de ser estacionária.

# Para usar o PCA, vamos colocar como variável dependente a temperatura e as demais variáveis como independentes para analisar possíveis influências de concentração de gases sobre a temperatura. A intenção dessa divisão é que possamos aplicar PCA e identificar quais variáveis melhor explicam a matriz de covariância.

# In[36]:


# Isolando as variáveis dependente e independentes
X = db_PT08.drop(['Date', 'Time', 'T'], axis = 1).values
y = db_PT08['T'].values


# Agora, vamos aplicar PCA  e descobrir quais variáveis detêm maior capacidade de explicar a matriz de covariância.

# In[37]:


pca = decomposition.PCA(n_components = None)
pca.fit(X)


# In[38]:


plt.scatter(np.arange(X.shape[1]), pca.explained_variance_ratio_)


# In[39]:


pca.components_


# CONCLUSÃO : Observando os pesos das combinações da primeira componente (que representa 80% das explicações do modelo) sabemos que a variável que apresenta maior peso dentro da componente é aquela relacionada ao NO2, o que é interessante, pois a intuição nos leva a acreditar que o mesmo seria direcionado ao CO.
