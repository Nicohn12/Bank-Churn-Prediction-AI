import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras.layers import Dense, Input, Dropout

#Abro el csv
df = pd.read_csv(r"C:\Users\Nico\Desktop\vista_para_ml.csv")

#Convierto la columa de paises en 0 y 1
df = pd.get_dummies(df , columns = ['Geography'])

df = df * 1

#Enumero las columnas que neceisto llevar entre 0 y 1 para que ninguna valga mas que otras nominalmente
Columnas_para_escalar = [
    'CreditScore',
    'Age',
    'Tenure',
    'Balance',
    'NumOfProducts',
    'HasCrCard',
    'IsActiveMember',
    'EstimatedSalary'
]

#Las escalo entre 0 y 1
Escalador = MinMaxScaler()

df[Columnas_para_escalar] = Escalador.fit_transform(df[Columnas_para_escalar])

#Genero la entrada
x = df.drop(['CustomerId' , 'Exited'], axis=1)

#Genero la salida
y = df['Exited']

#Armo los parametros del estimador
modelo = Sequential([
    Input(shape=(x.shape[1],)),
    Dense(64, activation = 'relu'),
    Dropout(0.2),
    Dense(1, activation = 'sigmoid')   
])

modelo.compile(
    optimizer = Adam(0.001),
    loss = binary_crossentropy,
    metrics = ['accuracy']
)

historial = modelo.fit(x, y, epochs=10 , batch_size=32,validation_split=0.2 )


correlaciones = df.corr()['Exited'].drop(['Exited', 'CustomerId'])

tabla_importancia = pd.DataFrame({
    'variable' : correlaciones.index,
    'peso_influencia' : correlaciones.values,
    'importancia_absoluta' : correlaciones.abs().values
})

tabla_importancia = tabla_importancia.sort_values(by = 'importancia_absoluta', ascending= False )

print(tabla_importancia)

prediccion = modelo.predict(x) 

df_resultados = pd.DataFrame({
    'CustomerId': df['CustomerId'],           #  ID original
    'Probabilidad_Fuga': prediccion.flatten() # Predicción
})



import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

#Carga de datos a SQL
load_dotenv()

user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')
host = os.getenv('DB_HOST')
dbname = os.getenv('DB_NAME')

cadena_conexion = f'postgresql://{user}:{password}@{host}:5432/{dbname}'
engine = create_engine(cadena_conexion)

#Enviar a SQL
try:
    df_resultados.to_sql(
        name='resultados_prediccion',
        con=engine,
        if_exists='replace',  
        index=False           
    )
    print("Se guardo bien")
except Exception as e:
    print("Error")
    
tabla_importancia.to_sql('analisis_importancia', engine, if_exists='replace', index=False)    
    