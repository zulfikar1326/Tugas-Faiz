import streamlit as st
from streamlit_option_menu import option_menu
import datetime
import pandas as pd

# Kelas Buku dan Turunannya
class Buku:
    def __init__(self, judul, penulis, tahun_terbit):
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.status = "tersedia"
        self.tanggal_peminjaman = None

    def info_buku(self):
        return f"Judul: {self.judul}, Penulis: {self.penulis}, Tahun Terbit: {self.tahun_terbit}, Status: {self.status}"

class BukuDigital(Buku):
    def __init__(self, judul, penulis, tahun_terbit, ukuran_file, format_file):
        super().__init__(judul, penulis, tahun_terbit)
        self.ukuran_file = ukuran_file
        self.format_file = format_file

    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Ukuran File: {self.ukuran_file}MB, Format: {self.format_file}"

class BukuFisik(Buku):
    def __init__(self, judul, penulis, tahun_terbit, jumlah_halaman, berat):
        super().__init__(judul, penulis, tahun_terbit)
        self.jumlah_halaman = jumlah_halaman
        self.berat = berat

    def info_buku(self):
        info = super().info_buku()
        return f"{info}, Jumlah Halaman: {self.jumlah_halaman}, Berat: {self.berat} gram"

class Perpustakaan:
    def __init__(self):
        self.daftar_buku = []

    def tambah_buku(self, buku):
        self.daftar_buku.append(buku)

    def cari_buku(self, judul):
        for buku in self.daftar_buku:
            if buku.judul.lower() == judul.lower():
                return buku
        return None

    def tampilkan_semua_buku(self):
        return [buku.info_buku() for buku in self.daftar_buku]

    def pinjam_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "tersedia":
            buku.status = "dipinjam"
            buku.tanggal_peminjaman = datetime.datetime.now()
            return f"Buku '{judul}' berhasil dipinjam."
        else:
            return f"Buku '{judul}' tidak tersedia untuk dipinjam."

    def kembalikan_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku and buku.status == "dipinjam":
            buku.status = "tersedia"
            buku.tanggal_peminjaman = None
            return f"Buku '{judul}' berhasil dikembalikan."
        else:
            return f"Buku '{judul}' tidak sedang dipinjam."

    def hapus_buku(self, judul):
        buku = self.cari_buku(judul)
        if buku:
            self.daftar_buku.remove(buku)
            return f"Buku '{judul}' berhasil dihapus."
        else:
            return f"Buku '{judul}' tidak ditemukan."

    def update_info_buku(self, judul, penulis=None, tahun_terbit=None):
        buku = self.cari_buku(judul)
        if buku:
            if penulis:
                buku.penulis = penulis
            if tahun_terbit:
                buku.tahun_terbit = tahun_terbit
            return f"Informasi buku '{judul}' berhasil diperbarui."
        else:
            return f"Buku '{judul}' tidak ditemukan."

    def buku_terlambat(self):
        buku_terlambat = []
        for buku in self.daftar_buku:
            if buku.status == "dipinjam" and buku.tanggal_peminjaman:
                if (datetime.datetime.now() - buku.tanggal_peminjaman).days > 7:
                    buku_terlambat.append(buku)
        return buku_terlambat

# Fungsi untuk menyimpan data ke file Excel
def simpan_data_excel(perpustakaan):
    data = []
    for buku in perpustakaan.daftar_buku:
        data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.status])
    df = pd.DataFrame(data, columns=["Judul", "Penulis", "Tahun Terbit", "Status"])
    df.to_excel("daftar_buku.xlsx", index=False)

# Inisialisasi perpustakaan di session state
if 'perpustakaan' not in st.session_state:
    st.session_state.perpustakaan = Perpustakaan()

perpustakaan = st.session_state.perpustakaan

# Pilihan menu
with st.sidebar:
    selected = option_menu(
        menu_title="Menu",
        options=["Tambah Buku", "Cari Buku", "Tampilkan Semua Buku", "Pinjam Buku", "Kembalikan Buku", "Hapus Buku", "Update Info Buku", "Buku Terlambat"],
        icons=["book", "search", "list", "book", "book", "trash", "pencil", "exclamation-triangle"],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#3498db"},
            "icon": {"color": "#27ae60", "font-size": "25px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#2980b9"},
            "nav-link-selected": {"background-color": "#27ae60"},
        }
    )

st.markdown(
    """
    <style>
    .main {
        background-color: #3498db;
        color: #fff;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #fff;
    }
    .stTextInput > div > div > input {
        color: #fff;
        background-color: #27ae60;
    }
    .stNumberInput > div > div > input {
        color: #fff;
        background-color: #27ae60;
    }
    .stButton > button {
        color: #fff;
        background-color: #2980b9;
    }
    .stRadio > div > div {
        color: #fff;
    }
    .css-1d391kg {
        background-color: #3498db;
        color: #fff;
    }
    .css-1aumxhk {
        background-color: #3498db;
        color: #fff;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if selected == "Tambah Buku":
    st.header("Tambah Buku Baru")

    jenis_buku = st.radio("Jenis Buku", ("Buku Fisik", "Buku Digital"))

    judul = st.text_input("Judul Buku")
    penulis = st.text_input("Penulis")
    tahun_terbit = st.number_input("Tahun Terbit", min_value=1000, max_value=datetime.datetime.now().year, step=1)

    if jenis_buku == "Buku Fisik":
        jumlah_halaman = st.number_input("Jumlah Halaman", min_value=1, step=1)
        berat = st.number_input("Berat (gram)", min_value=1, step=1)
        if st.button("Tambah Buku"):
            buku = BukuFisik(judul, penulis, tahun_terbit, jumlah_halaman, berat)
            perpustakaan.tambah_buku(buku)
            simpan_data_excel(perpustakaan)
            st.success("Buku fisik berhasil ditambahkan.")
    else:
        ukuran_file = st.number_input("Ukuran File (MB)", min_value=0.1, step=0.1)
        format_file = st.text_input("Format File")
        if st.button("Tambah Buku"):
            buku = BukuDigital(judul, penulis, tahun_terbit, ukuran_file, format_file)
            perpustakaan.tambah_buku(buku)
            simpan_data_excel(perpustakaan)
            st.success("Buku digital berhasil ditambahkan.")

elif selected == "Cari Buku":
    st.header("Cari Buku")
    judul = st.text_input("Masukkan Judul Buku")
    if st.button("Cari"):
        buku = perpustakaan.cari_buku(judul)
        if buku:
            st.write(buku.info_buku())
        else:
            st.warning("Buku tidak ditemukan.")

elif selected == "Tampilkan Semua Buku":
    st.header("Daftar Semua Buku")
    semua_buku = perpustakaan.tampilkan_semua_buku()
    if semua_buku:
        for info_buku in semua_buku:
            st.write(info_buku)
    else:
        st.write("Tidak ada buku yang ditemukan.")

elif selected == "Pinjam Buku":
    st.header("Pinjam Buku")
    judul = st.text_input("Masukkan Judul Buku")
    if st.button("Pinjam"):
        pesan = perpustakaan.pinjam_buku(judul)
        st.write(pesan)

elif selected == "Kembalikan Buku":
    st.header("Kembalikan Buku")
    judul = st.text_input("Masukkan Judul Buku")
    if st.button("Kembalikan"):
        pesan = perpustakaan.kembalikan_buku(judul)
        st.write(pesan)

elif selected == "Hapus Buku":
    st.header("Hapus Buku")
    judul = st.text_input("Masukkan Judul Buku")
    if st.button("Hapus"):
        pesan = perpustakaan.hapus_buku(judul)
        st.write(pesan)

elif selected == "Update Info Buku":
    st.header("Update Info Buku")
    judul = st.text_input("Masukkan Judul Buku")
    penulis_baru = st.text_input("Penulis Baru (opsional)")
    tahun_terbit_baru = st.number_input("Tahun Terbit Baru (opsional)", min_value=1000, max_value=datetime.datetime.now().year, step=1)

    if st.button("Update"):
        pesan = perpustakaan.update_info_buku(judul, penulis_baru if penulis_baru else None, tahun_terbit_baru if tahun_terbit_baru else None)
        st.write(pesan)

elif selected == "Buku Terlambat":
    st.header("Daftar Buku Terlambat")
    buku_terlambat = perpustakaan.buku_terlambat()
    if buku_terlambat:
        data = []
        for buku in buku_terlambat:
            data.append([buku.judul, buku.penulis, buku.tahun_terbit, buku.tanggal_peminjaman, (datetime.datetime.now() - buku.tanggal_peminjaman).days])
        df = pd.DataFrame(data, columns=["Judul", "Penulis", "Tahun Terbit", "Tanggal Peminjaman", "Hari Terlambat"])
        st.table(df)
    else:
        st.write("Tidak ada buku yang terlambat.")
