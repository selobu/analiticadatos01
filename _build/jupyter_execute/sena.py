#!/usr/bin/env python
# coding: utf-8

# # Análisis de datos

# Se importan las librerías

# In[1]:


import pandas as pd


# a) se leen los datos al dataframe

# In[2]:


res = pd.read_csv('DatosSeguros.csv')
res.head(3)


# Descripción de los datos

# In[3]:


res.describe()


# In[4]:


res.count()


# ## importar librebrias para graficar

# In[5]:


import matplotlib.pyplot as plt


# a) comparación entre el total de fumadores contra los que pagan mas por el valor del seguro

# In[6]:


# personas que fuman
cuenta_fumadores = res[res['fumador'] == 'yes']
fuma = cuenta_fumadores['fumador'].count()
# cantidad de personas que no fuman
nofuma = res[res['fumador'] != 'yes']['fumador'].count()


# In[7]:


print(f'fumadores: {fuma}, No fumadores: {nofuma}')


# In[8]:


plt.pie(x=[fuma, nofuma], labels=['Fumadores','No fumadores'],  autopct='%1.1f%%',        explode=[0.1, 0], shadow=True)
plt.title('Figura 6 distribución porcentual de fumadores')


# Gaficar un bloxplot donde se muestre el valor del seguro agrupado por fumadores

# In[9]:


fig = res.boxplot("valor_seguro", by="fumador")
plt.ylabel('Valor_seguro')
plt.suptitle('')
plt.title('Boxplot valor por condición')


# ## Generando el heatmap

# In[10]:


import seaborn as sns


# In[11]:


dt = res[['valor_seguro','imc','hijos','edad']]


# Compute pairwise correlation of columns

# In[12]:


corr = dt.corr()


# In[13]:


sns.heatmap(corr, linewidths=0.5, annot=True)


# # Se busca agrupar los datos por rango de edades

# ## Hay que crear una columna nueva calculada

# In[14]:


dt2 = res
dt2['Rango_edad'] = dt2.apply(lambda row: [[[['E','D'][row.edad < 50], 'C'][row.edad < 40], 'B'][row.edad < 30], 'A'][row.edad < 20], axis = 1)


# In[15]:


fig = sns.relplot(x='Rango_edad' ,y='valor_seguro',hue='imc',data=dt2)
# fig.set_titles('Figura 11. Relación tres variables: valor seguro, rango de edad y el índice de masa corporal')


# In[16]:


sns.barplot(data=dt2,x='Rango_edad',y='valor_seguro', hue='fumador')


# In[ ]:




