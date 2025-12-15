import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Gender Equality Analysis", layout="wide")

# En-tête du projet
st.title("Gender Equality Dashboard")
st.markdown("---")
st.markdown("**Project Description:** *[We are a programming society who have for mission to create a comprehensive gender equality analysis in the staff members of a compagny.*")
st.markdown("*We examine compensation, promotion, and representation disparities within the organization. The research aims to identify systemic biases across departments, experience levels, and demographic factors to provide data-driven insights for developing and following guidelines about equitable workplace practices and policies.]*")
st.markdown("")
st.markdown("**Methodology:** *[The analysis leverages three integrated datasets covering professional information, compensation details, and employee demographics.*")
st.markdown("*Analytical approaches include comparative statistics, trend analysis across career stages, departmental segmentation, and intersectional examination of gender with factors like parenthood, age, and contract type. Visualization techniques highlight key disparities and progression patterns.]*")
st.markdown("")
st.markdown("---")
st.markdown("*For complete analysis of the data, please go see the interactive excel file:*")
st.markdown("**Excel analysis:** [https://aivancity-my.sharepoint.com/:x:/g/personal/shauryaman_singh_aivancity_education/IQDhbZkiJbV5RaFYffYcB9aaAVaoZDvXeU6mgmi3YS_wpUM](https://aivancity-my.sharepoint.com/:x:/g/personal/shauryaman_singh_aivancity_education/IQDhbZkiJbV5RaFYffYcB9aaAVaoZDvXeU6mgmi3YS_wpUM)")
st.markdown("---") 

# Data loading
@st.cache_data
def load_data():
    pro = pd.read_csv("cleaned_data/cleaned_professional_data.csv")
    salary = pd.read_csv("cleaned_data/cleaned_salary_data.csv") 
    employee = pd.read_csv("cleaned_data/cleaned_employee_data.csv")
    df = employee.merge(pro, on="id_salarié").merge(salary, on="id_salarié")
    
    # Create calculated fields
    df['Age'] = 2024 - pd.to_datetime(df['Date_naissance']).dt.year
    df['Seniority_Bracket'] = pd.cut(df['Ancienneté_an'], 
                                   bins=[0, 3, 7, 15, 100], 
                                   labels=['0-3 years', '4-7 years', '8-15 years', '15+ years'])
    df['Salary_Quartile'] = pd.qcut(df['Salaire base mensuel'], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
    df['Hourly_Rate'] = df['Salaire base mensuel'] / df['Durée hebdo']
    
    return df

df = load_data()

# Key Metrics
st.header("Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    salary_gap = ((df[df['Sexe']=='H']['Salaire base mensuel'].mean() - 
                   df[df['Sexe']=='F']['Salaire base mensuel'].mean()) / 
                  df[df['Sexe']=='H']['Salaire base mensuel'].mean()) * 100
    st.metric("Average Gender Pay Gap", f"{salary_gap:.1f}%")

with col2:
    promo_rate_h = df[df['Sexe']=='H']['Promotion'].mean() * 100
    promo_rate_f = df[df['Sexe']=='F']['Promotion'].mean() * 100
    promo_gap = promo_rate_h - promo_rate_f
    st.metric("Average Promotion Gap", f"{promo_gap:.1f}%", "Men higher")

with col3:
    count_h = len(df[df['Sexe']=='H'])
    count_f = len(df[df['Sexe']=='F'])
    st.metric("Workforce", f"{count_f} Women", f"{count_h} Men")

with col4:
    cdi_count = len(df[df['Contrat']=='CDI'])
    cdd_count = len(df[df['Contrat']=='CDD'])
    st.metric("Contract Types", f"{cdi_count} CDI", f"{cdd_count} CDD")

st.markdown("---")

# Analysis Sections
st.header("Detailed Analysis")

# 1. Pay Gap by Department and Seniority
st.subheader("1. Pay Gap by Department and Experience")
pay_gap_data = df.groupby(['Service', 'Seniority_Bracket', 'Sexe'])['Salaire base mensuel'].mean().unstack()
pay_gap_data['Gap_Percentage'] = ((pay_gap_data['H'] - pay_gap_data['F']) / pay_gap_data['H']) * 100
pay_gap_data = pay_gap_data.reset_index()

fig1 = px.bar(pay_gap_data, x='Service', y='Gap_Percentage', color='Seniority_Bracket',
             title="Salary Gap Percentage by Department and Seniority Level")
st.plotly_chart(fig1, use_container_width=True)

st.write(f"**Interpretation:** This analysis shows pay gaps ranging from {pay_gap_data['Gap_Percentage'].min():.1f}% to {pay_gap_data['Gap_Percentage'].max():.1f}% across departments in specific seniority bracket. Positive values indicate men earn more, negative values indicate women earn more. We can see there is high salary gap in favor men and women depending on the department, this might indicates a department-specific bias rather than organization-wide bias.")

st.markdown("---")

# 2. Glass Ceiling Analysis
st.subheader("2. Access to Leadership Positions")
leadership_depts = ['Consultant', 'Commercial', 'R&D']
leadership_data = df[df['Service'].isin(leadership_depts)]
leadership_gender = leadership_data['Sexe'].value_counts()
women_leadership_pct = leadership_gender.get('F', 0) / len(leadership_data) * 100

fig2 = px.pie(leadership_gender, values=leadership_gender.values, names=leadership_gender.index,
             title="Gender Distribution in Strategic Departments")
st.plotly_chart(fig2, use_container_width=True)
st.write(f"**Interpretation:** Women represent {women_leadership_pct:.1f}% of employees in key strategic departments, indicating a small advantage to men to access influential positions. HOWEVER, considering a higher number of men in the enterprise's staff than women, 131 men to 125 women, making the distribution not relevent to interpret a bias.")

st.markdown("---")

# 3. Promotion Equity Over Time
st.subheader("3. Career Progression Patterns")
promo_data = df.groupby(['Seniority_Bracket', 'Sexe'])['Promotion'].mean().reset_index()

fig3 = px.line(promo_data, x='Seniority_Bracket', y='Promotion', color='Sexe',
              title="Promotion Rates by Career Stage",
              color_discrete_map={'H': 'blue', 'F': 'red'})
st.plotly_chart(fig3, use_container_width=True)

st.write(f"**Interpretation:** The promotion gap peaks between around 0-8 years of seniority, men are more likely to get promoted the first year around 12% than women, but women are after favored around 30% at their peak to get promoted at their fourth year of seniority. This suggests a favoritism bias of promotion for women for medium range seniority. We can also remark a lower gap rate of promotions between the two genders for the oldest workers, signaling also a decrease of promotions.")

st.markdown("---")

# 4. Motherhood Penalty Analysis
st.subheader("4. Parenthood Impact on Careers")
parent_data = df.groupby(['Enfants', 'Sexe'])['Salaire base mensuel'].mean().reset_index()

fig4 = px.line(parent_data, x='Enfants', y='Salaire base mensuel', color='Sexe',
              title="Salary Progression by Number of Children",
              color_discrete_map={'H': 'blue', 'F': 'red'})
st.plotly_chart(fig4, use_container_width=True)

# Compute impact of parentality
women_no_kids = parent_data[(parent_data['Sexe']=='F') & (parent_data['Enfants']==0)]['Salaire base mensuel'].mean()
women_with_kids = parent_data[(parent_data['Sexe']=='F') & (parent_data['Enfants']>=1)]['Salaire base mensuel'].mean()
men_no_kids = parent_data[(parent_data['Sexe']=='H') & (parent_data['Enfants']==0)]['Salaire base mensuel'].mean()
men_with_kids = parent_data[(parent_data['Sexe']=='H') & (parent_data['Enfants']>=1)]['Salaire base mensuel'].mean()

motherhood_penalty = ((women_with_kids - women_no_kids) / women_no_kids) * 100
fatherhood_bonus = ((men_with_kids - men_no_kids) / men_no_kids) * 100

st.write(f"**Interpretation:** We have a clear 'motherhood penalty' observed - women's salaries change by {motherhood_penalty:+.1f}% after having children, while men experience a 'fatherhood bonus' of {fatherhood_bonus:+.1f}%. Parenthood is rewarded differently by gender. Women who have one or two children have a strong salarial gap to men which demonstrate an illegal discrimination to be corrected.")

st.markdown("---")

# 5. Departmental Segregation
st.subheader("5. Occupational Segregation Patterns")
dept_composition = df.groupby('Service')['Sexe'].value_counts(normalize=True).unstack().fillna(0) * 100
dept_composition = dept_composition.reset_index()

fig5 = px.bar(dept_composition, x='Service', y=['F', 'H'],
             title="Gender Concentration by Department (%)",
             barmode='stack',
             color_discrete_map={'H': 'blue', 'F': 'red'})
st.plotly_chart(fig5, use_container_width=True)

# Identification of department gender bias
most_female_dept = dept_composition.loc[dept_composition['F'].idxmax()]
most_male_dept = dept_composition.loc[dept_composition['H'].idxmax()]
st.write(f"**Interpretation:** Commercial and RH departments are mostly equal, but for Compta Finances is {most_female_dept['F']:.1f}% female-dominated while Consult, Makerting and R&D, the most male-dominated is {most_male_dept['H']:.1f}%. This might involve a bias preference towards men, but national records show that few womens are disponible on the R&D department.")

st.markdown("---")

# 6. Variable Pay Bias
st.subheader("6. Bonus and Variable Pay Distribution")
variable_data = df.groupby(['Service', 'Sexe'])['%variable_moyen'].mean().reset_index()

fig6 = px.bar(variable_data, x='Service', y='%variable_moyen', color='Sexe',
             title="Average Variable Pay by Department and Gender",
             barmode='group',
             color_discrete_map={'H': 'blue', 'F': 'red'})
st.plotly_chart(fig6, use_container_width=True)

# Finding biggest bonus pay gap
variable_pivot = variable_data.pivot(index='Service', columns='Sexe', values='%variable_moyen')
variable_pivot['Gap'] = variable_pivot['H'] - variable_pivot['F']
max_bonus_gap = variable_pivot['Gap'].max()
st.write(f"**Interpretation:** Men receive higher variable compensation on Compta Finances, Marketing and R&D, particularly in Commercial department where the gap reaches {max_bonus_gap:.1f}%. But on Consultant and RH deparment, the average variable pay advantage women. This suggests a complex and unexpected disparity in the entreprise's workers, in performance evaluation and bonus allocation processes, where women are not victim of clear discrimination depending on department variable.")

st.markdown("---")

# 7. Salary Distribution Analysis
st.subheader("7. Overall Salary Distribution")

# Create a cleaner histogram
fig7 = px.histogram(df, x='Salaire base mensuel', color='Sexe',
                   title='Salary Distribution by Gender',
                   labels={'Salaire base mensuel': 'Monthly Salary (€)', 'Sexe': 'Gender'},
                   barmode='overlay',  # Overlap the bars for direct comparison
                   opacity=0.7)        # Make bars slightly transparent for better visualisation

# Add median lines for clarity
male_median = df[df['Sexe']=='H']['Salaire base mensuel'].median()
female_median = df[df['Sexe']=='F']['Salaire base mensuel'].median()

fig7.add_vline(x=male_median, line_dash='dash', line_color='blue', annotation_text=f'Men Median: {male_median:.0f}€')
fig7.add_vline(x=female_median, line_dash='dash', line_color='red', annotation_text=f'Women Median: {female_median:.0f}€')

st.plotly_chart(fig7, use_container_width=True)

# Simple interpretation
distribution_gap = ((male_median - female_median) / male_median) * 100
st.write(f'**Interpretation:** Men have a higher median salary ({male_median:.0f}€) than women ({female_median:.0f}€), a gap of {distribution_gap:.1f}%. The overlapping bars show a salary gap around 500€ between men and women.')

st.markdown('---')

# 8. Work-Life Balance Impact
st.subheader("8. Part-Time Work and Compensation")
part_time_data = df[df['Durée hebdo'] < 35]

hourly_data = part_time_data.groupby('Sexe')['Hourly_Rate'].mean().reset_index()
fig8 = px.bar(hourly_data, x='Sexe', y='Hourly_Rate',
                title='Average Hourly Rate for Part-Time Workers',
                labels={'Hourly_Rate': 'Hourly Rate (€)', 'Sexe': 'Gender'},
                color='Sexe',
                barmode='group')
st.plotly_chart(fig8, use_container_width=True)
st.write(f'**Interpretation:** Estimation of average hourly money generated by part-time worker genre.We have a small advantage for women for around 3€, no bias can be proven.')

st.markdown("---")

# 9. Satisfaction vs Compensation 
st.subheader("9. Employee Satisfaction Analysis")
fig9 = px.scatter(df, x='Salaire base mensuel', y='Niveau de satisfaction', color='Sexe',
                 title="Salary vs Satisfaction by Gender",
                 color_discrete_map={'H': 'blue', 'F': 'red'},
                 trendline="ols")  # Add Ordinary Least Squares trendline
st.plotly_chart(fig9, use_container_width=True)

st.write(f"**Interpretation:** Each point represent a worker with his level of satisfaction and genre. We can see no correlation from the graph, there is no trend.")

st.markdown("---")

# 10. Age and Gender Intersectionality
st.subheader("10. Career Trajectories by Age and Gender")
age_brackets = pd.cut(df['Age'], bins=[20, 35, 45, 55, 65], labels=['20-35', '36-45', '46-55', '56-65'])
age_salary_data = df.groupby([age_brackets, 'Sexe'])['Salaire base mensuel'].mean().reset_index()

fig10 = px.line(age_salary_data, x='Age', y='Salaire base mensuel', color='Sexe',
               title="Salary Progression by Age Group",
               color_discrete_map={'H': 'blue', 'F': 'red'})
st.plotly_chart(fig10, use_container_width=True)

st.write(f"**Interpretation:** We can analyze a early salary gap around 600€ in favour of women in early age for 20-30 year olds, then around 200€ in favour of men for middle aged workers 32-40 year olds, then a second major salary gap in favour of women happen around 42-54 for an average of 400€. But after an alarming decrease of salary level is showed for both genres to the most aged workers, it demonstrates a clear seniority discrimination.")


# Footer
st.markdown("---")
st.markdown("Project Repository: [https://github.com/Keogo811/gender_equality](https://github.com/Keogo811/gender_equality)")