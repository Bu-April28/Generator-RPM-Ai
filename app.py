import streamlit as st
import google.generativeai as genai
from io import BytesIO
import pandas as pd

# 1. KONFIGURASI HALAMAN
st.set_page_config(page_title="Generator RPM AI - Kemendikdasmen", layout="wide")

# 2. FUNGSI CSS UNTUK TAMPILAN
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .report-header { text-align: center; font-family: 'Arial'; }
    </style>
    """, unsafe_allow_html=True)

# 3. KONEKSI GOOGLE GEMINI
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # --- SIDEBAR: INPUT DATA GURU & SEKOLAH ---
    st.sidebar.header("📋 Data Administrasi")
    logo_file = st.sidebar.file_uploader("Upload Logo Sekolah", type=["jpg", "png", "jpeg"])
    nama_sekolah = st.sidebar.text_input("Nama Satuan Pendidikan")
    nama_guru = st.sidebar.text_input("Nama Guru")
    nip_guru = st.sidebar.text_input("NIP Guru")
    nama_kepsek = st.sidebar.text_input("Nama Kepala Sekolah")
    tgl_buat = st.sidebar.text_input("Tanggal Pembuatan", value="... April 2026")

    # --- MAIN CONTENT: FORM INPUT RPM ---
    st.title("🤖 AI Generator: Rencana Pembelajaran Mendalam (RPM)")
    st.info("Sesuai Standar Kemendikdasmen: Adaptif & Inklusi")

    col1, col2 = st.columns(2)
    with col1:
        jenjang = st.selectbox("Jenjang Pendidikan", ["SD", "SMP", "SMA"])
        fase = st.selectbox("Fase", ["A", "B", "C", "D", "E", "F"])
        kelas = st.text_input("Kelas")
        mapel = st.text_input("Mata Pelajaran")
        materi = st.text_area("Materi Pelajaran")
        tp_input = st.text_area("Tujuan Pembelajaran (Input Awal)")

    with col2:
        pertemuan = st.number_input("Jumlah Pertemuan", min_value=1, step=1)
        alokasi = st.text_input("Alokasi Waktu (Misal: 2x45 Menit)")
        disiplin = st.text_input("Disiplin Ilmu")
        kemitraan = st.text_input("Kemitraan Pembelajaran")
        lingkungan = st.text_input("Lingkungan Pembelajaran")
        digital = st.text_input("Pemanfaatan Digital")
        sarpras = st.text_area("Sarana dan Prasarana")

    st.subheader("Capaian Pembelajaran (CP)")
    cp_fase = st.text_area("CP Per Fase")
    cp_elemen = st.text_area("CP Per Elemen")

    st.subheader("Praktik Pedagogis")
    c3, c4 = st.columns(2)
    with c3:
        pendekatan = st.text_input("Pendekatan")
        model_belajar = st.text_input("Model Pembelajaran")
    with c4:
        metode = st.text_input("Metode")
        teknik = st.text_input("Teknik")

    st.subheader("Dimensi Lulusan (Ceklis)")
    dimensi = st.multiselect("Pilih Dimensi:", 
        ["Keimanan dan ketaqwaan", "Kewargaan", "Penalaran kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"])

    # --- PROMPT LOGIC ---
    if st.button("Generate RPM Sekarang"):
        if not materi or not tp_input:
            st.warning("Materi dan Tujuan Pembelajaran wajib diisi!")
        else:
            with st.spinner("AI sedang menyusun RPM Mendalam, Adaptif, dan Inklusi..."):
                
                prompt = f"""
                Buatkan Rencana Pembelajaran Mendalam (RPM) yang sangat rinci dengan struktur berikut:
                
                1. IDENTIFIKASI
                A. Peserta Didik: Analisis mendalam aspek Kognitif, Sikap, dan Keterampilan.
                B. Materi: Ringkasan materi {materi}.
                C. Dimensi profil Lulusan: {', '.join(dimensi)}.

                2. DESAIN PEMBELAJARAN
                A. Capaian Pembelajaran: {cp_fase} & {cp_elemen}.
                B. Tujuan Pembelajaran: Ubah "{tp_input}" menjadi format ABCD (Audience, Behavior, Condition, Degree).
                C. Disiplin Ilmu: {disiplin}.
                D. Praktik Pedagogis: Pendekatan {pendekatan}, Model {model_belajar}, Metode {metode}, Teknik {teknik}.
                E. Kemitraan: {kemitraan}, F. Lingkungan: {lingkungan}, G. Digital: {digital}, H. Sarpras: {sarpras}.

                3. PENGALAMAN BELAJAR (Buat {pertemuan} pertemuan)
                Setiap pertemuan harus ada: 
                - Kegiatan Awal (Berkesadaran, Bermakna, Menyenangkan, Pertanyaan Pemantik).
                - Kegiatan Inti (Sesuai Sintak Model {model_belajar}, Memahami, Mengaplikasi).
                - Refleksi & Penutup (Berkesadaran, Bermakna, Menyenangkan).
                *Catatan: Harus ADAPTIF & INKLUSI.*

                4. ASESMEN AUTHENTIC
                - Asesmen Awal (Diagnostik).
                - Asesmen Proses (Formatif: Observasi, Rubrik Diskusi). Buatkan tabel rubrik lengkap.
                - Asesmen Akhir (Sumatif: Produk/Tugas/Presentasi). Buatkan petunjuk tugas dan rubrik penilaian rincinya.

                DATA ADMINISTRASI:
                Sekolah: {nama_sekolah}, Guru: {nama_guru}, NIP: {nip_guru}, Kepsek: {nama_kepsek}, Tanggal: {tgl_buat}.
                """

                response = model.generate_content(prompt)
                hasil_ai = response.text

                st.markdown("### 📄 Hasil Generate RPM")
                
                # Tampilkan Logo jika ada
                if logo_file:
                    st.image(logo_file, width=100)
                
                st.markdown(hasil_ai)
                
                # Tambahkan Tanda Tangan
                st.markdown(f"""
                <div style="display: flex; justify-content: space-between; margin-top: 50px;">
                    <div> Mengetahui,<br>Kepala Sekolah<br><br><br><b>{nama_kepsek}</b><br>NIP. {nip_guru}</div>
                    <div> {tgl_buat}<br>Guru Mata Pelajaran<br><br><br><b>{nama_guru}</b><br>NIP. {nip_guru}</div>
                </div>
                """, unsafe_allow_html=True)

                # --- FITUR DOWNLOAD ---
                st.subheader("📥 Unduh Hasil")
                col_dl1, col_dl2, col_dl3 = st.columns(3)
                
                # Download sebagai Markdown (Bisa dibuka di Word)
                col_dl1.download_button("Download .doc / .txt", hasil_ai, file_name=f"RPM_{materi}.doc")
                
                # Download sebagai PDF (Simulasi lewat browser print)
                col_dl2.info("Tips: Gunakan Ctrl+P untuk simpan sebagai PDF yang rapi.")
                
                # Salin Teks
                st.text_area("Salin Kode di bawah ini:", value=hasil_ai, height=200)

except Exception as e:
    st.error(f"Error: {e}. Pastikan API Key sudah terpasang di Secrets.") 
