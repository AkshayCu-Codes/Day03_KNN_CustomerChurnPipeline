import streamlit as st
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------
# PAGE CONFIGURATION
# -----------------------------------------------
st.set_page_config(page_title="Churn Prediction Dashboard", layout="wide", page_icon="📊")

st.title("📊 Customer Churn Prediction Dashboard")
st.write("This dashboard predicts churn using an API, stores every prediction, and provides analytics on saved records.")


# -----------------------------------------------
# FILE & DATA MANAGEMENT
# -----------------------------------------------
PREDICTION_FILE = "../data/predictions.csv"

# Create file if not exists
if not os.path.exists("../data"):
    os.makedirs("../data")

if not os.path.exists(PREDICTION_FILE):
    pd.DataFrame(columns=[
        "gender","SeniorCitizen","Partner","Dependents","tenure","PhoneService","MultipleLines",
        "InternetService","OnlineSecurity","OnlineBackup","DeviceProtection","TechSupport",
        "StreamingTV","StreamingMovies","Contract","PaperlessBilling","PaymentMethod",
        "MonthlyCharges","TotalCharges","Prediction"
    ]).to_csv(PREDICTION_FILE, index=False)

# Load predictions
pred_df = pd.read_csv(PREDICTION_FILE)


# -----------------------------------------------
# INPUT MAPPINGS
# -----------------------------------------------
gender_map = {"Male": 1, "Female": 0}
yes_no_map = {"Yes": 1, "No": 0}
internet_map = {"No Internet": 0, "DSL": 1, "Fiber Optic": 2}
service_map = {"Not Available": 0, "Yes": 1, "No": 2}
contract_map = {"Month-to-Month": 0, "One Year": 1, "Two Year": 2}
payment_map = {"Electronic Check": 0, "Mailed Check": 1, "Bank Transfer": 2, "Credit Card": 3}


# -----------------------------------------------
# SIDEBAR FORM
# -----------------------------------------------
st.sidebar.header("Enter Customer Details")

gender = gender_map[st.sidebar.selectbox("Gender", list(gender_map.keys()))]
SeniorCitizen = yes_no_map[st.sidebar.selectbox("Senior Citizen?", list(yes_no_map.keys()))]
Partner = yes_no_map[st.sidebar.selectbox("Has Partner?", list(yes_no_map.keys()))]
Dependents = yes_no_map[st.sidebar.selectbox("Has Dependents?", list(yes_no_map.keys()))]
tenure = st.sidebar.slider("Tenure (Months)", 0, 72)
PhoneService = yes_no_map[st.sidebar.selectbox("Phone Service?", list(yes_no_map.keys()))]
MultipleLines = yes_no_map[st.sidebar.selectbox("Multiple Phone Lines?", list(yes_no_map.keys()))]
InternetService = internet_map[st.sidebar.selectbox("Internet Type", list(internet_map.keys()))]
OnlineSecurity = service_map[st.sidebar.selectbox("Online Security", list(service_map.keys()))]
OnlineBackup = service_map[st.sidebar.selectbox("Online Backup", list(service_map.keys()))]
DeviceProtection = service_map[st.sidebar.selectbox("Device Protection", list(service_map.keys()))]
TechSupport = service_map[st.sidebar.selectbox("Tech Support", list(service_map.keys()))]
StreamingTV = service_map[st.sidebar.selectbox("Streaming TV", list(service_map.keys()))]
StreamingMovies = service_map[st.sidebar.selectbox("Streaming Movies", list(service_map.keys()))]
Contract = contract_map[st.sidebar.selectbox("Contract Type", list(contract_map.keys()))]
PaperlessBilling = yes_no_map[st.sidebar.selectbox("Paperless Billing?", list(yes_no_map.keys()))]
PaymentMethod = payment_map[st.sidebar.selectbox("Payment Method", list(payment_map.keys()))]
MonthlyCharges = st.sidebar.number_input("Monthly Charges (€)", 0.00, 500.00)
TotalCharges = st.sidebar.number_input("Total Charges (€)", 0.00, 10000.00)

payload = {
    "gender": gender, "SeniorCitizen": SeniorCitizen, "Partner": Partner, "Dependents": Dependents,
    "tenure": tenure, "PhoneService": PhoneService, "MultipleLines": MultipleLines, "InternetService": InternetService,
    "OnlineSecurity": OnlineSecurity, "OnlineBackup": OnlineBackup, "DeviceProtection": DeviceProtection,
    "TechSupport": TechSupport, "StreamingTV": StreamingTV, "StreamingMovies": StreamingMovies, "Contract": Contract,
    "PaperlessBilling": PaperlessBilling, "PaymentMethod": PaymentMethod, "MonthlyCharges": MonthlyCharges,
    "TotalCharges": TotalCharges
}


# -----------------------------------------------
# PREDICTION HANDLING
# -----------------------------------------------
if st.button("Predict"):
    try:
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        result = response.json()["message"]

        # Show result
        if "Leave" in result:
            st.error(f"❌ {result}")
            prediction = 1
        else:
            st.success(f"✅ {result}")
            prediction = 0

        # Save prediction
        payload["Prediction"] = prediction
        new_df = pd.DataFrame([payload])
        pred_df = pd.concat([pred_df, new_df], ignore_index=True)
        pred_df.to_csv(PREDICTION_FILE, index=False)
        st.info("📁 Prediction saved to history.")

    except:
        st.error("🚨 Could not reach API. Run: uvicorn api.app:app --reload")


# -----------------------------------------------
# HISTORY & DELETION MANAGEMENT
# -----------------------------------------------
st.subheader("📁 Prediction History")
st.dataframe(pred_df)

remove_option = st.radio("Delete Records:", ["None", "Delete One", "Delete Multiple", "Delete All"])

if remove_option == "Delete One":
    index = st.number_input("Row index to delete", 0, len(pred_df)-1, 0)
    if st.button("Confirm Delete"):
        pred_df = pred_df.drop(index)
        pred_df.to_csv(PREDICTION_FILE, index=False)
        st.success("Deleted one record.")

if remove_option == "Delete Multiple":
    rows = st.multiselect("Select rows to delete", pred_df.index)
    if st.button("Confirm Deletions"):
        pred_df = pred_df.drop(rows)
        pred_df.to_csv(PREDICTION_FILE, index=False)
        st.success("Multiple records deleted.")

if remove_option == "Delete All":
    if st.button("⚠️ Confirm Delete All Data"):
        pred_df = pred_df.iloc[0:0]
        pred_df.to_csv(PREDICTION_FILE, index=False)
        st.warning("🚨 All prediction records cleared.")


# -----------------------------------------------
# VISUALIZATIONS BASED ON SAVED PREDICTIONS
# -----------------------------------------------
st.subheader("📊 Analytics from Saved Predictions")

if len(pred_df) > 0:
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Churn Count")
        fig, ax = plt.subplots()
        sns.countplot(data=pred_df, x="Prediction", palette="coolwarm", ax=ax)
        ax.set_xticklabels(["Stays (0)", "Leaves (1)"])
        st.pyplot(fig)

    with col2:
        st.write("### Tenure vs Churn")
        fig2, ax2 = plt.subplots()
        sns.barplot(data=pred_df, x="Prediction", y="tenure", palette="coolwarm", ax=ax2)
        ax2.set_xticklabels(["Stays", "Leaves"])
        st.pyplot(fig2)

else:
    st.info("No saved predictions yet. Make a prediction to generate analytics.")
