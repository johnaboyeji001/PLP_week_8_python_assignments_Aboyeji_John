import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
import re

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("metadata.csv")
    df = df.dropna(subset=["title", "abstract"])
    df["publish_time"] = pd.to_datetime(df["publish_time"], errors="coerce")
    df["year"] = df["publish_time"].dt.year
    return df

df = load_data()

# App title
st.title("📖 CORD-19 Research Metadata Explorer")
st.write("Explore COVID-19 research trends, journals, and insights.")

# Sidebar filters
year_filter = st.sidebar.slider("Select Year", int(df["year"].min()), int(df["year"].max()), int(df["year"].min()))

filtered_df = df[df["year"] == year_filter]

# Show dataset sample
st.subheader("Sample of Data")
st.write(filtered_df.head())

# Publications over time
st.subheader("Number of Publications per Year")
papers_per_year = df["year"].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(8,5))
sns.lineplot(x=papers_per_year.index, y=papers_per_year.values, marker="o", ax=ax)
ax.set_title("Publications per Year")
st.pyplot(fig)

# Top journals
st.subheader("Top Journals")
top_journals = df["journal"].value_counts().head(10)

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x=top_journals.values, y=top_journals.index, ax=ax)
ax.set_title("Top Journals")
st.pyplot(fig)

# Word frequency
st.subheader("Most Frequent Words in Titles")
all_words = " ".join(df["title"].dropna()).lower()
words = re.findall(r"\\b[a-z]{4,}\\b", all_words)
word_freq = Counter(words).most_common(15)
word_df = pd.DataFrame(word_freq, columns=["word", "count"])

fig, ax = plt.subplots(figsize=(8,5))
sns.barplot(x="count", y="word", data=word_df, ax=ax)
ax.set_title("Frequent Words in Titles")
st.pyplot(fig)
