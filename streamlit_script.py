import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import openai
import os
from dotenv import load_dotenv  # ✅ Import dotenv

# ✅ Load environment variables from .env file
load_dotenv()

# ✅ Load OpenAI API Key securely from environment variable
from dotenv import load_dotenv

# ✅ Load environment variables manually
load_dotenv()

import openai
import os  # For secure API key handling

# ✅ Now fetch API key from .env
from dotenv import load_dotenv

# ✅ Load environment variables manually
load_dotenv()

import openai
import os  # For secure API key handling

# ✅ Now fetch API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

# Debugging: Print to confirm API key is being loaded (Remove after testing)
print("Loaded API Key:", openai.api_key)

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
st.title("🚀 Quintessence AI: Business Selection Tool")

# ✅ Sidebar: Upload CSV or Enter Manually
st.sidebar.header("Upload CSV or Enter Details")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("📊 **Uploaded Data Preview:**")
    st.dataframe(df)
else:
    st.write("✍️ **Manual Entry (if no CSV uploaded)**")

    # ✅ Value Proposition Inputs
    st.subheader("📌 Value Proposition")
    sector = st.selectbox("Select Business Sector", [
        "Healthcare_and_Allied_services", "ICT_and_digital_serivces",
        "Financial,_professional,_and_management_", "Agriculture,_Agroforestry,_Crops_and_Horticulture",
        "Processed_Food", "Fashion,_apparel_and_crafts", "Accommodation,_food_and_beverage_service",
        "Wholesale_and_retail", "Construction_and_building_services", "Tranportation_and_travel",
        "Enterpreneurship_skills", "electric__auto__equipment__che", "Soft_and_employability_skill",
        "Mining,_quarry_and_utilities", "Public_Administration,_community_and_soc", "other"
    ])

    # ✅ Market & Growth Potential Inputs
    st.subheader("📌 Market & Growth Potential")
    revenue = st.number_input("Annual Revenue", min_value=0, value=10000)
    jobs = st.number_input("Number of Employees", min_value=0, value=5)
    investment = st.number_input("Investment Received", min_value=0, value=1000)
    clients = st.number_input("Number of Clients", min_value=0, value=100)
    rural_producers = st.number_input("Number of Rural Producers Supported", min_value=0, value=0)

    # ✅ Team & Expertise Inputs
    st.subheader("📌 Team & Expertise")
    education = st.selectbox("Highest Level of Education", ["PhD", "Masters", "Bachelors", "Highschool", "No Formal Education"])
    age = st.number_input("Age of Founder", min_value=18, max_value=100, value=35)
    gender = st.selectbox("Gender of Founder", ["Male", "Female", "Other"])

    # ✅ Compute Scores Based on Inputs
    def score_value_proposition(sector):
        sector_scores = {
            "Healthcare_and_Allied_services": 5, "ICT_and_digital_serivces": 5,
            "Financial,_professional,_and_management_": 5, "Agriculture,_Agroforestry,_Crops_and_Horticulture": 5,
            "Processed_Food": 4, "Fashion,_apparel_and_crafts": 3, "Accommodation,_food_and_beverage_service": 3,
            "Wholesale_and_retail": 2, "Construction_and_building_services": 3, "Tranportation_and_travel": 3,
            "Enterpreneurship_skills": 3, "electric__auto__equipment__che": 4, "Soft_and_employability_skill": 3,
            "Mining,_quarry_and_utilities": 2, "Public_Administration,_community_and_soc": 2, "other": 2
        }
        return sector_scores.get(sector, 2)

    def score_revenue(value):
        return 1.5 if value > 500000 else 1 if 100000 <= value <= 500000 else 0.5

    def score_jobs(value):
        return 1.0 if value > 8 else 0.75 if value >= 4 else 0.5

    def score_investment(value):
        return 1 if value > 50000 else 0.75 if 10000 <= value <= 50000 else 0.5

    def score_clients(value):
        return 1.0 if value > 5000 else 0.75 if value >= 401 else 0.5 if value >= 51 else 0.25

    def score_rural_producers(value):
        return 1.0 if value > 50 else 0.75 if value >= 6 else 0.5 if value >= 1 else 0.25

    def score_education(value):
        education_map = {"PhD": 1.75, "Masters": 1.75, "Bachelors": 1.75, "Highschool": 1.25, "No Formal Education": 0.75}
        return education_map.get(value, 0.75)

    def score_age(value):
        return 1.5 if value < 35 else 1.0 if value <= 50 else 0.5

    def score_gender(value):
        return 1.0 if value == "Female" else 0.5

    # ✅ Compute Factor Scores
    value_prop_score = score_value_proposition(sector)
    market_potential_score = (score_revenue(revenue) + score_jobs(jobs) +
                              score_investment(investment) + score_clients(clients) + score_rural_producers(rural_producers))
    team_expertise_score = (score_education(education) + score_age(age) + score_gender(gender))

    # ✅ Compute Final Score
    final_score = (value_prop_score * 0.25) + (market_potential_score * 0.25) + (team_expertise_score * 0.50)
    final_score_percentage = ((final_score - 1) / 4) * 100
    selection_status = "Accepted" if final_score_percentage >= 50 else "Rejected"

    # ✅ Display Results
    if st.button("Predict Selection Status"):
        st.write("📌 **Predictions:**")
        st.write(f"🏆 **Final Score:** {final_score:.2f} ({final_score_percentage:.2f}%)")
        st.write(f"✅ **Selection Status:** {selection_status}")

# ✅ NLP TEXT ANALYSIS: Business Descriptions & Selection Patterns
st.header("📝 AI-Based Analysis of Business Descriptions")

# ✅ Generate WordClouds
def generate_wordcloud(data, title):
    text = " ".join(data.dropna().astype(str))
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(text)
    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wordcloud, interpolation="bilinear")
    ax_wc.axis("off")
    plt.title(title, fontsize=14)
    st.pyplot(fig_wc)

# ✅ AI CHATBOT: Business Selection Insights
st.header("💬 Ask the AI Assistant")
st.write("🤖 **Ask about business selection trends, predictors, or insights!**")

sample_questions = [
    "What factors most influence selection in healthcare startups?",
    "Which industries have the highest acceptance rates?",
    "How has the selection criteria changed over the last 3 years?"
]

selected_question = st.selectbox("🔍 Choose a sample question or type your own:", [""] + sample_questions)
user_query = st.text_input("💡 Type your question here and press Enter:", value=selected_question if selected_question else "")

def get_ai_response(query):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI analyzing business selection data."},
                      {"role": "user", "content": query}],
            temperature=0.7,
            max_tokens=300
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ Error: {str(e)}"

if user_query:
    response = get_ai_response(user_query)
    st.write("💡 **AI Assistant:**", response)

st.markdown("---")
st.markdown("🔍 **Built with AI | Powered by Streamlit**")