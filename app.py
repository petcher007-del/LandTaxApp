import streamlit as st
import datetime
import pandas as pd
import base64

# --- 1. ตั้งค่าหน้าเว็บ (Page Config) ---
st.set_page_config(
    page_title="ระบบประเมินราคาที่ดินและสิ่งปลูกสร้าง",
    page_icon="🏡",
    layout="wide"
)

# ==========================================
# 🎨 ฟังก์ชันสำหรับใส่ภาพพื้นหลัง (Background)
# ==========================================
def add_bg_from_local(image_file):
    try:
        with open(image_file, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/{"png"};base64,{encoded_string.decode()});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        /* ปรับพื้นหลังของกล่องข้อความให้เป็นสีขาวโปร่งแสง เพื่อให้อ่านง่ายขึ้น */
        .stMetric, .css-1d391kg, .stTextInput, .stNumberInput, .stSelectbox {{
            background-color: rgba(255, 255, 255, 0.85) !important;
            border-radius: 10px;
            padding: 5px;
        }}
        /* ปรับสีตัวหนังสือหัวข้อให้เข้มขึ้นสู้กับ Background */
        h1, h2, h3 {{
            color: #1a1a1a !important;
            text-shadow: 2px 2px 4px rgba(255,255,255,0.8);
        }}
        </style>
        """,
        unsafe_allow_html=True
        )
    except FileNotFoundError:
        # กรณีหาไฟล์รูปไม่เจอ จะไม่แสดง error แต่จะใช้พื้นหลังปกติ
        st.warning(f"⚠️ ไม่พบไฟล์รูปภาพชื่อ {image_file} ในโฟลเดอร์ กรุณานำรูปมาวางเพื่อแสดงพื้นหลัง")

# >>>>> เรียกใช้ฟังก์ชันใส่พื้นหลังตรงนี้ <<<<<
# ตรวจสอบว่าคุณมีไฟล์ชื่อ background.jpg ในโฟลเดอร์หรือไม่
add_bg_from_local('background.jpg') 


# --- ฟังก์ชันคำนวณ (Logic เดิม) ---
def calculate_depreciation(build_type, age):
    if age < 1: age = 1
    dep_percent = 0
    if build_type == 'ตึก (Concrete)':
        if age <= 10: dep_percent = age * 1
        else: dep_percent = 10 + (age - 10) * 2
        if dep_percent > 76: dep_percent = 76
    elif build_type == 'ครึ่งตึกครึ่งไม้ (Half)':
        if age <= 5: dep_percent = age * 2
        elif age <= 15: dep_percent = 10 + (age - 5) * 4
        else: dep_percent = 10 + 40 + (age - 15) * 5
        if dep_percent > 85: dep_percent = 85
    elif build_type == 'ไม้ (Wood)':
        if age <= 5: dep_percent = age * 3
        elif age <= 15: dep_percent = 15 + (age - 5) * 5
        else: dep_percent = 15 + 50 + (age - 15) * 7
        if dep_percent > 93: dep_percent = 93
    return dep_percent

# ==========================================
# ส่วนการนำทาง (Sidebar)
# ==========================================
# สร้างพื้นหลังสีขาวให้ Sidebar อ่านง่าย
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background-color: rgba(255, 255, 255, 0.95);
}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("เมนูหลัก")
page = st.sidebar.radio("เลือกหน้าที่ต้องการไป:", 
    ["🏠 หน้าหลัก", "🧮 เครื่องมือคำนวณราคา"]
)
st.sidebar.markdown("---")
st.sidebar.info("ระบบช่วยประเมินราคาเบื้องต้น อ้างอิงเกณฑ์ปี 2535")

# ==========================================
# PAGE 1: หน้าหลัก
# ==========================================
if page == "🏠 หน้าหลัก":
    # สร้างกล่องขาวรองรับข้อความ เพื่อให้อ่านง่ายบนพื้นหลัง
    with st.container():
        st.markdown('<div style="background-color: rgba(255,255,255,0.9); padding: 30px; border-radius: 15px;">', unsafe_allow_html=True)
        
        st.title("🏠 ระบบประเมินราคาที่ดินและสิ่งปลูกสร้าง")
        st.subheader("ยินดีต้อนรับ")
        st.write("""
        โปรแกรมนี้ช่วยประมาณการมูลค่าทรัพย์สินตามหลักเกณฑ์กรมธนารักษ์ (พ.ศ. 2535)
        โดยใช้ตารางค่าเสื่อมราคาแบบขั้นบันได
        """)
        st.info("👈 กรุณาเลือกเมนู 'เครื่องมือคำนวณราคา' ทางด้านซ้ายเพื่อเริ่มใช้งาน")
        
        st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# PAGE 2: เครื่องมือคำนวณ
# ==========================================
elif page == "🧮 เครื่องมือคำนวณราคา":
    # สร้างกล่องขาวรองรับเนื้อหาทั้งหมด
    st.markdown('<div style="background-color: rgba(255,255,255,0.9); padding: 20px; border-radius: 15px; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.title("🧮 เครื่องมือคำนวณราคาประเมิน")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # สร้าง Tabs
    tab1, tab2, tab3 = st.tabs(["1. ข้อมูลที่ดิน 🌳", "2. ข้อมูลสิ่งปลูกสร้าง 🏠", "3. สรุปผล 📊"])

    # --- TAB 1 ---
    with tab1:
        st.markdown('<div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
        st.header("ข้อมูลแปลงที่ดิน")
        col1, col2, col3 = st.columns(3)
        with col1: land_rai = st.number_input("ไร่", min_value=0, value=0)
        with col2: land_ngan = st.number_input("งาน", min_value=0, value=0)
        with col3: land_wah = st.number_input("ตารางวา", min_value=0.0, value=17.0, step=0.1)

        total_wah_calc = (land_rai * 400) + (land_ngan * 100) + land_wah
        st.info(f"📍 รวมเนื้อที่ทั้งหมด: **{total_wah_calc:,.1f}** ตารางวา")
        
        land_price_per_wah = st.number_input("ราคาประเมินต่อตารางวา (บาท)", min_value=0.0, value=24000.0, step=500.0)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2 ---
    with tab2:
        st.markdown('<div style="background-color: rgba(255,255,255,0.8); padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
        st.header("ข้อมูลโรงเรือน")
        build_type = st.selectbox("ประเภทสิ่งปลูกสร้าง", ['ตึก (Concrete)', 'ครึ่งตึกครึ่งไม้ (Half)', 'ไม้ (Wood)'])
        current_year_sys = datetime.datetime.now().year + 543
        col_b1, col_b2 = st.columns(2)
        with col_b1: build_year_th = st.number_input("ปีที่สร้างเสร็จ (พ.ศ.)", min_value=2450, max_value=current_year_sys, value=2553)
        with col_b2: calc_year_th = st.number_input("ปีที่ประเมินภาษี (พ.ศ.)", min_value=2500, value=2565)
        col_b3, col_b4 = st.columns(2)
        with col_b3: build_area = st.number_input("พื้นที่ใช้สอย (ตร.ม.)", min_value=0.0, value=120.0)
        with col_b4: build_price_sqm = st.number_input("ราคาประเมินกลาง (บาท/ตร.ม.)", min_value=0.0, value=10400.0)
        st.markdown('</div>', unsafe_allow_html=True)

    # Calculation
    total_land_price = total_wah_calc * land_price_per_wah
    age = calc_year_th - build_year_th
    dep_percent = calculate_depreciation(build_type, age)
    full_build_price = build_area * build_price_sqm
    dep_amount = full_build_price * (dep_percent / 100)
    net_build_price = full_build_price - dep_amount
    grand_total = total_land_price + net_build_price

    # --- TAB 3 ---
    with tab3:
        st.markdown('<div style="background-color: rgba(255,255,255,0.95); padding: 20px; border-radius: 10px;">', unsafe_allow_html=True)
        st.header("บทสรุปการประเมิน")
        st.markdown(f"""<div style="background-color: #d4edda; padding: 20px; border-radius: 15px; text-align: center; border: 2px solid #c3e6cb;"><h3 style="margin:0; color: #155724;">มูลค่าทรัพย์สินรวมทั้งสิ้น</h3><h1 style="margin:10px 0; color: #155724; font-size: 42px;">{grand_total:,.2f} บาท</h1></div><br>""", unsafe_allow_html=True)

        chart_data = pd.DataFrame({'รายการ': ['ที่ดิน', 'สิ่งปลูกสร้าง (สุทธิ)'], 'มูลค่า (บาท)': [total_land_price, net_build_price]})
        st.bar_chart(chart_data, x='รายการ', y='มูลค่า (บาท)', color=["#FF9800"])

        st.markdown("### 📄 รายละเอียดการคำนวณ")
        summary_data = {
            "รายการ": ["1. มูลค่าที่ดิน", "2. สิ่งปลูกสร้าง (ตั้งต้น)", "3. หักค่าเสื่อมราคา", "4. สิ่งปลูกสร้าง (สุทธิ)"],
            "รายละเอียด": [f"{total_wah_calc:,.1f} ตร.ว. x {land_price_per_wah:,.0f} บ.", f"{build_area:,.0f} ตร.ม. x {build_price_sqm:,.0f} บ.", f"หัก {dep_percent}% (อายุ {age} ปี)", "มูลค่าหลังหักค่าเสื่อม"],
            "จำนวนเงิน (บาท)": [total_land_price, full_build_price, -dep_amount, net_build_price]
        }
        df = pd.DataFrame(summary_data)
        st.table(df)
        st.markdown('</div>', unsafe_allow_html=True)
