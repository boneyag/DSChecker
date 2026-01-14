from sklearn.preprocessing import MinMaxScaler
import pandas as pd

df = pd.DataFrame({
    'Age': [20, 25, 30, 35],
    'Income': [40000, 50000, 60000, 1500000],
    'Gender': ['Male', 'Female', 'Female', 'Male']
})
 
scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(df[['Age', 'Income']])
