Quintessence AI: Business Selection Tool 🚀

Overview

Quintessence AI is a Streamlit-based business selection tool designed to help evaluate businesses based on various factors such as market potential, investment received, and revenue.

Features

📂Upload CSV or Enter Manually: Users can either upload a dataset or manually enter business details.

📈Real-time Business Scoring: The app automatically calculates scores based on weighted criteria.

📊Data-Driven Selection: Uses a weighted scoring system to assess business eligibility.

✨Deployed on Streamlit Cloud: Accessible via a public link.

Live App 🌍

[Launch Quintessence AI](https://quintessence-ai-2025.streamlit.app/)

Project Setup

🔢 1. Clone the Repository

git clone https://github.com/Ambs1947/Atomcamp.git
cd Atomcamp

🔄 2. Create a Virtual Environment (Recommended)

python -m venv venv
source venv/bin/activate   # For macOS/Linux
venv\Scripts\activate    # For Windows

🔧 3. Install Dependencies

pip install -r requirements.txt

🔐 4. Set Up OpenAI API Key

Create a .env file in the project root directory.

Add the following line, replacing your-api-key-here with your actual OpenAI API key:

OPENAI_API_KEY=your-api-key-here

🔄 5. Run the Streamlit App

streamlit run streamlit_script.py

Repository Structure

Atomcamp/
│── streamlit_script.py    # Main Streamlit app script
│── requirements.txt       # Dependencies
│── final_ai_selection_model.pkl  # Pre-trained AI model
│── final_va_selection_results.csv  # Dataset
│── final_annual_survey_results.csv  # Dataset
│── README.md              # Project Documentation
│── venv/                  # Virtual environment (not included in repo)

Technologies Used

Python

Streamlit

Pandas

OpenAI API

Git & GitHub

Contributors

Ambareen Baig (GitHub: Ambs1947)

License

This project is licensed under the MIT License.

Contact

For any issues or improvements, open an issue on GitHub or contact me via GitHub Discussions.

