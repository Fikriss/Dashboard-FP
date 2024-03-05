import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

day_df = pd.read_csv("day_df.csv")

day_df['dteday'] = pd.to_datetime(day_df['dteday'])

min_date_day = day_df["dteday"].min()
max_date_day = day_df["dteday"].max()

with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://cdn0-production-images-kly.akamaized.net/baKr7P7mNt9DvGALEMda-RtlW7k=/1200x900/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/3169554/original/054235300_1593770750-20200703-Pemprov-DKI-Akan-Sediakan-Layanan-Bike-Sharing-angga-5.jpg")
    
    # Mengambil start_date & end_date dari date_input
    start_date_day, end_date_day = st.date_input(
        label='Rentang Waktu', min_value=min_date_day,
        max_value=max_date_day,
        value=[min_date_day, max_date_day]
    )

main_df = day_df[(day_df["dteday"] >= str(start_date_day)) & 
                     (day_df["dteday"] <= str(end_date_day))]

def resample_and_plot(day_df):
    # Resample data to monthly frequency
    monthly_df = day_df.resample(rule='M', on='dteday').sum().reset_index()

    # Plotting
    plt.figure(figsize=(12, 5))
    plt.plot(monthly_df.index, monthly_df['casual'], color='blue', label='Casual User', marker='o', markersize=5)
    plt.plot(monthly_df.index, monthly_df['registered'], color='orange', label='Registered User', marker='o', markersize=5)
    plt.xlabel('Date (Month - Year)', size=15)
    plt.ylabel('Monthly bike rented', size=15)

    # Set x-axis labels with month-year format (e.g., 1-2011, 2-2011, etc.)
    plt.xticks(ticks=monthly_df.index, labels=[date.strftime('%m-%Y') for date in monthly_df['dteday']], rotation=45)

    plt.legend()
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()
    
def plot_seasonal_data(day_df):
    # Kelompokkan data berdasarkan musim dan hitung jumlah baris dalam setiap kelompok
    jumlah_data_per_musim = day_df.groupby(by='season')['cnt'].sum()

    # Buat plot diagram batang
    plt.bar(jumlah_data_per_musim.index, jumlah_data_per_musim.values, color=['steelblue', 'steelblue', 'steelblue', 'steelblue'])
    
    # Atur label sumbu x dan y serta judul diagram
    plt.xlabel('Season')
    plt.ylabel('Total Rented Bike')
    plt.title('Jumlah Data per Musim')

    # Tampilkan diagram menggunakan st.pyplot()
    st.pyplot()

st.header('Casual vs Registered per Month over the Years')
with st.expander("How's the trend of rented bike per month over the year for the casual and registered user?"):
    st.write(
        """We can see that casual user has lower trends than registered user, but it has same pattern on maximum bik rented in May - Septmber every years (2011-2012). It means that weathershit and season really influential on bike rent.
        """
    )    
create_monthly_bike_df = resample_and_plot(main_df)
st.header('Seasonal Rent Bike Count')
with st.expander("How's the pattern of rented bike in different season?"):
    st.write(
        """We can see that the highest value season to rent bike is Fall and the lowest demand to rent bike is Spring.
        """
    )
seasonal_data_df = plot_seasonal_data(main_df)
