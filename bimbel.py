import streamlit as st 
import pandas as pd 
import numpy as np 
import re 
import plotly.express as px 
import plotly.graph_objects as go 
 
# ============================================================ 
# KONFIGURASI 
# ============================================================ 
 
st.set_page_config( 
    page_title="Dashboard Keuangan Bimbel 2026", 
    page_icon="💰", 
    layout="wide", 
    initial_sidebar_state="expanded" 
) 
 
# Palet visual dashboard 
px.defaults.template = "plotly_white" 
px.defaults.color_discrete_sequence = [ 
    "#1976A8", "#F59E0B", "#10B981", "#8B5CF6", 
    "#EF4444", "#06B6D4", "#64748B", "#EC4899" 
] 
 
# ============================================================ 
# STYLE 
# ============================================================ 
 
st.markdown( 
    """ 
<style> 
    /* ===================== GLOBAL ===================== */ 
    .stApp { 
        background: #f5f7fb; 
    } 
 
    .main .block-container { 
        padding-top: 2rem; 
        padding-bottom: 3rem; 
        max-width: 1500px; 
    } 
 
    /* Semua teks umum dibuat hitam/gelap agar kontras */ 
    body, p, span, label, div { 
        color: #1e293b; 
    } 
 
    /* ===================== HEADER ===================== */ 
    .dashboard-hero { 
        background: linear-gradient(135deg, #0f2747 0%, #164e78 55%, #1976a8 100%); 
        padding: 28px 32px; 
        border-radius: 22px; 
        margin-bottom: 20px; 
        box-shadow: 0 10px 30px rgba(15, 39, 71, 0.16); 
        color: #ffffff !important; 
    } 
 
    .dashboard-hero .main-title { 
        color: #ffffff !important; 
        font-size: 32px; 
        font-weight: 800; 
        margin: 0 0 6px 0; 
        letter-spacing: -0.5px; 
    } 
 
    .dashboard-hero .subtitle { 
        color: rgba(255,255,255,.82) !important; 
        font-size: 14px; 
        margin: 0; 
    } 
 
    .section-title { 
        font-size: 21px; 
        font-weight: 800; 
        color: #102a43 !important; 
        margin-top: 30px; 
        margin-bottom: 14px; 
        padding-left: 12px; 
        border-left: 5px solid #1976a8; 
    } 
 
    .small-note { 
        color: #667085 !important; 
        font-size: 13px; 
    } 
 
    /* ===================== KPI ===================== */ 
    div[data-testid="stMetric"] { 
        background: #ffffff; 
        border: 1px solid #e4e9f0; 
        border-radius: 17px; 
        padding: 18px 20px; 
        min-height: 115px; 
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.055); 
        transition: all .2s ease; 
    } 
 
    div[data-testid="stMetric"]:hover { 
        transform: translateY(-2px); 
        box-shadow: 0 9px 24px rgba(15, 23, 42, 0.09); 
        border-color: #cbd8e6; 
    } 
 
    /* Label KPI */ 
    div[data-testid="stMetricLabel"], 
    div[data-testid="stMetricLabel"] p, 
    div[data-testid="stMetricLabel"] label, 
    div[data-testid="stMetricLabel"] span { 
        color: #000000 !important; 
        opacity: 1 !important; 
        font-size: 12px !important; 
        font-weight: 800 !important; 
        text-transform: uppercase; 
        letter-spacing: .35px; 
        line-height: 1.4 !important; 
    } 
 
    /* Nilai KPI */ 
    div[data-testid="stMetricValue"], 
    div[data-testid="stMetricValue"] * { 
        color: #000000 !important; 
        font-size: 25px !important; 
        font-weight: 800 !important; 
    } 
 
    /* ===================== SIDEBAR ===================== */ 
    section[data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #0f2747 0%, #123b5d 55%, #0e2a44 100%); 
    } 
 
    section[data-testid="stSidebar"] .stMarkdown h1, 
    section[data-testid="stSidebar"] .stMarkdown h2, 
    section[data-testid="stSidebar"] .stMarkdown h3, 
    section[data-testid="stSidebar"] .stMarkdown p { 
        color: #f8fafc !important; 
    } 
 
    section[data-testid="stSidebar"] hr { 
        border-color: rgba(255,255,255,.16); 
    } 
 
    section[data-testid="stSidebar"] .stSelectbox label, 
    section[data-testid="stSidebar"] .stMultiSelect label, 
    section[data-testid="stSidebar"] .stFileUploader label { 
        color: #ffffff !important; 
        font-weight: 600 !important; 
    } 
 
    /* Memastikan teks opsi/pilihan di dalam dropdown/multiselect berwarna hitam */ 
    div[data-baseweb="select"] * { 
        color: #000000 !important; 
    } 
 
    /* Menjaga latar belakang kotak pencarian/input di sidebar */ 
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div { 
        background: #ffffff !important; 
        border: 1px solid rgba(255,255,255,.18); 
        border-radius: 10px; 
    } 
 
    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] { 
        background: rgba(255,255,255,.08); 
        border: 1px dashed rgba(255,255,255,.30); 
        border-radius: 12px; 
    } 
 
    /* ===================== INFO / ALERT ===================== */ 
    div[data-testid="stAlert"] { 
        border-radius: 13px; 
        border: 1px solid #dbe5ef; 
    } 
 
    div[data-testid="stAlert"] * { 
        color: #0f172a !important; 
    } 
 
    /* ===================== CHART CONTAINER ===================== */ 
    div[data-testid="stPlotlyChart"] { 
        background: #ffffff; 
        border: 1px solid #e4e9f0; 
        border-radius: 17px; 
        padding: 8px; 
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.045); 
        margin-bottom: 8px; 
    } 
 
    /* ===================== TABLE ===================== */ 
    div[data-testid="stDataFrame"] { 
        border: 1px solid #e4e9f0; 
        border-radius: 14px; 
        overflow: hidden; 
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04); 
        background: #ffffff; 
    } 
 
    div[data-testid="stDataFrame"] * { 
        color: #000000 !important; 
    } 
 
    /* ===================== BUTTON ===================== */ 
    .stDownloadButton > button { 
        width: 100%; 
        border-radius: 11px; 
        font-weight: 700; 
        border: 1px solid #1976a8; 
        color: #000000 !important; 
    } 
 
    /* ===================== EXPANDER ===================== */ 
    div[data-testid="stExpander"] { 
        background: #ffffff; 
        border: 1px solid #e4e9f0; 
        border-radius: 14px; 
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04); 
    } 
 
    div[data-testid="stExpander"] * { 
        color: #000000 !important; 
    } 
 
    /* ===================== SPACING ===================== */ 
    .stCaption { 
        color: #667085 !important; 
    } 
 
    /* Mobile Responsive */ 
    @media (max-width: 768px) { 
        .main .block-container { 
            padding: 1rem .8rem 2rem .8rem; 
        } 
 
        .dashboard-hero { 
            padding: 22px; 
            border-radius: 17px; 
        } 
 
        .dashboard-hero .main-title { 
            font-size: 25px; 
        } 
 
        div[data-testid="stMetricValue"] { 
            font-size: 20px !important; 
        } 
    } 
</style> 
""", 
    unsafe_allow_html=True, 
) 
 
# ============================================================ 
# HELPER 
# ============================================================ 
 
def normalisasi_teks(x): 
    if pd.isna(x): 
        return "" 
    x = str(x).replace("\n", " ").replace("\r", " ").replace("\t", " ") 
    return re.sub(r"\s+", " ", x).strip() 
 
 
def key_teks(x): 
    return re.sub(r"\s+", "", normalisasi_teks(x)).casefold() 
 
 
def rupiah(x): 
    try: 
        x = float(x) 
        return "Rp{:,.0f}".format(x).replace(",", ".") 
    except Exception: 
        return "Rp0" 
 
 
def clean_numeric(series): 
    if series is None: 
        return pd.Series(dtype=float) 
 
    def parse(x): 
        if pd.isna(x) or str(x).strip() == "": 
            return 0.0 
 
        if isinstance(x, (int, float, np.integer, np.floating)): 
            return float(x) 
 
        s = str(x).strip() 
        s = s.replace("Rp", "").replace("rp", "").replace(" ", "") 
        s = s.replace("\u00a0", "") 
 
        # Format Indonesia: 1.234.567,89 
        if "." in s and "," in s: 
            s = s.replace(".", "").replace(",", ".") 
        # Angka seperti 1.234.567 
        elif re.fullmatch(r"-?\d{1,3}(\.\d{3})+", s): 
            s = s.replace(".", "") 
        else: 
            s = s.replace(",", "") 
 
        s = re.sub(r"[^0-9.\-]", "", s) 
 
        try: 
            return float(s) 
        except Exception: 
            return 0.0 
 
    return series.apply(parse) 
 
 
def format_tabel_rupiah(df, kolom): 
    df = df.copy() 
    for col in kolom: 
        if col in df.columns: 
            df[col] = df[col].apply(rupiah) 
    return df 
 
 
def find_col(df, candidates): 
    normalized = {key_teks(c): c for c in df.columns} 
 
    # exact 
    for c in candidates: 
        k = key_teks(c) 
        if k in normalized: 
            return normalized[k] 
 
    # contains 
    for c in candidates: 
        k = key_teks(c) 
        for nk, original in normalized.items(): 
            if k and (k in nk or nk in k): 
                return original 
 
    return None 
 
 
def normalisasi_semua_teks(df): 
    df = df.copy() 
 
    for col in df.columns: 
        mapping = {} 
 
        for value in df[col]: 
            if not isinstance(value, str): 
                continue 
 
            k = key_teks(value) 
            if not k: 
                continue 
 
            if k not in mapping: 
                mapping[k] = normalisasi_teks(value) 
 
        if mapping: 
            df[col] = df[col].apply( 
                lambda x: mapping.get(key_teks(x), normalisasi_teks(x)) 
                if isinstance(x, str) else x 
            ) 
 
    return df 
 
 
# ============================================================ 
# PEMBACA SHEET LAPORAN 
# ============================================================ 
 
def baca_laporan_khusus(uploaded_file, sheet_name="LAPORAN"): 
    raw = pd.read_excel( 
        uploaded_file, 
        sheet_name=sheet_name, 
        header=None 
    ) 
 
    if raw.empty or len(raw) < 3: 
        return pd.DataFrame(), {} 
 
    # 1. Olah Header 
    header_atas = raw.iloc[1].fillna("").tolist() 
    header_bawah = raw.iloc[2].fillna("").tolist() 
 
    headers = [] 
    for atas, bawah in zip(header_atas, header_bawah): 
        a = normalisasi_teks(atas) 
        b = normalisasi_teks(bawah) 
        header = b if b else a 
        headers.append(header) 
 
    final_headers = [] 
    counter = {} 
    for i, h in enumerate(headers): 
        if not h: 
            h = f"KOLOM_{i+1}" 
        base = h 
        if base in counter: 
            counter[base] += 1 
            h = f"{base} ({counter[base]})" 
        else: 
            counter[base] = 1 
        final_headers.append(h) 
 
    # 2. Ambil data mulai baris ke-3 
    data = raw.iloc[3:].copy() 
    data.columns = final_headers 
    data = data.reset_index(drop=True) 
 
    # 3. Temukan Aliases Kolom 
    aliases = { 
        "bulan": find_col(data, ["BULAN"]), 
        "tanggal": find_col(data, ["TANGGAL"]), 
        "nama_siswa": find_col(data, ["NAMA SISWA"]), 
        "status_klien": find_col(data, ["STATUS BARU/ REPEAT ORDER"]), 
        "jumlah_pertemuan": find_col(data, ["JUMLAH PERTEMUAN"]), 
        "sudah_berjalan": find_col(data, ["SUDAH BERJALAN"]), 
        "sisa_pertemuan": find_col(data, ["SISA PERTEMUAN"]), 
        "biaya_les": find_col(data, ["BIAYA LES"]), 
        "sudah_dibayar": find_col(data, ["SUDAH DIBAYAR"]), 
        "sisa_pembayaran": find_col(data, ["SISA PEMBAYARAN"]), 
        "metode": find_col(data, ["METODE PEMBAYARAN"]), 
        "status_pembayaran": find_col(data, ["STATUS PEMBAYARAN"]), 
        "tentor": find_col(data, ["TENTOR"]), 
        "total_fee_tentor": find_col(data, ["TOTAL FEE"]), 
        "fee_dibayar": find_col(data, ["SUDAH DIBAYAR"]), 
        "kekurangan_fee": find_col(data, ["KEKURANGAN FEE"]), 
        "catatan": find_col(data, ["CATATAN"]), 
    } 
 
    if len(data.columns) >= 15: 
        aliases["sudah_dibayar"] = data.columns[8] 
        aliases["fee_dibayar"] = data.columns[14] 
 
    # 4. TERAPKAN NORMALISASI SPASI TERLEBIH DAHULU KE SEMUA KOLOM TEKS 
    for col in data.columns: 
        data[col] = data[col].apply(normalisasi_teks) 
 
    # 5. FILTER BARIS VALIDE (Toleran terhadap spasi) 
    col_siswa = aliases.get("nama_siswa") 
    col_tentor = aliases.get("tentor") 
    col_biaya = aliases.get("biaya_les") 
 
    # Baris dianggap valid jika minimal ada Nama Siswa, ATAU Tentor, ATAU Biaya Les 
    conditions = [] 
    if col_siswa: 
        conditions.append(data[col_siswa] != "") 
    if col_tentor: 
        conditions.append(data[col_tentor] != "") 
    if col_biaya: 
        conditions.append(data[col_biaya] != "") 
 
    if conditions: 
        mask_valid = conditions[0] 
        for cond in conditions[1:]: 
            mask_valid = mask_valid | cond 
        data = data.loc[mask_valid].reset_index(drop=True) 
 
    # 6. Proses Tanggal & Bulan 
    if aliases["bulan"]: 
        data[aliases["bulan"]] = data[aliases["bulan"]].replace("", np.nan).ffill() 
 
    if aliases["tanggal"]: 
        data[aliases["tanggal"]] = pd.to_datetime( 
            data[aliases["tanggal"]], errors="coerce" 
        ) 
 
    # 7. Cleaning Kolom Numerik 
    for key in [ 
        "jumlah_pertemuan", "sudah_berjalan", "sisa_pertemuan", 
        "biaya_les", "sudah_dibayar", "sisa_pembayaran", 
        "total_fee_tentor", "fee_dibayar", "kekurangan_fee" 
    ]: 
        col = aliases.get(key) 
        if col: 
            data[col] = clean_numeric(data[col]) 
 
    # 8. Kolom Turunan Tanggal 
    if aliases["tanggal"]: 
        data["Tahun"] = data[aliases["tanggal"]].dt.year 
        data["Bulan_Nomor"] = data[aliases["tanggal"]].dt.month 
        data["Periode"] = data[aliases["tanggal"]].dt.strftime("%Y-%m") 
        data["Nama_Bulan"] = data[aliases["tanggal"]].dt.strftime("%B") 
    else: 
        data["Tahun"] = np.nan 
        data["Bulan_Nomor"] = np.nan 
        data["Periode"] = "" 
        data["Nama_Bulan"] = "" 
 
    return data, aliases 
 
# ============================================================ 
# BACA SHEET BIASA 
# ============================================================ 
 
def baca_sheet_umum(uploaded_file, sheet_name): 
    """Membaca sheet Excel biasa dengan baris pertama sebagai header.""" 
    try: 
        data = pd.read_excel( 
            uploaded_file, 
            sheet_name=sheet_name, 
            header=0 
        ) 
        data = data.copy() 
        data.columns = [normalisasi_teks(c) for c in data.columns] 
        data = normalisasi_semua_teks(data) 
        return data.reset_index(drop=True) 
    except Exception as e: 
        st.error(f"Gagal membaca sheet {sheet_name}: {e}") 
        return pd.DataFrame() 
 
 
def normalisasi_teks(x): 
    if pd.isna(x): 
        return "" 
    # Ubah ke string & bersihkan spasi tak kasat mata (non-breaking space) 
    x = str(x).replace("\u00a0", " ").replace("\xa0", " ") 
    x = x.replace("\n", " ").replace("\r", " ").replace("\t", " ") 
    # Hapus spasi berlebih di tengah & spasi di awal/akhir (strip) 
    x = re.sub(r"\s+", " ", x) 
    return x.strip() 
 
 
# ============================================================ 
# SIDEBAR 
# ============================================================ 
 
st.sidebar.markdown( 
    '<div style="padding:8px 0 14px 0;">' 
    '<div style="font-size:27px;font-weight:800;color:white;">💰 Bimbel 2026</div>' 
    '<div style="font-size:13px;color:#bfdbfe;margin-top:4px;">' 
    'Dashboard Keuangan & Operasional</div>' 
    '</div>', 
    unsafe_allow_html=True 
) 
st.sidebar.divider() 
 
uploaded_file = st.sidebar.file_uploader( 
    "📁 Upload Laporan Keuangan", 
    type=["xlsx", "xls"] 
) 
 
if uploaded_file is None: 
    st.markdown( 
        '<div class="dashboard-hero">' 
        '<div class="main-title">💰 Dashboard Keuangan Bimbel 2026</div>' 
        '<div class="subtitle">Upload laporan Excel untuk melihat ringkasan ' 
        'keuangan dan operasional bimbel.</div>' 
        '</div>', 
        unsafe_allow_html=True 
    ) 
    st.info("👈 Upload file Excel di sidebar untuk memulai.") 
    st.stop() 
 
# ============================================================ 
# SHEET 
# ============================================================ 
 
try: 
    xls = pd.ExcelFile(uploaded_file) 
    daftar_sheet = xls.sheet_names 
except Exception as e: 
    st.error(f"Gagal membaca Excel: {e}") 
    st.stop() 
 
st.sidebar.markdown("### 📑 Pilih Sheet") 
 
default_sheet_idx = ( 
    daftar_sheet.index("LAPORAN") 
    if "LAPORAN" in daftar_sheet 
    else 0 
) 
 
sheet_pilihan = st.sidebar.selectbox( 
    "Sheet yang digunakan:", 
    daftar_sheet, 
    index=default_sheet_idx 
) 
 
# LAPORAN menjadi sumber utama dashboard 
if sheet_pilihan == "LAPORAN": 
    df, aliases = baca_laporan_khusus( 
        uploaded_file, 
        "LAPORAN" 
    ) 
else: 
    df = baca_sheet_umum( 
        uploaded_file, 
        sheet_pilihan 
    ) 
    aliases = { 
        "bulan": find_col(df, ["BULAN"]), 
        "tanggal": find_col(df, ["TANGGAL", "TANGGAL DEAL"]), 
        "nama_siswa": find_col(df, ["NAMA SISWA", "NAMA"]), 
        "status_klien": find_col(df, ["STATUS BARU/ REPEAT ORDER", "STATUS"]), 
        "biaya_les": find_col(df, ["BIAYA LES", "BIAYA"]), 
        "sudah_dibayar": find_col(df, ["PEMASUKAN", "SUDAH DIBAYAR"]), 
        "sisa_pembayaran": find_col(df, ["SISA PEMBAYARAN", "PIUTANG"]), 
        "metode": find_col(df, ["METODE PEMBAYARAN"]), 
        "status_pembayaran": find_col(df, ["STATUS PEMBAYARAN"]), 
        "tentor": find_col(df, ["TENTOR", "NAMA TUTOR"]), 
        "total_fee_tentor": find_col(df, ["TOTAL FEE", "FEE TUTOR"]), 
        "fee_dibayar": find_col(df, ["SUDAH DIBAYAR"]), 
        "kekurangan_fee": find_col(df, ["KEKURANGAN FEE", "FEE BELUM TERBAYAR"]), 
        "catatan": find_col(df, ["CATATAN"]) 
    } 
 
# ============================================================ 
# CEK DATA 
# ============================================================ 
 
if df.empty: 
    st.warning("Data pada sheet tersebut kosong atau tidak dapat dibaca.") 
    st.stop() 
 
# ============================================================ 
# HEADER 
# ============================================================ 
 
st.markdown( 
    '<div class="dashboard-hero">' 
    '<div class="main-title">💰 Dashboard Keuangan Bimbel 2026</div>' 
    '<div class="subtitle">Monitoring keuangan, pembayaran siswa, piutang, ' 
    'fee tentor, dan aktivitas operasional dalam satu dashboard.</div>' 
    '</div>', 
    unsafe_allow_html=True 
) 
 
st.info( 
    f"📄 **{uploaded_file.name}**  ·  " 
    f"📑 Sheet: **{sheet_pilihan}**  ·  " 
    f"📊 **{len(df):,}** baris data terbaca".replace(",", ".") 
) 
 
# ============================================================ 
# FILTER 
# ============================================================ 
 
st.sidebar.markdown("### 🔎 Filter Dashboard") 
 
df_filter = df.copy() 
 
if "Tahun" in df_filter.columns: 
    tahun_valid = sorted( 
        pd.to_numeric(df_filter["Tahun"], errors="coerce") 
        .dropna() 
        .astype(int) 
        .unique() 
        .tolist() 
    ) 
else: 
    tahun_valid = [] 
 
if tahun_valid: 
    tahun_pilihan = st.sidebar.multiselect( 
        "Tahun:", 
        tahun_valid, 
        default=tahun_valid 
    ) 
    df_filter = df_filter[ 
        df_filter["Tahun"].isin(tahun_pilihan) 
    ] 
 
# ============================================================ 
# FILTER BULAN — PERBAIKAN 
# ============================================================ 
# Semua bulan Januari-Desember selalu ditampilkan. 
# Filter tetap menggunakan Bulan_Nomor dari kolom TANGGAL. 
 
bulan_dict = { 
    1: "Januari", 
    2: "Februari", 
    3: "Maret", 
    4: "April", 
    5: "Mei", 
    6: "Juni", 
    7: "Juli", 
    8: "Agustus", 
    9: "September", 
    10: "Oktober", 
    11: "November", 
    12: "Desember" 
} 
 
if "Bulan_Nomor" in df_filter.columns: 
 
    # Selalu tampilkan 12 bulan 
    bulan_tersedia = list(range(1, 13)) 
 
    bulan_pilihan = st.sidebar.multiselect( 
        "Bulan:", 
        options=bulan_tersedia, 
        default=bulan_tersedia, 
        format_func=lambda x: bulan_dict.get(x, str(x)) 
    ) 
 
    if bulan_pilihan: 
        df_filter = df_filter[ 
            pd.to_numeric( 
                df_filter["Bulan_Nomor"], 
                errors="coerce" 
            ).isin(bulan_pilihan) 
        ] 
 
if aliases.get("status_klien") and aliases["status_klien"] in df_filter.columns: 
    vals = sorted([ 
        x for x in df_filter[aliases["status_klien"]].dropna().unique() 
        if normalisasi_teks(x) 
    ]) 
    status_klien_pilih = st.sidebar.multiselect( 
        "Status Klien:", 
        vals, 
        default=vals 
    ) 
    if status_klien_pilih: 
        df_filter = df_filter[ 
            df_filter[aliases["status_klien"]].isin(status_klien_pilih) 
        ] 
 
if aliases.get("status_pembayaran") and aliases["status_pembayaran"] in df_filter.columns: 
    vals = sorted([ 
        x for x in df_filter[aliases["status_pembayaran"]].dropna().unique() 
        if normalisasi_teks(x) 
    ]) 
    status_bayar_pilih = st.sidebar.multiselect( 
        "Status Pembayaran:", 
        vals, 
        default=vals 
    ) 
    if status_bayar_pilih: 
        df_filter = df_filter[ 
            df_filter[aliases["status_pembayaran"]].isin(status_bayar_pilih) 
        ] 
 
if aliases.get("tentor") and aliases["tentor"] in df_filter.columns: 
    vals = sorted([ 
        x for x in df_filter[aliases["tentor"]].dropna().unique() 
        if normalisasi_teks(x) 
    ]) 
    tentor_pilih = st.sidebar.multiselect( 
        "Tentor:", 
        vals, 
        default=vals 
    ) 
    if tentor_pilih: 
        df_filter = df_filter[ 
            df_filter[aliases["tentor"]].isin(tentor_pilih) 
        ] 
 
# ============================================================ 
# KOLOM NILAI 
# ============================================================ 
 
def total_col(key): 
    col = aliases.get(key) 
    if col and col in df_filter.columns: 
        return float(df_filter[col].sum()) 
    return 0.0 
 
total_biaya = total_col("biaya_les") 
total_bayar = total_col("sudah_dibayar") 
total_piutang = total_col("sisa_pembayaran") 
total_fee = total_col("total_fee_tentor") 
total_fee_dibayar = total_col("fee_dibayar") 
total_fee_kurang = total_col("kekurangan_fee") 
 
# ============================================================ 
# JUMLAH TRANSAKSI 
# ============================================================ 
# Jumlah transaksi dihitung dari BARIS yang memiliki BIAYA LES > 0. 
# Jadi baris kosong / BIAYA LES = 0 tidak ikut dihitung sebagai transaksi. 
if aliases.get("biaya_les") and aliases["biaya_les"] in df_filter.columns: 
    jumlah_transaksi = int( 
        (pd.to_numeric( 
            df_filter[aliases["biaya_les"]], 
            errors="coerce" 
        ) > 0).sum() 
    ) 
else: 
    jumlah_transaksi = 0 
 
# ============================================================ 
# KPI UTAMA 
# ============================================================ 
 
st.markdown('<div class="section-title">📌 Ringkasan Utama</div>', unsafe_allow_html=True) 
 
k1, k2, k3, k4 = st.columns(4) 
k1.metric("TOTAL TAGIHAN / BIAYA LES", rupiah(total_biaya)) 
k2.metric("TOTAL SUDAH DIBAYAR", rupiah(total_bayar)) 
k3.metric("TOTAL PIUTANG SISWA", rupiah(total_piutang)) 
k4.metric( 
    "JUMLAH TRANSAKSI", 
    f"{jumlah_transaksi:,}".replace(",", ".") 
) 
 
k5, k6, k7, k8 = st.columns(4) 
k5.metric("TOTAL FEE TENTOR", rupiah(total_fee)) 
k6.metric("FEE SUDAH DIBAYAR", rupiah(total_fee_dibayar)) 
k7.metric("KEKURANGAN FEE TENTOR", rupiah(total_fee_kurang)) 
k8.metric( 
    "JUMLAH SISWA", 
    f"{df_filter[aliases['nama_siswa']].nunique():,}".replace(",", ".") 
    if aliases.get("nama_siswa") else "0" 
) 
 
# ============================================================ 
# STATUS KLIEN & PEMBAYARAN 
# ============================================================ 
 
st.markdown('<div class="section-title">👥 Status Klien / Siswa</div>', unsafe_allow_html=True) 
 
c1, c2 = st.columns(2) 
 
if aliases.get("status_klien") and aliases["status_klien"] in df_filter.columns: 
    status_df = ( 
        df_filter[aliases["status_klien"]] 
        .replace("", np.nan) 
        .dropna() 
        .value_counts() 
        .reset_index() 
    ) 
    status_df.columns = ["Status Klien", "Jumlah"] 
 
    with c1: 
        fig = px.pie( 
            status_df, 
            names="Status Klien", 
            values="Jumlah", 
            hole=0.45, 
            title="Distribusi Klien Baru vs Repeat Order" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
    # Nilai berdasarkan status klien 
    tmp = df_filter.copy() 
    tmp["_nilai"] = ( 
        tmp[aliases["biaya_les"]] 
        if aliases.get("biaya_les") 
        else 0 
    ) 
 
    omset_status = ( 
        tmp.groupby(aliases["status_klien"], dropna=False)["_nilai"] 
        .sum() 
        .reset_index() 
    ) 
    omset_status.columns = ["Status Klien", "Total Biaya Les"] 
 
    with c2: 
        fig = px.bar( 
            omset_status, 
            x="Status Klien", 
            y="Total Biaya Les", 
            text_auto=".3s", 
            title="Total Biaya Les berdasarkan Status Klien" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
else: 
    st.info("Kolom status klien tidak tersedia pada sheet ini.") 
 
# ============================================================ 
# STATUS PEMBAYARAN 
# ============================================================ 
 
st.markdown('<div class="section-title">💳 Status Pembayaran</div>', unsafe_allow_html=True) 
 
c1, c2 = st.columns(2) 
 
if aliases.get("status_pembayaran") and aliases["status_pembayaran"] in df_filter.columns: 
    pay_status = ( 
        df_filter[aliases["status_pembayaran"]] 
        .replace("", np.nan) 
        .dropna() 
        .value_counts() 
        .reset_index() 
    ) 
    pay_status.columns = ["Status Pembayaran", "Jumlah"] 
 
    with c1: 
        fig = px.bar( 
            pay_status, 
            x="Status Pembayaran", 
            y="Jumlah", 
            text_auto=True, 
            title="Jumlah berdasarkan Status Pembayaran" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
    with c2: 
        if aliases.get("sisa_pembayaran"): 
            tmp = df_filter.copy() 
            tmp["_piutang"] = tmp[aliases["sisa_pembayaran"]] 
            pay_value = ( 
                tmp.groupby(aliases["status_pembayaran"])["_piutang"] 
                .sum() 
                .reset_index() 
            ) 
            pay_value.columns = ["Status Pembayaran", "Piutang"] 
 
            fig = px.bar( 
                pay_value, 
                x="Status Pembayaran", 
                y="Piutang", 
                text_auto=".3s", 
                title="Piutang berdasarkan Status Pembayaran" 
            ) 
            st.plotly_chart(fig, use_container_width=True) 
 
# ============================================================ 
# TREN BULANAN 
# ============================================================ 
 
st.markdown('<div class="section-title">📈 Perkembangan Keuangan per Bulan</div>', unsafe_allow_html=True) 
 
if aliases.get("tanggal") and aliases["tanggal"] in df_filter.columns: 
    trend = df_filter.dropna(subset=[aliases["tanggal"]]).copy() 
    trend["Periode"] = trend[aliases["tanggal"]].dt.to_period("M").astype(str) 
 
    agg_dict = {} 
    if aliases.get("biaya_les"): 
        agg_dict["Tagihan"] = (aliases["biaya_les"], "sum") 
    if aliases.get("sudah_dibayar"): 
        agg_dict["Sudah Dibayar"] = (aliases["sudah_dibayar"], "sum") 
    if aliases.get("sisa_pembayaran"): 
        agg_dict["Piutang"] = (aliases["sisa_pembayaran"], "sum") 
    if aliases.get("total_fee_tentor"): 
        agg_dict["Fee Tentor"] = (aliases["total_fee_tentor"], "sum") 
 
    if agg_dict: 
        monthly = trend.groupby("Periode").agg(**agg_dict).reset_index() 
 
        long_monthly = monthly.melt( 
            id_vars="Periode", 
            var_name="Jenis", 
            value_name="Nilai" 
        ) 
 
        fig = px.bar( 
            long_monthly, 
            x="Periode", 
            y="Nilai", 
            color="Jenis", 
            barmode="group", 
            title="Tagihan, Pembayaran, Piutang, dan Fee Tentor" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
# ============================================================ 
# METODE PEMBAYARAN 
# ============================================================ 
 
st.markdown('<div class="section-title">🏦 Metode Pembayaran</div>', unsafe_allow_html=True) 
 
if aliases.get("metode") and aliases["metode"] in df_filter.columns: 
    method = ( 
        df_filter.groupby(aliases["metode"], dropna=False) 
        .agg( 
            Jumlah_Transaksi=(aliases["metode"], "size"), 
            Total_Dibayar=( 
                aliases["sudah_dibayar"], 
                "sum" 
            ) if aliases.get("sudah_dibayar") else 
            (aliases["metode"], "size") 
        ) 
        .reset_index() 
    ) 
 
    method = method.rename(columns={aliases["metode"]: "Metode Pembayaran"}) 
 
    c1, c2 = st.columns(2) 
 
    with c1: 
        fig = px.pie( 
            method, 
            names="Metode Pembayaran", 
            values="Jumlah_Transaksi", 
            hole=0.4, 
            title="Distribusi Metode Pembayaran" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
    with c2: 
        fig = px.bar( 
            method, 
            x="Metode Pembayaran", 
            y="Total_Dibayar", 
            text_auto=".3s", 
            title="Total Pembayaran berdasarkan Metode" 
        ) 
        st.plotly_chart(fig, use_container_width=True) 
 
# ============================================================ 
# FEE TENTOR 
# ============================================================ 
 
st.markdown('<div class="section-title">👨‍🏫 Analisis Fee Tentor</div>', unsafe_allow_html=True) 
 
if aliases.get("tentor") and aliases["tentor"] in df_filter.columns: 
    fee_group = df_filter.copy() 
 
    fee_group["Tentor_View"] = fee_group[aliases["tentor"]].replace( 
        "", "Belum Diisi" 
    ) 
 
    agg = { 
        "Jumlah Project": ("Tentor_View", "size") 
    } 
 
    if aliases.get("total_fee_tentor"): 
        agg["Total Fee"] = (aliases["total_fee_tentor"], "sum") 
 
    if aliases.get("fee_dibayar"): 
        agg["Sudah Dibayar"] = (aliases["fee_dibayar"], "sum") 
 
    if aliases.get("kekurangan_fee"): 
        agg["Kekurangan Fee"] = (aliases["kekurangan_fee"], "sum") 
 
    if aliases.get("nama_siswa"): 
        agg["Jumlah Siswa"] = (aliases["nama_siswa"], "nunique") 
 
    fee_tentor = ( 
        fee_group.groupby("Tentor_View", dropna=False) 
        .agg(**agg) 
        .reset_index() 
        .sort_values( 
            "Kekurangan Fee" if "Kekurangan Fee" in agg else "Total Fee", 
            ascending=False 
        ) 
    ) 
 
    c1, c2 = st.columns(2) 
 
    with c1: 
        plot_col = "Total Fee" if "Total Fee" in fee_tentor.columns else "Jumlah Baris" 
        fig = px.bar( 
            fee_tentor.head(15), 
            x="Tentor_View", 
            y=plot_col, 
            text_auto=".3s", 
            title="Total Fee Tentor" 
        ) 
        fig.update_layout(xaxis_title="Tentor", yaxis_title=plot_col) 
        st.plotly_chart(fig, use_container_width=True) 
 
    with c2: 
        plot_col = "Kekurangan Fee" if "Kekurangan Fee" in fee_tentor.columns else "Sudah Dibayar" 
        fig = px.bar( 
            fee_tentor.head(15), 
            x="Tentor_View", 
            y=plot_col, 
            text_auto=".3s", 
            title="Kekurangan Fee Tentor" 
        ) 
        fig.update_layout(xaxis_title="Tentor", yaxis_title=plot_col) 
        st.plotly_chart(fig, use_container_width=True) 
 
    fee_view = fee_tentor.copy() 
 
    for col in ["Total Fee", "Sudah Dibayar", "Kekurangan Fee"]: 
        if col in fee_view.columns: 
            fee_view[col] = fee_view[col].apply(rupiah) 
 
    fee_view.columns = [ 
        "Tentor" if c == "Tentor_View" else c 
        for c in fee_view.columns 
    ] 
 
    st.dataframe( 
        fee_view, 
        use_container_width=True, 
        hide_index=True 
    ) 
 
else: 
    st.info("Kolom tentor tidak ditemukan.") 
 
# ============================================================ 
# PIUTANG PER SISWA 
# ============================================================ 
 
st.markdown('<div class="section-title">💸 Piutang Siswa</div>', unsafe_allow_html=True) 
 
if aliases.get("nama_siswa") and aliases.get("sisa_pembayaran"): 
    piutang = ( 
        df_filter.groupby(aliases["nama_siswa"], dropna=False) 
        .agg( 
            Total_Tagihan=(aliases["biaya_les"], "sum"), 
            Sudah_Dibayar=(aliases["sudah_dibayar"], "sum"), 
            Piutang=(aliases["sisa_pembayaran"], "sum") 
        ) 
        .reset_index() 
        .rename(columns={aliases["nama_siswa"]: "Nama Siswa"}) 
    ) 
 
    piutang = piutang[piutang["Piutang"] > 0].sort_values( 
        "Piutang", 
        ascending=False 
    ) 
 
    piutang_view = piutang.copy() 
    for col in ["Total_Tagihan", "Sudah_Dibayar", "Piutang"]: 
        piutang_view[col] = piutang_view[col].apply(rupiah) 
 
    piutang_view.columns = [ 
        "Nama Siswa", 
        "Total Tagihan", 
        "Sudah Dibayar", 
        "Piutang" 
    ] 
 
    if not piutang_view.empty: 
        st.dataframe( 
            piutang_view, 
            use_container_width=True, 
            hide_index=True 
        ) 
    else: 
        st.success("Tidak ada piutang pada filter yang dipilih.") 
 
# ============================================================ 
# STATUS SISWA DETAIL (Lanjutan) 
# ============================================================ 
 
st.markdown('<div class="section-title">📋 Detail Status Siswa</div>', unsafe_allow_html=True) 
 
if aliases.get("nama_siswa"): 
    group_cols = [aliases["nama_siswa"]] 
    agg = {} 
 
    if aliases.get("status_klien"): 
        agg["Status Klien"] = (aliases["status_klien"], "first") 
    if aliases.get("biaya_les"): 
        agg["Total Tagihan"] = (aliases["biaya_les"], "sum") 
    if aliases.get("sudah_dibayar"): 
        agg["Sudah Dibayar"] = (aliases["sudah_dibayar"], "sum") 
    if aliases.get("sisa_pembayaran"): 
        agg["Sisa Pembayaran"] = (aliases["sisa_pembayaran"], "sum") 
 
    if agg: 
        detail_siswa = df_filter.groupby(group_cols).agg(**agg).reset_index() 
        detail_siswa = detail_siswa.rename(columns={aliases["nama_siswa"]: "Nama Siswa"}) 
         
        # Format nilai mata uang 
        for col in ["Total Tagihan", "Sudah Dibayar", "Sisa Pembayaran"]: 
            if col in detail_siswa.columns: 
                detail_siswa[col] = detail_siswa[col].apply(rupiah) 
 
        st.dataframe( 
            detail_siswa, 
            use_container_width=True, 
            hide_index=True 
        ) 
 
# ============================================================ 
# SEMUA KOLOM ASLI 
# ============================================================ 
 
st.markdown('<div class="section-title">🗂️ Semua Kolom Sheet LAPORAN</div>', unsafe_allow_html=True) 
 
st.caption( 
    "Bagian ini sengaja menampilkan seluruh kolom yang terbaca dari sheet " 
    "LAPORAN sehingga tidak ada informasi transaksi yang hilang." 
) 
 
# Tampilkan kolom asli + kolom turunan secara horizontal 
display_df = df_filter.copy() 
 
# Format hanya untuk tampilan, tidak mengubah data asli 
display_view = display_df.copy() 
 
currency_keywords = [ 
    "BIAYA LES", 
    "SUDAH DIBAYAR", 
    "SISA PEMBAYARAN", 
    "TOTAL FEE", 
    "KEKURANGAN FEE" 
] 
 
for col in display_view.columns: 
    if any(key_teks(k) in key_teks(col) for k in currency_keywords): 
        display_view[col] = display_view[col].apply( 
            lambda x: rupiah(x) if pd.notna(x) else "" 
        ) 
 
st.dataframe( 
    display_view, 
    use_container_width=True, 
    hide_index=True, 
    height=500 
) 
 
# ============================================================ 
# INFORMASI STRUKTUR DATA 
# ============================================================ 
 
with st.expander("🔎 Informasi struktur data"): 
    info = pd.DataFrame({ 
        "Nama Kolom": df.columns, 
        "Tipe Data": [str(df[c].dtype) for c in df.columns], 
        "Jumlah Terisi": [int(df[c].notna().sum()) for c in df.columns], 
        "Jumlah Kosong": [int(df[c].isna().sum()) for c in df.columns], 
        "Jumlah Unik": [int(df[c].nunique(dropna=True)) for c in df.columns] 
    }) 
 
    st.dataframe( 
        info, 
        use_container_width=True, 
        hide_index=True 
    ) 
 
# ============================================================ 
# DOWNLOAD 
# ============================================================ 
 
st.markdown('<div class="section-title">⬇️ Export Data</div>', unsafe_allow_html=True) 
 
csv_data = df_filter.to_csv(index=False).encode("utf-8-sig") 
 
st.download_button( 
    "📥 Download Data Bersih CSV", 
    data=csv_data, 
    file_name="LAPORAN_BIMBEL_2026_BERSIH.csv", 
    mime="text/csv" 
)