#Mengimpor seluruh library
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

#LOAD DATA
def load_data():
    data = pd.read_csv("hour.csv")
    return data

data = load_data()

#LOAD DATA1
def load_data1():
    data1 = pd.read_csv("day.csv")
    return data1

data1 = load_data1()

#Membuat Header
st.header('BIKE SHARE DASHBOARD :sparkles:')

#SIDEBAR
#membaca data penyewaan sepeda
hour = pd.read_csv("hour.csv")

#Mengambil tanggal terkecil dan terbesar
min_date = hour["dteday"].min()
max_date = hour["dteday"].max()
min_date = pd.to_datetime(min_date)
max_date = pd.to_datetime(max_date)

with st.sidebar:
    #Menambahkan logo
    st.image("https://cdn.pixabay.com/photo/2013/07/13/10/22/mountain-bike-157085_1280.png")

    #Mengambil start_data & end_date dari dteday_x
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = hour[(hour["dteday"] >= str(start_date)) & 
                (hour["dteday"] <= str(end_date))]

st.sidebar.title("Dataset Bike Share")
#Tampilkan dataset
if st.sidebar.checkbox("Tampilkan Dataset"):
    st.subheader("Raw Data")
    st.write(data)

#Tampilkan rangkuman statistik
    if st.sidebar.checkbox("Tunjukkan Rangkuman Statistik"):
        st.subheader("Rangkuman Statistik")
        st.write(data.describe())

#Tampilkan info dataset
st.sidebar.markdown('**Weathersit:**')
st.sidebar.markdown('1: Clear, Few clouds, Partly cloudy, Partly cloudy')
st.sidebar.markdown('2: Mist + Cloudy, Mist + Broken clouds, Mist + Few clouds, Mist')
st.sidebar.markdown('3: Light Snow, Light Rain + Thunderstorm + Scattered clouds, Light Rain + Scattered clouds')
st.sidebar.markdown('4: Heavy Rain + Ice Pallets + Thunderstorm + Mist, Snow + Fog')


#VISUALISASI
#Membuat layout 2 kolom
st.subheader("Laporan Sewa Sepeda")
col1, col2 = st.columns(2)

with col1:
    total_casual = hour["casual"].sum()
    st.write("Total Casual:", total_casual)

with col2:
    total_registered = hour["registered"].sum()
    st.write("Total Registered:", total_registered)


#Jumlah Sewa Sepeda Setiap jam
st.subheader("Jumlah Sewa Sepeda Setiap Jam")
hitung_jam = data.groupby("hr")["cnt"].sum().reset_index()
fig, ax = plt.subplots(figsize=(10,6))
ax.plot(hitung_jam["hr"], hitung_jam["cnt"])
ax.set_title("Jumlah Sewa Sepeda Setiap Jam")
ax.set_xlabel("Hour")
ax.set_ylabel("Jumlah Sewa Sepeda")
st.pyplot(fig)

#Jumlah sewa sepeda berdasarkan musim
st.subheader("Jumlah Sewa Sepeda Berdasarkan Musim")
#Mapping dari angka ke musim
season_mapping = {1: "spring", 2: "summer", 3:"fall", 4: "winter"}
data["label_season"] = data["season"].map(season_mapping)
#Menghitung jumlah sewa sepeda berdasarkan musim
hitung_season = data.groupby("label_season")["cnt"].sum().reset_index()
#Menampilkan diagram batang
fig, ax = plt.subplots(figsize=(8,6))
ax.bar(hitung_season["label_season"], hitung_season["cnt"])
ax.set_title("Jumlah Sewa Sepeda Berdasarkan Musim")
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Sewa Sepeda")
st.pyplot(fig)


#Jumlah pangsa sepeda berdasarkan cuaca
st.subheader("Jumlah Sewa Sepeda Berdasarkan Cuaca")
#menghitung jumlah sewa sepeda berdasarkan cuaca
hitung_weather = data.groupby("weathersit")["cnt"].sum().reset_index()
#Menampilkan diagram batang
fig, ax = plt.subplots(figsize=(8, 6))
ax.bar(hitung_weather["weathersit"], hitung_weather["cnt"])
ax.set_title("Jumlah Sewa Sepeda Berdasarkan Cuaca")
ax.set_xlabel("Weathersit")
ax.set_ylabel("Jumlah Sewa Sepeda")
st.pyplot(fig)


#Bagaimana cara untuk meningkatkan jumlah sewa sepeda yang digunakan pengguna tedaftar (registered) pada hari kerja (hari kerja =1)?
st.header(" Bagaimana cara untuk meningkatkan jumlah sewa sepeda yang digunakan pengguna tedaftar (registered) pada hari kerja (hari kerja =1)?")
filter_data = data1[(data1["workingday"] == 1) & (data1["registered"] > 0)]
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(filter_data["weekday"], filter_data["registered"], edgecolor='none')
ax.set_title("Jumlah Penyewa Sepeda Terdaftar pada Hari Kerja")
ax.set_xlabel("hari Kerja")
ax.set_ylabel("Jumlah Penyewa Sepeda Terdaftar")
st.pyplot(fig)


#Apa pengaruh cuaca (weathersit) pada jumlah sewa sepeda (cnt) selama musim semi (season 1)?
st.header("Apa pengaruh cuaca (weathersit) pada jumlah sewa sepeda (cnt) selama musim semi (season 1)?")
filter_data = data1[data1["season"] == 1]
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(filter_data["weathersit"], filter_data["cnt"], edgecolor='none')
ax.set_title("Pengaruh Weathersit pada Cnt")
ax.set_xlabel("Weathersit")
ax.set_ylabel("Cnt")
st.pyplot(fig)


#Temperatur vs cnt
st.subheader("Temperatur vs Cnt")
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(data["temp"], data["cnt"])
ax.set_title("Temperatur vs Cnt")
ax.set_xlabel("Temperatur")
ax.set_ylabel("Cnt")
st.pyplot(fig)
