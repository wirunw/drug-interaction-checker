import streamlit as st
import pandas as pd

# --- 1. โหลดและเตรียมข้อมูล ---
# ใช้ @st.cache_data เพื่อให้โหลดข้อมูลแค่ครั้งเดียว
@st.cache_data
def load_data():
    df = pd.read_csv("drug_interactions_pharmacological_groups.csv")
    return df

df = load_data()

# --- 2. สร้างหน้าตาของแอป ---
st.title("💊 ระบบตรวจสอบการตีกันของยา (Drug Interaction Checker)")

# -- Dropdown 1: เลือกกลุ่มยา --
# สร้าง list ของกลุ่มยาที่ไม่ซ้ำกัน และเรียงตามตัวอักษร
all_groups = sorted(df['drug1_group'].dropna().unique())
selected_group = st.selectbox("ขั้นตอนที่ 1: เลือกกลุ่มยา", options=[""] + all_groups, format_func=lambda x: "กรุณาเลือก..." if x == "" else x)

# -- Dropdown 2: เลือกยาตัวที่ 1 --
if selected_group:
    # กรองยาในกลุ่มที่เลือก
    drugs_in_group = sorted(df[df['drug1_group'] == selected_group]['drug1'].unique())
    selected_drug1 = st.selectbox("ขั้นตอนที่ 2: เลือกยาตัวที่ 1", options=[""] + drugs_in_group, format_func=lambda x: "กรุณาเลือก..." if x == "" else x)

    # -- Dropdown 3: เลือกยาตัวที่ 2 --
    if selected_drug1:
        # กรองยาตัวที่ 2 ที่มี Interaction กับยาตัวที่ 1
        interacting_drugs = sorted(df[df['drug1'] == selected_drug1]['drug2'].unique())
        selected_drug2 = st.selectbox("ขั้นตอนที่ 3: เลือกยาตัวที่ 2 ที่ต้องการตรวจสอบ", options=[""] + interacting_drugs, format_func=lambda x: "กรุณาเลือก..." if x == "" else x)

        # -- 3. แสดงผลลัพธ์ --
        if selected_drug1 and selected_drug2:
            st.markdown("---")
            st.subheader("ผลการตรวจสอบ:")
            
            result = df[(df['drug1'] == selected_drug1) & (df['drug2'] == selected_drug2)]
            
            if not result.empty:
                st.success("พบข้อมูลปฏิกิริยาระหว่างยา!")
                interaction = result.iloc[0]
                st.markdown(f"**ผลกระทบ:** {interaction['interaction_effect']}")
                st.markdown(f"**ระดับความรุนแรง:** {interaction['severity']}")
                st.markdown(f"**การจัดการ:** {interaction['management']}")
            else:
                # กรณีนี้ไม่น่าเกิดขึ้นได้ เพราะเรากรองตัวเลือกแล้ว
                st.info("ไม่พบข้อมูลปฏิกิริยาระหว่างยา 2 ชนิดนี้")