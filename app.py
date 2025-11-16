import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="Route Optimization", page_icon="🚚", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv('data/survey_data.csv')

df = load_data()
df['Interested'] = df['Interest_Level'].apply(lambda x: 'Yes' if x >= 4 else 'No')

st.title("🚚 Route Optimization SaaS - Market Analysis")
st.markdown("---")

total = len(df)
interested = len(df[df['Interest_Level'] >= 4])
avg_budget = df['Willingness_to_Pay'].mean()
nps = ((len(df[df['NPS_Score'] >= 9]) - len(df[df['NPS_Score'] <= 6])) / total) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("Respondents", "{:,}".format(total))
col2.metric("Interested", "{}".format(interested))
col3.metric("Avg Budget", "Rs{:,.0f}".format(avg_budget))
col4.metric("NPS", "{:.1f}".format(nps))

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["Overview", "Budget", "Charts"])

with tab1:
    st.header("Market Overview")
    fig, ax = plt.subplots(figsize=(10, 6))
    df['Interest_Level'].value_counts().sort_index().plot(kind='bar', ax=ax, color='#3498db')
    ax.set_title('Interest Distribution', fontsize=14, fontweight='bold')
    ax.set_xlabel('Interest Level')
    st.pyplot(fig)
    plt.close()

with tab2:
    st.header("Budget Analysis")
    st.subheader("Average: Rs{:,.0f}/vehicle/month".format(avg_budget))
    fig, ax = plt.subplots(figsize=(12, 6))
    df.boxplot(column='Willingness_to_Pay', by='Company_Size', ax=ax)
    plt.suptitle('')
    st.pyplot(fig)
    plt.close()

with tab3:
    st.header("Visualizations")
    viz_files = sorted(Path('visualizations').glob('*.png'))
    if viz_files:
        for viz in viz_files:
            st.image(str(viz), use_column_width=True)

st.sidebar.title("Stats")
st.sidebar.metric("Total", "{:,}".format(len(df)))
st.sidebar.metric("Interested %", "{:.1f}%".format(interested/total*100))
st.sidebar.info("Interactive dashboard for market analysis")
