import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="MindMeter", page_icon="🧠", layout="wide")

# --- HEADER SECTION ---
st.title("🧠 MindMeter")
st.subheader("Psychometric Analysis of Confidence, Happiness, and Mental Pressure")
st.markdown("""
Welcome!  
Please answer all the questions honestly. Your responses will help analyze your confidence, happiness, and mental pressure levels.  
All data is confidential and used only within the system for analysis.
""")

st.divider()

# --- CONSENT FORM ---
st.markdown("### Participant Consent")
consent = st.radio(
    "Do you voluntarily agree to participate and provide your responses as per the conditions stated?",
    ["No, I do not agree", "Yes, I agree and give my consent"]
)
if consent == "No, I do not agree":
    st.warning("You must agree to continue.")
    st.stop()

st.divider()

# --- QUESTION SETUP ---
sections = {
    "Confidence": [
        "I believe in my ability to solve difficult problems.",
        "I can take initiative in group projects.",
        "I am comfortable expressing my ideas in discussions.",
        "I approach challenges with a positive attitude.",
        "I adapt easily to new technologies or tools.",
        "I handle criticism without losing self-esteem."
    ],
    "Happiness": [
        "I generally feel happy and content.",
        "I enjoy spending time with friends and classmates.",
        "I feel satisfied with my daily life.",
        "I find joy in learning new things.",
        "I feel motivated to attend classes.",
        "I often feel optimistic about my future."
    ],
    "Mental Pressure": [
        "I often feel anxious before exams or submissions.",
        "I find it difficult to relax after college hours.",
        "I worry frequently about performance or grades.",
        "I feel mentally exhausted after studying for long hours.",
        "I overthink small academic issues.",
        "I find it difficult to balance study and personal life."
    ]
}

options = {
    1: "Strongly Disagree",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly Agree"
}

# --- QUESTIONNAIRE FORM ---
st.markdown("### Please respond to the following statements (1–5):")

responses = {}
for section, questions in sections.items():
    st.subheader(f"📘 {section} Section")
    for q in questions:
        responses[q] = st.radio(q, list(options.keys()), format_func=lambda x: options[x], key=q)
    st.divider()

# --- SUBMIT BUTTON ---
if st.button("Submit and Analyze"):
    df = pd.DataFrame.from_dict(responses, orient="index", columns=["Score"])

    # Calculate category averages
    confidence_score = df.loc[list(sections["Confidence"])].mean().values[0]
    happiness_score = df.loc[list(sections["Happiness"])].mean().values[0]
    pressure_score = df.loc[list(sections["Mental Pressure"])].mean().values[0]

    # Normalize to percentage
    conf_percent = confidence_score / 5 * 100
    happy_percent = happiness_score / 5 * 100
    press_percent = pressure_score / 5 * 100

    # --- Display Results ---
    st.success("✅ Analysis Completed Successfully!")

    col1, col2, col3 = st.columns(3)
    col1.metric("Confidence Level", f"{conf_percent:.1f}%", 
                "High" if conf_percent >= 70 else "Moderate" if conf_percent >= 50 else "Low")
    col2.metric("Happiness Level", f"{happy_percent:.1f}%", 
                "High" if happy_percent >= 70 else "Moderate" if happy_percent >= 50 else "Low")
    col3.metric("Mental Pressure", f"{press_percent:.1f}%", 
                "High" if press_percent >= 70 else "Moderate" if press_percent >= 50 else "Low")

    st.divider()

    # --- Visualization ---
    categories = ["Confidence", "Happiness", "Mental Pressure"]
    values = [conf_percent, happy_percent, press_percent]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.barh(categories, values, color=["#8E7CC3", "#FFD966", "#F4B183"])
    ax.set_xlim(0, 100)
    ax.set_xlabel("Score (%)")
    ax.set_title("Psychometric Result Overview")
    st.pyplot(fig)

    st.divider()

    # --- Interpretation ---
    st.markdown("### 🧩 Interpretation")
    if conf_percent >= 70 and happy_percent >= 70 and press_percent < 50:
        st.success("You exhibit strong confidence, high happiness, and healthy stress levels. Great balance!")
    elif press_percent > 70:
        st.warning("Your mental pressure level appears high. Consider taking breaks and practicing relaxation.")
    elif conf_percent < 50:
        st.info("Your confidence seems a bit low — try focusing on small wins and positive reinforcement.")
    else:
        st.write("You maintain a balanced mindset. Keep nurturing your emotional and mental well-being!")

    # Optional data download
    csv = df.to_csv().encode('utf-8')
    st.download_button("📥 Download My Responses (CSV)", data=csv, file_name="MindMeter_Responses.csv", mime="text/csv")

st.divider()
st.caption("© 2025 MindMeter | Your privacy and trust matter. Responses are not stored permanently.")
