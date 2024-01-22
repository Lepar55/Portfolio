import pandas as pd
import matplotlib.pyplot as plt
file_path = 'D:\programming\works\project Data Science\house_ads.csv'
data = pd.read_csv(file_path)
city_data = data[data['city'] == 'Львів']

max_price = city_data['price'].max()
city_data['price'].plot(kind='hist')  
plt.title('Розподіл цін у Львові')  
plt.xlabel('Ціна')  
plt.ylabel('Частота') 

plt.axvline(x=max_price, color='r', linestyle='--', label=f'Найбільша ціна: {max_price}')  

plt.show()

print("Найбільша ціна:", max_price)