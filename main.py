import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Ваш API-ключ
api_key = '48aaef5c1amsh742439722462139p1c30d6jsn6d124ab21f82'

# URL для запроса
url = 'https://meteostat.p.rapidapi.com/stations/daily'

# Параметры запроса
params = {
    'station': '26063',
    'start': '2019-01-01',
    'end': '2023-12-31'
}

# Заголовки запроса
headers = {
    'x-rapidapi-host': 'meteostat.p.rapidapi.com',
    'x-rapidapi-key': api_key
}

# Выполнение GET-запроса
response = requests.get(url, headers=headers, params=params)

# Проверка статуса ответа
if response.status_code == 200:
    data = response.json()  # Обработка данных, если запрос успешен
    df = pd.DataFrame(data['data'])

    # Преобразование столбцов дат и температур
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df['tavg'] = (df['tmin'] + df['tmax']) / 2  # Вычисление средней температуры

    # Дисперсионный анализ (ANOVA)
    anova_result = stats.f_oneway(
        *[group['tavg'].values for name, group in df.groupby('year')]
    )
    print(f"ANOVA Result: F-statistic = {anova_result.statistic}, p-value = {anova_result.pvalue}")

    # Построение графиков
    plt.figure(figsize=(12, 6))

    # Boxplot для сравнения средних температур по годам
    sns.boxplot(x='year', y='tavg', data=df)
    plt.title('Иванов Федор Сравнение средней температуры по годам')
    plt.xlabel('Год')
    plt.ylabel('Средняя температура (°C)')
    plt.grid(True)
    plt.show()

    # Линейный график для визуализации трендов по годам
    mean_temp_per_year = df.groupby('year')['tavg'].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=mean_temp_per_year, x='year', y='tavg', marker='o')
    plt.title('Иванов Федор Средняя температура в Санкт-Петербурге (2019-2023)')
    plt.xlabel('Год')
    plt.ylabel('Средняя температура (°C)')
    plt.xticks(mean_temp_per_year['year'])
    plt.grid(True)
    plt.show()

else:
    print(f'Ошибка при получении данных: {response.status_code}')
    print(response.text)  # Вывод текста ошибки
