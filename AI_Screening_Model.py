import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import openai
import os  # For secure API key handling

# ✅ Load OpenAI API Key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# ✅ Load the trained AI model
model = joblib.load("final_ai_selection_model.pkl")

# ✅ Load VA Selection & Annual Survey Data
@st.cache_data
def load_data():
    va_data = pd.read_csv("final_va_selection_results.csv")
    annual_data = pd.read_csv("final_annual_survey_results.csv")
    return va_data, annual_data

va_df, annual_df = load_data()

# ✅ Streamlit App Title
st.title("🚀 AI-Based Business Selection Tool")

# ✅ Sidebar: Upload CSV or Enter Manually
st.sidebar.header("Upload CSV or Enter Details")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📊 **Uploaded Data Preview:**")
    st.dataframe(df)
else:
    st.write("✍️ **Manual Entry (if no CSV uploaded)**")
    value_prop = st.number_input("Value Proposition Score (1-5)", min_value=1, max_value=5, value=3)
    market_potential = st.number_input("Market & Growth Potential Score (1-5)", min_value=1, max_value=5, value=3)
    team_expertise = st.number_input("Team & Expertise Score (1-5)", min_value=1, max_value=5, value=3)

    df = pd.DataFrame({
        "Value_Proposition_Score": [value_prop],
        "Market_Growth_Potential_Score": [market_potential],
        "Team_Expertise_Score": [team_expertise]
    })

# ✅ Predict Selection Status
if st.button("Predict Selection Status"):
    if df is not None:
        predictions = model.predict(df)
        df["Predicted_Selection_Status"] = ["Accepted" if pred == 1 else "Rejected" for pred in predictions]

        # ✅ Show results
        st.write("📌 **Predictions:**")
        st.dataframe(df)

        # ✅ Download option
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Results as CSV",
            data=csv,
            file_name="AI_Selection_Results.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Please upload a CSV file or enter details manually.")

# ✅ DATA INSIGHTS SECTION
st.header("📊 Data Insights: VA Selection & Annual Survey")

# ✅ Show dataset previews
st.subheader("VA Selection Dataset Overview")
st.dataframe(va_df.head())

st.subheader("Annual Survey Dataset Overview")
st.dataframe(annual_df.head())

# ✅ Visualize Selection Outcomes
st.subheader("🔍 Selection Status Breakdown")
fig_status, ax_status = plt.subplots()
sns.countplot(data=va_df, x="Final_AI_Selection_Status", palette="coolwarm", ax=ax_status)
ax_status.set_title("Distribution of AI Selection Status")
st.pyplot(fig_status)

# ✅ Visualize Industry Influence on Selection
st.subheader("🌍 Industry-Wise Selection Breakdown")
industry_counts = va_df["Industry"].value_counts().nlargest(10)
fig_industry, ax_industry = plt.subplots()
sns.barplot(x=industry_counts.values, y=industry_counts.index, palette="viridis", ax=ax_industry)
ax_industry.set_xlabel("Number of Businesses")
ax_industry.set_ylabel("Industry")
ax_industry.set_title("Top 10 Industries in VA Selection")
st.pyplot(fig_industry)

# ✅ NLP TEXT ANALYSIS: Business Descriptions & Selection Patterns
st.header("📝 AI-Based Analysis of Business Descriptions")

# ✅ Generate WordClouds
def generate_wordcloud(data, title):
    text = " ".join(data.dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)

    # Unique variable names for each figure
    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    plt.title(title, fontsize=14)
    st.pyplot(fig_wc)

# ✅ WordCloud for Accepted Businesses
st.subheader("📌 Key Words in Accepted Business Applications")
accepted_desc = va_df[va_df["Final_AI_Selection_Status"] == "Accepted"]["Business/Project description"]
generate_wordcloud(accepted_desc, "Most Frequent Words in Accepted Businesses")

# ✅ WordCloud for Rejected Businesses
st.subheader("📌 Key Words in Rejected Business Applications")
rejected_desc = va_df[va_df["Final_AI_Selection_Status"] == "Rejected"]["Business/Project description"]
generate_wordcloud(rejected_desc, "Most Frequent Words in Rejected Businesses")

# ✅ AI CHATBOT: Business Selection Insights
st.header("💬 Ask the AI Assistant")
st.write("🤖 **Ask about business selection trends, predictors, or insights!**")

# ✅ Predefined sample questions
sample_questions = [
    "What factors most influence selection in healthcare startups?",
    "Which industries have the highest acceptance rates?",
    "How has the selection criteria changed over the last 3 years?",
    "What are the most commonly used words in accepted business applications?",
    "What is the likelihood of success for a business in the fashion industry?",
    "What characteristics most often lead to rejection?",
    "Show a trend analysis of businesses selected by VA over the last 5 years."
]

# ✅ Dropdown for sample questions
selected_question = st.selectbox("🔍 Choose a sample question or type your own:", [""] + sample_questions)

# ✅ User input box for custom questions
user_query = st.text_input("💡 Type your question here and press Enter:", value=selected_question if selected_question else "")

# ✅ OpenAI-Powered AI Assistant (Compatible with OpenAI `0.28.0`)
def get_ai_response(query):
    """Use OpenAI's updated API format to generate business insights."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Using GPT-3.5 for better speed and affordability
            messages=[
                {"role": "system", "content": "You are an AI assistant trained to analyze business selection trends based on VA Selection and Annual Survey data."},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ✅ Show AI response if user enters a question
if user_query:
    response = get_ai_response(user_query)
    st.write("💡 **AI Assistant:**", response)

# ✅ Footer
st.markdown("---")
st.markdown("🔍 **Built with AI | Powered by Streamlit**")

