# 🚀 AI Loan Affordability Microservice

> **A full-stack, AI-powered financial fiduciary built with FastAPI, Streamlit, Machine Learning, and Google Gemini.**

Most loan calculators just spit out a monthly payment number and leave the user to figure out the rest. I built this microservice to solve that problem by combining traditional financial math with predictive machine learning and generative AI. 

Instead of a basic calculator, this application acts as a strict, personalized financial advisor—calculating risk, predicting safe limits, and explicitly advising users against loans that could cause financial distress.

## ✨ Why I Built This (The Core Features)
* **Hybrid Intelligence:** Uses a custom Scikit-Learn model to predict the user's "maximum safe EMI" based on their income, credit score, and existing debt. 
* **Fiduciary AI:** Integrates Google's `gemini-2.5-flash` model using strict prompt engineering. If the ML model flags a loan as "HIGH RISK," Gemini is instructed to reject the loan and offer actionable alternatives.
* **Enterprise Architecture:** Structured as a modular REST API. It uses Pydantic for strict data validation and SQLAlchemy 2.0 to securely log applications into a persistent SQLite database.
* **Decoupled Frontend:** A lightweight Streamlit UI that communicates asynchronously with the FastAPI backend.

## 🛠️ Tech Stack
* **Backend:** FastAPI, Python 3.x
* **Frontend:** Streamlit
* **Database & ORM:** SQLite, SQLAlchemy 2.0
* **Machine Learning:** Scikit-Learn, Pandas, Joblib
* **Generative AI:** Google GenAI SDK (`gemini-2.5-flash`)
* **Validation & Security:** Pydantic, python-dotenv

## ⚙️ Architecture Breakdown
I designed this project with scalability and clean code principles in mind. The logic is strictly separated:
* `main.py` - The FastAPI traffic controller and routing logic.
* `services.py` - Isolated mathematical business logic (EMI calculations, risk evaluation).
* `schemas.py` - Pydantic models acting as the data bouncer for incoming API requests.
* `models.py` & `database.py` - SQLAlchemy database mapping and session management.

## 🚀 How to Run It Locally

**1. Clone the repository**
git clone https://github.com/YOUR_USERNAME/ai-loan-affordability-microservice.git
cd ai-loan-affordability-microservice

**2. Set up the virtual environment**
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt

**3. Configure your Environment Variables**
Create a `.env` file in the root directory and add your Google Gemini API key:
GEMINI_API_KEY=your_api_key_here
*(Note: Do not use quotes around the key. See `.env.example` for reference.)*

**4. Start the FastAPI Backend**
cd app
uvicorn main:app --reload
*The API will be live at http://127.0.0.1:8000. You can view the interactive Swagger UI docs at http://127.0.0.1:8000/docs.*

**5. Start the Streamlit Frontend**
Open a second terminal window, activate your environment, and run:
cd app
streamlit run frontend.py

## 📈 Next Steps & Roadmap
* Containerizing the application using Docker for easier deployment.
* Expanding the ML model to account for macroeconomic factors (like inflation rates).
* Migrating from SQLite to PostgreSQL for production readiness.
