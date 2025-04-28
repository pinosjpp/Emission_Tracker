# 🚗 Emission Tracker Dashboard

This is a Streamlit web application that visualizes vehicle registration data across U.S. states and analyzes real-world CO2 emissions and fuel efficiency metrics by vehicle type over time.

---

## 📊 Features

- 📍 Interactive **Choropleth map** of vehicle registrations across U.S. states (1900–2020)
- 👉 Toggle individual vehicle types (Auto, Bus, Truck, Motorcycle)
- ❌ Option to exclude California (outlier control)
- 📈 Line charts for registrations and emissions trends
- 🖐️ Compare CO2, MPG, weight, horsepower, and more across vehicle classes
- 🔊 Talk to an AI emissions expert chatbot

---

## 🛠 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/pinosjpp/Emission_Tracker.git
cd Emission_Tracker
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, here are the main dependencies:
```bash
pip install streamlit pandas plotly altair numpy openai
```

### 3. OpenAI Key Setup (for ChatBot Functionality)
To enable the AI Chatbot feature:
- Obtain an OpenAI API Key from [https://platform.openai.com/account/api-keys](https://platform.openai.com/account/api-keys).
- Create a folder named `.streamlit` in your project root if it doesn't exist.
- Inside `.streamlit/`, create a file called `secrets.toml`.
- Add your key like this:
```toml
OPENAI_API_KEY = "your-openai-api-key-here"
```

Make sure not to commit your `secrets.toml` file to GitHub (it's listed in `.gitignore`).

### 4. Run the App
```bash
streamlit run Home.py
```

---

## 📁 File Structure

```plaintext
🗖️ Emission_Tracker
├── Home.py                     # App landing page
├── pages/
│   ├── Co2_Emssions.py         # CO2 Emissions dashboard
│   ├── Manufacture.py          # Manufacture tab
│   ├── Registrations.py        # Vehicle Registration dashboard
│   └── ChatWithAI.py           # Talk to AI emissions expert
├── data/
│   ├── Data_by_Vehicle.csv
│   └── Motor_Vehicle_Registrations_Dashboard_data.csv
├── Motor.ipynb                 # (Optional) Jupyter analysis
├── .streamlit/
│   └── secrets.toml            # (local only, not pushed)
├── requirements.txt
└── README.md
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Link your repo and select `Home.py` as the main file
4. Add your OpenAI key to the app **Secrets** through the Streamlit Cloud settings
5. Click **Deploy**

---

## 📩 Contact

Maintained by [@pinosjpp](https://github.com/pinosjpp)  
Feel free to open issues or suggestions!

