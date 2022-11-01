#!/usr/bin/env python
# coding: utf-8

# # Estudio de caso: análisis exploratorio de datos
# 
# La empresa A&A Ltda, empieza un proceso de implementación de Machine Learning, usted ha sido designado para una de las tareas más importante dentro del proyecto, el cual consisten en realizar el análisis exploratorio de los datos y documentar los resultados encontrados, generando un informe que involucre los procedimientos y los resultados. 
# El archivo que se analizara corresponde a precios de viviendas y locales para la venta y la colección de datos cuenta con variables que se ven involucradas en ese valor.
# La información se encuentra en el siguiente [enlace](https://www.datos.gov.co/Hacienda-y-Cr-dito-P-blico/Inmuebles-Disponibles-Para-La-Venta/72gd-px77/data)  la cual usted debe descargar e importar con la herramienta anaconda, el archivo lo puede exportar en formato CSV.
# 
# [vínculo de descarga](https://www.datos.gov.co/api/views/72gd-px77/rows.csv?accessType=DOWNLOAD)

# El informe debe dar cuenta de:
# * Procedimiento para la importación del archivo en formato CSV
# * Plante una pregunta objetivo
# * Total, de Registros
# * Total, de columnas
# * Detallado de cada columna
# * Identificar cuáles de las columnas son categóricas y numéricas
# * Identifique en que columnas existen valores nulos
# * Identifique si existen registros duplicados
# * Realice un reporte estadístico de los datos numéricos (media, moda, mediana, desviación estándar, cuartiles, entre otros que considere)
# * Identifique columnas con valores erróneos
# * Utilice gráficos para identificar valores atípicos
# * Realice histogramas de frecuencia
# * Use la herramienta para gráficos para determinar correlación entre variables
# * Realice y explique la eliminación de datos nulos y duplicados
# * Agrupe columnas que considere pueden generar información importante
# * Cree nuevas columnas a partir de las existentes
# * Identifique columnas que no aportan de acuerdo con su pregunta objetivo
# * Realice conclusiones sobre las variables que considere tienen mayor relevancia
# * Dejar documentado usando gráficos y capturas de pantalla todo el proceso realizado.
# 

# Se importa pandas

# In[1]:


import pandas as pd


# ## Solución
# 
# ### 1) Procedimiento para la importación del archivo en formato CSV

# In[2]:


filename = 'Inmuebles_Disponibles_Para_La_Venta.csv'


# In[3]:


data = pd.read_csv(filename)
# se ajusta el precio dividido entre 1000_000 para entender mejor la información
data['Precio'] = data['Precio']/1000_000;


# ### 2) Plantee una pregunta objetivo

# Describir el mercado actual de viviendas en Colombia comparando el valor de precios por estrato y localidad

# ### 3) Total, de Registros

# In[4]:


totalregistros = data['Codigo'].count()
print(f'total registros {totalregistros}')
# en forma alternativa 
data.shape[0]


# ### 4) Total de columnas

# In[5]:


totalcolumnas = data.shape[1];
print(f'total columnas {totalcolumnas}')


# ### 5) Detallado de cada columna

# In[6]:


data.info()


# ### 6) Identificar cuáles de las columnas son categóricas y numéricas

# In[7]:


info = data.dtypes 


# In[8]:


res = dict((key, 'Numérica') if value == 'int64' else (key, 'Categórica') for key, value in info.items())
# se muestra como un dataframe
pd.DataFrame({'Columna': res.keys(),'tipo': res.values()})


# ### 7) Identifique en que columnas existen valores nulos

# In[9]:


with_null = dict()
for key, value in data.isna().sum().items():
    if value > 0:
        with_null[key] = value
pd.DataFrame({'Columnas': with_null.keys(), 'Nulos':with_null.values() })


# ### 8) Identifique si existen registros duplicados

# In[10]:


newdata = data.drop_duplicates()
# Se hace una segunda prueba con multiples columnas
newdata = newdata.drop_duplicates(subset=['Ciudad','Departamento','Barrio','Direccion'])
duplicados = data.shape[0]- newdata.shape[0]
if duplicados == 0:
    print('No se encontraron datos repetidos')        
else:
    print(f'Hay {duplicados} registros duplicados, se procede a reemplazar la variable data con con contenidos de newdata')
    data = newdata


# In[11]:


print(f'El estudio se realizará con {data.shape[0]} filas')


# ### 9) Realice un reporte estadístico de los datos numéricos (media, moda, mediana, desviación estándar, cuartiles, entre otros que considere)

# In[12]:


data.describe()


# In[13]:


import matplotlib.pyplot as plt
fig = data.boxplot("Precio", by="Departamento");
muestras = data.shape[0];
plt.ylabel('precio');
plt.suptitle('');
plt.xticks(rotation=75);
plt.title(f'Boxplot valor por condición {muestras} muestras');


# ### Estudio de precio por cuidad y tipo de inmueble
# 
# Siempre y cuando la muestra total sea representativa (mas de 15 muestras)

# In[14]:


norepre = dict()
for tipoinmueble in data['Tipo de Inmueble'].unique():
    muestras = data[data['Tipo de Inmueble'] == tipoinmueble].shape[0]
    if muestras < 11:
        norepre[tipoinmueble] = muestras
        continue
    fig = data[data['Tipo de Inmueble'] == tipoinmueble].boxplot("Precio", by="Departamento")
    plt.ylabel('precio')
    plt.suptitle('')
    plt.xticks(rotation=75);
    plt.title(f'Tipo inmueble {tipoinmueble} sobre {muestras} muestras')
print('Inmuebles no representativos por categoría')
pd.DataFrame({'Tipo inmueble':norepre.keys(),'muestras':norepre.values()})


# In[15]:


import matplotlib.pyplot as plt


# In[16]:


# se identifica la cantida de diferenes departamentos en la muestra
def showbycity(departamento, minimo = 11):
    dpto = departamento.upper()
    muestras = data[data['Departamento'] == dpto].shape[0]
    if muestras < minimo:
        return (dpto, muestras)
    fig = data[data['Departamento'] == dpto].boxplot("Precio",by="Ciudad")
    plt.ylabel('Precio')
    plt.xticks(rotation=45);
    plt.suptitle('')
    plt.title(f'{dpto} valor por condición, {muestras} muestras')


# ### Estudio comparativo de variación de precios por cuidad

# In[17]:


# se identifican todas las cuidades
res = dict()
for departamento in data['Departamento'].unique():
    val = showbycity(departamento, minimo=10)
    if val is None:
        continue
    res[val[0]] = val[1]
print('Omitidos en este punto por cantidad de muestras insuficientes')
pd.DataFrame({'Departamento': res.keys() , 'Muestras':res.values()})


# ### Estudio comparativo de variación de precios por estrato
# Se convierte los valores de estrato a numéricos en una nueva columna, para que muestre los gráficos en orden

# In[18]:


data['Estrato'].unique()
mapa={'UNO':1,
      'DOS':2,
      'TRES':3,
      'CUATRO':4,
      'CINCO':5,
      'SEIS':6,
      'RURAL': 8,
      'COMERCIAL':9,
      'INDUSTRIAL':10,
     }
data['Estrato_num'] = data.apply(lambda row: mapa[row.Estrato], axis = 1)
data.head(5)


# ### 10) Identifique columnas con valores erróneos

# Para este punto uno de los validadores corresponde al área de terreno debe se mayor a cero, también el áre construida. Los reportes de los registros con valores erróneos se haran en archivos locales en formato csv

# In[19]:


sin_area = data[data['Area Terreno'] == 0]['Area Terreno'].count();
print(f'Cantidad de registros sin area {sin_area}')


# ### 11) Utilice gráficos para identificar valores atípicos
# 
# Ya se pueden visualizar en los puntos representados en los boxplot del punto anterior

# In[20]:


# se busca relacion entre el estrato y el valor de la vivenda
ax = data.boxplot('Precio', by='Estrato_num');
plt.suptitle('');
plt.ylim(0,100_000_000)# se modifican los límites para observar mejor los datos
plt.ylabel('Valor')
plt.xlabel('Estrato')
#plt.xticks(rotation=45);
ax.set_xticklabels(mapa.keys(), rotation='vertical', fontsize=10);


# ### 12) Realice histogramas de frecuencia
# 
# Se graficarán:
# * Cantidad de reportes por estrato
# * Cantidad de reportes por departamento
# * Rango de valores de vivienda

# In[21]:


# se define el rango de valores a graficar
from math import ceil
bins = 100
minimo = data['Precio'].min(axis=0);
maximo = data['Precio'].max(axis=0);


# In[22]:


def get_hist_values(data, minimo, maximo, bins):
    values = list();
    delta = ceil((maximo -minimo)/bins);
    initvalue = minimo;
    endvalue = minimo + delta;
    names = []
    inits = []
    ended = []
    cantidad = [] 
    k=1
    while initvalue < maximo:
        localmax = initvalue + delta + 0.01
        names.append(k)
        inits.append(initvalue)
        ended.append(localmax)
        cantidad.append(data[(data['Precio'] >= initvalue) & (data['Precio'] < localmax)].shape[0])
        initvalue = localmax
        k +=1
    print('Datos para construir el histograma');
    res = pd.DataFrame({'id': names, 'cantidad': cantidad, 'inicial': inits,'final':ended});
    return res


# In[23]:


res = get_hist_values(data, minimo, maximo, bins)
res.head(20)


# Con base en el punto anterior se nota que la mayor cantida de datos, 429, está hasta el valor de 76950021, por lo que se ajusta este como el valor límite y se corre nuevamente la función

# In[24]:


res = get_hist_values(data, minimo, 76950021 , bins=200)
res.head(20)
#ax.set_xticklabels(res['inicial'], rotation='vertical', fontsize=10);
# se procede a graficar


# In[25]:


ax = plt.bar(res['id'], res['cantidad']);
plt.ylabel("Cantidad");
plt.xlabel('Precios');
plt.title('histograma distribución de precios');


# In[26]:


# gráfica ampliada
res = get_hist_values(data, minimo, 447773.01 , bins=200)
res.head(20)


# In[27]:


# se procede a graficar
axis = plt.bar(res['id'], res['cantidad']);
plt.title('Histograma distribución de presios ampliado')
plt.ylabel("Cantidad");
plt.xlabel('Precios');
#plt.tick_params(axis='x', length=0)


# ### Función para mejorar automáticamente el rango para hacer el estudio, sacando los datos abs
# Para ello el rango a utilizar será
# * límite inferior: Q2-1.5*IQR
# * Límite superior: Q3+1.5*IQR
# 
# Donde Q2: es el cuartil 2, Q3: es el cuartil 3, IQR es el rango intercuartílico 

# ### Función para mejorar el cálculo del número de bins en forma automática
# 
# Si bien el número de bins se puede poner de forma manual sería recomendable poder hacerlo de forma automática, para ello se utilizará la fórmula de [Sturge’s rule](https://en.wikipedia.org/wiki/Histogram)

# In[28]:


import numpy as np
def get_rango(data: pd.DataFrame, colname: str):
    res = data[colname].describe()
    q2 = res['25%']
    q3 = res['75%']
    iqr = q3-q2
    minvalue = q2-1.5*iqr;
    maxvalue = q3+1.5*iqr;
    bins = int(np.ceil(np.log2(data.shape[0])) + 1)
    return (max([0,minvalue]), maxvalue, max([1, bins]))


# In[29]:


maximo, minimo, bins = get_rango(data, 'Precio');
print(f'Rango sugerido para el histograma {maximo} - {minimo}, intervalos = {bins} ')


# In[30]:


res = get_hist_values(data, maximo, minimo, bins)
res.head(20)


# In[31]:


axis = plt.bar(res['id'], res['cantidad']);
plt.title('Histograma distribución de precios')
plt.ylabel("Cantidad");
plt.xlabel('Indicador de precios');


# ### 13 Use la herramienta para gráficos para determinar correlación entre variables

# Del análisis de eliminaron las columnas de área y area construida por tener mas de 400 datos con valor cero

# In[32]:


import seaborn as sns


# In[33]:


corr = data[['Estrato_num','Codigo','Precio','Departamento']].corr()


# In[34]:


sns.heatmap(corr, linewidths=0.5, annot=True);


# Con base en la gráfica se puede notar que la mayor relación está entre el estrato y el código de la vivienda, sin embargo como este último es solo un consecutivo se puede concluir que por falta de información en cuanto a las áreas no es posible concluir sobre una relación al respecto

# ### 14) Realice y explique la eliminación de datos nulos y duplicados

# Desde el punto 8 se eliminaron los datos duplicados y en el punto 7 se presentaron las columnas con valores nulos, ahora se procederá a buscar los datos nulos en cuanto al precio

# In[35]:


data.info()


# Se filtran los contenidos con filas que tengan valores nulos en alguna de las columnas

# In[36]:


columns = [k for (k, value) in data.items()]


# In[37]:


dt = data
for k in columns:
    dt = dt[dt[k].notnull()];
dt.count()
#dropped = data.dropna(how='all', axis=1);
#dropped


# ### Resultado filas sin ningún valor nulo

# In[38]:


dt.head(min([10,dt.shape[0]]))


# ### 15) Agrupe columnas que considere pueden generar información importante
# ### 16) Cree nuevas columnas a partir de las existentes

# Se creará una columna nivel que agrupa las columnas de estrato y barrio

# In[39]:


data['Nivel'] = data.apply(lambda row: f'{row.Estrato_num} - {row.Barrio}', axis=1)
data.head(10)


# ### 17) Identifique columnas que no aportan de acuerdo con su pregunta objetivo

# Acorde con la información analizada se idenfica que las columnas que no aportan para el análisis son 
# 
# 1. Codigo
# 2. Area -  porque la mayoría son datos sin reportar o cero
# 3. Detalle Disponibilidad
# 4. Direccion

# ### 18) Realice conclusiones sobre las variables que considere tienen mayor relevancia

# Conclusiones:
# 
# 1. No se pudo realizar el análisis concluyente por no porder calcular el valor por metro cuadrado
# 2. La mayor cantidad de datos reportador fueron hast  458_220 millones
# 3. La mayor variablidad de precios se encuentra en el sector rural.
# 4. La mayor información disponible está para los **locales** con 301 muestras.
# 5. Para realizar una compra se deberá completar la información de las áreas y tomar una mejor desición con base en la evidencia
# 

# ### 19) Dejar documentado usando gráficos y capturas de pantalla todo el proceso realizado.

# Se hizo por este medio

# In[ ]:




