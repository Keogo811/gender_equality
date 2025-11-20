import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Gender Equality Report - Preview version", layout="wide")
st.title("📊 Gender Equality Project - PREVIEW VERSION 1.7")

# Data loading
@st.cache_data
def load_data():
    pro = pd.read_csv("cleaned_data/cleaned_professional_data.csv")
    salary = pd.read_csv("cleaned_data/cleaned_salary_data.csv") 
    employee = pd.read_csv("cleaned_data/cleaned_employee_data.csv")
    return employee.merge(pro, on="id_salarié").merge(salary, on="id_salarié")

df = load_data()

# Executive summary
st.header("📋 Executive Summary")
col1, col2, col3, col4 = st.columns(4)

with col1:
    salary_gap = ((df[df['Sexe']=='H']['Salaire base mensuel'].mean() - 
                   df[df['Sexe']=='F']['Salaire base mensuel'].mean()) / 
                  df[df['Sexe']=='H']['Salaire base mensuel'].mean()) * 100
    st.metric("Average Gender Pay Gap", f"{salary_gap:.1f}%")

with col2:
    promo_gap = (df[df['Sexe']=='H']['Promotion'].mean() - 
                 df[df['Sexe']=='F']['Promotion'].mean()) * 100
    st.metric("Promotion Gap", f"{promo_gap:.1f}%")

with col3:
    satisfaction_h = df[df['Sexe']=='H']['Niveau de satisfaction'].mean()
    satisfaction_f = df[df['Sexe']=='F']['Niveau de satisfaction'].mean()
    st.metric("Satisfaction", f"{satisfaction_f:.0f}/100 F", f"{satisfaction_h:.0f}/100 H")

with col4:
    count_h = len(df[df['Sexe']=='H'])
    count_f = len(df[df['Sexe']=='F'])
    total = len(df)
    st.metric("Workforce", f"{count_f}F / {count_h}H", f"Total: {total}")

# 3 main charts with description and interpretation sections
tab1, tab2, tab3 = st.tabs(["💰 Salaries", "🚀 Promotions", "👥 Distribution"])

with tab1:
    st.subheader("Salary Distribution by Gender")
    
    # CHART DESCRIPTION - TO BE FILLED LATER
    st.write("📝 **Chart Description:** *[Describe what this chart shows about salary distribution between genders]*")
    
    fig1 = px.box(df, x='Sexe', y='Salaire base mensuel', 
                  title="Salary Distribution by Gender")
    st.plotly_chart(fig1, use_container_width=True)
    
    # INTERPRETATION - TO BE FILLED LATER
    st.write("💡 **Interpretation:** *[Add your analysis and conclusions about salary equity here]*")

with tab2:
    st.subheader("Promotion Rate by Department")
    
    # CHART DESCRIPTION - TO BE FILLED LATER
    st.write("📝 **Chart Description:** *[Describe promotion patterns across departments and genders]*")
    
    promo_data = df.groupby(['Service', 'Sexe'])['Promotion'].mean().reset_index()
    fig2 = px.bar(promo_data, x='Service', y='Promotion', color='Sexe',
                  title="Promotion Rate by Department", barmode='group')
    st.plotly_chart(fig2, use_container_width=True)
    
    # INTERPRETATION - TO BE FILLED LATER
    st.write("💡 **Interpretation:** *[Add your analysis of promotion equity and departmental biases here]*")

with tab3:
    st.subheader("Gender Distribution by Department")
    
    # CHART DESCRIPTION - TO BE FILLED LATER
    st.write("📝 **Chart Description:** *[Describe gender representation across different departments]*")
    
    service_gender = df.groupby(['Service', 'Sexe']).size().reset_index(name='Count')
    fig3 = px.bar(service_gender, x='Service', y='Count', color='Sexe',
                  title="Gender Distribution by Department", barmode='stack')
    st.plotly_chart(fig3, use_container_width=True)
    
    # INTERPRETATION - TO BE FILLED LATER
    st.write("💡 **Interpretation:** *[Add your analysis of gender segregation and representation patterns here]*")

# Project information and GitHub link
st.markdown("---")
st.info("🔜 Full version under development in PowerBI")

# PERMANENT GITHUB LINK - TO BE UPDATED LATER
st.markdown(
    """
    **Project Repository:** [https://github.com/your-username/gender-equality-project](https://github.com/your-username/gender-equality-project)
    """,
    unsafe_allow_html=True
)