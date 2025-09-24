import streamlit as st
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import numpy as np

# Load Data
df = pd.read_csv("CARS.csv")

# Data Cleaning
df = df.fillna(0)
df.MSRP = df.MSRP.replace('[$,]', '', regex=True).astype('int64')
df.Invoice = df.Invoice.replace('[$,]', '', regex=True).astype('int64')
df = df.drop('Length', axis=1)
df = df.rename(columns={'Model': 'Model_Type'})

st.title("Car Data Explorer 🚗")

# Show dataset
if st.checkbox("Show Raw Data"):
    st.write(df)

# Dropdown for Make selection
make_choice = st.selectbox("Select Make Type", df.Make.unique())
filtered_make = df[df.Make == make_choice]

# Dropdown for Type selection
type_choice = st.selectbox("Select Car Type", filtered_make.Type.unique())
filtered_type = filtered_make[filtered_make.Type == type_choice]

# Barplot
fig, ax = plt.subplots()
sb.barplot(x=filtered_type.Model_Type, y=filtered_type.MPG_City, ax=ax)
plt.xticks(rotation=90)
st.pyplot(fig)

# Pie chart for Type distribution
st.subheader("Distribution of Car Types")
type_counts = df.Type.value_counts()

fig2, ax2 = plt.subplots()
ax2.pie(type_counts.values, labels=type_counts.index, autopct='%d%%')
st.pyplot(fig2)

# KDE Plot for Weight
st.subheader("KDE Plot of Car Weight")
fig3, ax3 = plt.subplots()
sb.kdeplot(df.Weight, ax=ax3)
st.pyplot(fig3)
