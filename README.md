# Dashboard E-Commerce-Public-Dataset-Analysis

Welcome to the **My E-Commerce Dashboard**! Proyek ini menyediakan dashboard interaktif untuk menganalisis metrik utama dari bisnis e-commerce, termasuk kinerja penjualan, kinerja produk, perilaku pelanggan, dan lainnya. Dengan menggunakan Python, Streamlit, dan beberapa pustaka analisis data, dashboard ini memberikan gambaran yang intuitif dan visual tentang berbagai metrik bisnis.
## Demo
![My App](demo.gif)

## Fitur

- **Ringkasan Pesanan Harian**: Menampilkan tren harian dari pesanan dan kinerja penjualan.
- **Produk Terbaik dan Terburuk**: Menyediakan analisis tentang produk yang paling banyak terjual dan produk yang kurang diminati.
- **Geolokasi Pelanggan dan Penjual**: Visualisasi distribusi geografis pelanggan dan penjual.
- **Distribusi Metode Pembayaran**: Menampilkan berbagai metode pembayaran yang digunakan oleh pelanggan.
- **Analisis RFM Pelanggan**: Melakukan analisis Recency, Frequency, dan Monetary untuk mengidentifikasi segmen pelanggan.
- **Filter dan Visualisasi Interaktif**: Menggunakan kemampuan interaktif Streamlit untuk memfilter dan memvisualisasikan data berdasarkan berbagai parameter.

## Teknologi

- **Python**: Untuk pemrosesan data dan visualisasi.
- **Streamlit**: Kerangka kerja untuk membangun aplikasi web interaktif.
- **Pandas**, **NumPy**, **Matplotlib**, **Seaborn**: Pustaka yang digunakan untuk manipulasi, analisis, dan visualisasi data.

## Penjelasan Fitur Utama

1. **Ringkasan Pesanan Harian**  
   Dashboard ini memungkinkan pengguna untuk melihat tren penjualan dan pesanan setiap harinya. Pengguna dapat dengan mudah melacak fluktuasi penjualan dan menganalisis apakah ada lonjakan atau penurunan pada periode tertentu.

2. **Analisis Produk Terbaik dan Terburuk**  
   Dengan fitur ini, pengguna dapat mengetahui produk-produk yang paling banyak terjual (produk terbaik) dan produk yang tidak berkinerja baik (produk terburuk). Analisis ini membantu dalam pengambilan keputusan terkait inventarisasi dan promosi produk.

3. **Geolokasi Pelanggan dan Penjual**  
   Fitur ini memungkinkan pengguna untuk melihat sebaran geografis pelanggan dan penjual. Dengan informasi ini, pengguna dapat menganalisis pasar yang lebih potensial atau area yang perlu lebih banyak perhatian.

4. **Distribusi Metode Pembayaran**  
   Dashboard ini juga menyediakan visualisasi untuk mengetahui jenis metode pembayaran yang paling banyak digunakan oleh pelanggan. Ini memberikan wawasan tentang preferensi pembayaran yang dapat membantu dalam pengambilan keputusan bisnis.

5. **Analisis RFM (Recency, Frequency, Monetary) Pelanggan**  
   Analisis RFM digunakan untuk mengelompokkan pelanggan berdasarkan tiga kriteria:  
   - **Recency**: Seberapa baru pelanggan melakukan pembelian?  
   - **Frequency**: Seberapa sering pelanggan membeli?  
   - **Monetary**: Seberapa banyak uang yang dibelanjakan pelanggan?  
   Segmentasi ini membantu untuk mengidentifikasi pelanggan potensial dan yang membutuhkan perhatian lebih.

6. **Filter dan Visualisasi Interaktif**  
   Dengan menggunakan Streamlit, dashboard ini memungkinkan pengguna untuk memfilter data berdasarkan waktu, kategori produk, metode pembayaran, dan banyak lagi. Visualisasi yang interaktif memungkinkan analisis yang lebih mendalam dan pemahaman yang lebih baik tentang data bisnis.

## Teknologi yang Digunakan

- **Python**: Bahasa pemrograman utama yang digunakan untuk memproses dan menganalisis data. Python juga digunakan untuk mengintegrasikan pustaka visualisasi dan membangun logika aplikasi.
- **Streamlit**: Framework web yang digunakan untuk membangun dashboard interaktif. Streamlit memungkinkan pembuatan aplikasi web dengan kode Python yang minimal, membuat pengembangan dashboard lebih cepat.
- **Pandas**: Pustaka Python untuk manipulasi dan analisis data, sangat berguna dalam membersihkan dan mengolah data e-commerce.
- **NumPy**: Digunakan untuk perhitungan numerik yang efisien, terutama dalam manipulasi array dan perhitungan berbasis matriks.
- **Matplotlib dan Seaborn**: Digunakan untuk menghasilkan grafik dan visualisasi data yang dapat membantu dalam membuat insight yang lebih jelas dari data.

## Setup dan Cara Menjalankan

1. **Clone repositori**:
    ```bash
    git clone https://github.com/risdaaaa/Dashboard-E-Commerce-Public-Dataset-Analysis.git
    ```

2. **Masuk ke direktori proyek**:
    ```bash
    cd dashboard
    ```

3. **Instal dependensi yang dibutuhkan**:
    Sebelum menjalankan aplikasi, pastikan semua dependensi terinstal dengan menjalankan:
    ```bash
    pip install -r requirements.txt
    ```

4. **Jalankan aplikasi secara lokal**:
    Setelah dependensi terinstal, jalankan aplikasi Streamlit dengan perintah berikut:
    ```bash
    streamlit run dashboard.py
    ```

Setelah mengikuti langkah-langkah di atas, Anda akan dapat melihat dashboard yang telah Anda buat secara lokal melalui browser.

---

