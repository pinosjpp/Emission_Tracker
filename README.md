# 🚗 Emission Tracker Dashboard

This is a Streamlit web application that visualizes vehicle registration data across U.S. states and analyzes real-world CO2 emissions and fuel efficiency metrics by vehicle type over time.

---

## 📊 Features

- 📍 Interactive **Choropleth map** of vehicle registrations across U.S. states (1900–2020)
- �� Toggle individual vehicle types (Auto, Bus, Truck, Motorcycle)
- ❌ Option to exclude California (outlier control)
- 📈 Line charts for registrations and emissions trends
- 🖐️ Compare CO2, MPG, weight, horsepower, and more across vehicle classes

---

## 🛠 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/pinosjpp/Emission_Tracker.git
cd Emission_Tracker
```

### 2. (Optional but recommended) Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate   # Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, here are the main dependencies:
```bash
pip install streamlit pandas plotly altair numpy
```

### 4. Run the App
```bash
streamlit run Home.py
```

---

## 📁 File Structure

```plaintext
📆 Emission_Tracker
├── Home.py                     # App landing page
├── pages/
│   ├── Co2_Emssions.py         # CO2 Emissions dashboard
│   └── Registrations.py        # Vehicle Registration dashboard
├── data/
│   ├── Data_by_Vehicle.csv
│   └── Motor_Vehicle_Registrations_Dashboard_data.csv
├── Motor.ipynb                 # (Optional) Jupyter analysis
└── README.md
```

---

## 🌐 Deploy on Streamlit Cloud

1. Push this repo to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Link your repo and select `Home.py` as the main file
4. Click **Deploy**

---

## 📩 Contact

Maintained by [@pinosjpp](https://github.com/pinosjpp)  
Feel free to open issues or suggestions!

