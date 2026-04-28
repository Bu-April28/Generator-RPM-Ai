import streamlit as st
import pandas as pd
from docx import Document
from docx.shared import Inches
from io import BytesIO
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# --- KONFIGURASI API AI (Gunakan API Key Anda) ---
# Anda bisa mendapatkan API Key gratis di https://aistudio.google.com/
os_api_key = st.sidebar.text_input("Masukkan Google API Key:", type="password")
if os_api_key:
    genai.configure(api_key=os_api_key)

st.set_page_config(page_title="AI RPM Generator Pro", layout="wide")

# --- UI HEADER ---
st.title("🚀 AI Generator Rencana Pembelajaran Mendalam (RPM)")
st.caption("Edisi Lengkap: Identifikasi, Desain, Pengalaman Belajar, & Asesmen")

# --- INPUT DATA ---
with st.sidebar:
    st.header("Informasi Sekolah & Guru")
    logo = st.file_uploader("Upload Logo Sekolah", type=['png', 'jpg', 'jpeg'])
    unit = st.text_input("Nama Satuan Pendidikan")
    guru = st.text_input("Nama Guru")
    nip_g = st.text_input("NIP Guru")
    kepsek = st.text_input("Nama Kepala Sekolah")
    nip_k = st.text_input("NIP Kepala Sekolah")
    tgl_cetak = st.text_input("Tempat, Tanggal Pembuatan", value="Jakarta, 20 Mei 2024")

col1, col2 = st.columns(2)
with col1:
    jenjang = st.selectbox("Jenjang", ["SD", "SMP", "SMA"])
    fase = st.selectbox("Fase", ["A", "B", "C", "D", "E", "F"])
    kelas = st.text_input("Kelas")
    semester = st.radio("Semester", ["Ganjil", "Genap"])
    mapel = st.text_input("Mata Pelajaran")
    materi = st.text_area("Materi Pokok")
    jml_temu = st.number_input("Jumlah Pertemuan", min_value=1)
    alokasi = st.text_input("Alokasi Waktu")

with col2:
    cp = st.text_area("Capaian Pembelajaran (Fase/Elemen)")
    tujuan_awal = st.text_area("Tujuan Pembelajaran (Draft)")
    dimensi = st.multiselect("Dimensi Profil Lulusan", 
        ["Keimanan dan ketaqwaan", "Kewargaan", "Penalaran kritis", "Kreativitas", "Kolaborasi", "Kemandirian", "Kesehatan", "Komunikasi"])
    pedagogis = st.text_input("Model Pembelajaran (PBL/PjBL/Discovery/dll)")
    sarpras = st.text_area("Sarana Prasarana")

# --- LOGIKA GENERATOR AI ---
def panggil_ai(prompt):
    if not os_api_key:
        return "Silakan masukkan API Key di sidebar untuk mengaktifkan AI."
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text

if st.button("✨ Generate RPM Lengkap sekarang"):
    with st.spinner("AI sedang berpikir menyusun rencana pembelajaran mendalam..."):
        
        prompt_utama = f"""
        Buatkan Rencana Pembelajaran Mendalam (RPM) lengkap untuk:
        Mapel: {mapel}, Materi: {materi}, Kelas: {kelas}, Jenjang: {jenjang}, Fase: {fase}.
        Model: {pedagogis}. Jml Pertemuan: {jml_temu}.
        
        Output harus 4 bagian:
        1. IDENTIFIKASI: Analisis aspek kognitif, sikap, keterampilan siswa dan Dimensi: {dimensi}.
        2. DESAIN: Ubah tujuan '{tujuan_awal}' menjadi format ABCD. Detailkan Disiplin Ilmu, Lingkungan, Kemitraan, Digital.
        3. PENGALAMAN BELAJAR: Buat detail per pertemuan (1-{jml_temu}). Tiap pertemuan ada:
           - Kegiatan Awal (Pemantik, Bermakna, Menyenangkan)
           - Kegiatan Inti (Sesuai Sintak Model {pedagogis})
           - Refleksi & Penutup.
        4. ASESMEN: Buat instrumen Diagnostik, Formatif (Rubrik Observasi), dan Sumatif (Tugas/Produk) secara rinci.
        
        Gunakan bahasa Indonesia yang formal dan profesional.
        """
        
        hasil_ai = panggil_ai(prompt_utama)
        st.session_state['hasil_rpm'] = hasil_ai
        st.markdown(hasil_ai)

# --- FITUR DOWNLOAD ---
if 'hasil_rpm' in st.session_state:
    
    def buat_docx():
        doc = Document()
        if logo:
            doc.add_picture(logo, width=Inches(1))
        
        doc.add_heading(f'RENCANA PEMBELAJARAN MENDALAM - {unit}', 0)
        
        # Tabel Identitas
        table = doc.add_table(rows=5, cols=2)
        table.cell(0,0).text = "Mata Pelajaran"
        table.cell(0,1).text = f": {mapel}"
        table.cell(1,0).text = "Kelas/Semester"
        table.cell(1,1).text = f": {kelas} / {semester}"
        # ... tambahkan baris lain
        
        doc.add_paragraph("\n" + st.session_state['hasil_rpm'])
        
        # Tanda Tangan
        doc.add_paragraph(f"\n\n{tgl_cetak}")
        ttd = doc.add_table(rows=1, cols=2)
        ttd.cell(0,0).text = f"Mengetahui,\nKepala Sekolah\n\n\n\n{kepsek}\nNIP. {nip_k}"
        ttd.cell(0,1).text = f"Guru Mata Pelajaran\n\n\n\n{guru}\nNIP. {nip_g}"
        
        out = BytesIO()
        doc.save(out)
        return out.getvalue()

    st.divider()
    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button("📩 Download Word (.docx)", data=buat_docx(), file_name=f"RPM_{mapel}.docx")
    with col_dl2:
        st.button("📋 Salin Semua Teks")
    
    st.success("RPM Berhasil dibuat! Silakan download file di atas.")
