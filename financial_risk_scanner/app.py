import streamlit as st
import tempfile
import matplotlib.pyplot as plt
from pdf_utils import load_pdf
from rag_engine import create_vector_store, retrieve_context
from risk_agent import analyze_risk
from simulation_agent import simulate_scenario
from guardrails import validate_output
from n8n_trigger import trigger_n8n


st.set_page_config(page_title="Financial Risk Scanner", layout="wide")

st.title("📄 Financial Document Risk Scanner")
st.caption("Agentic AI • RAG Powered • Visual Risk Mapping • Simulation Mode")

uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    # Reset alert state for new upload
    st.session_state.pop("alert_triggered", None)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        file_path = tmp.name

    documents = load_pdf(file_path)
    vectordb = create_vector_store(documents)

    query = "Identify financial and legal risks"
    context = retrieve_context(vectordb, query)

    with st.spinner("Analyzing risks..."):
        raw_output = analyze_risk(context)

    is_valid, result = validate_output(raw_output)

    if is_valid:

        st.subheader("📊 Risk Heatmap")

        breakdown = result["risk_breakdown"]

        labels = list(breakdown.keys())
        values = list(breakdown.values())

        fig, ax = plt.subplots()
        ax.bar(labels, values)
        ax.set_ylim(0, 100)
        ax.set_ylabel("Risk Score")
        ax.set_title("Risk Breakdown")

        st.pyplot(fig)

        st.subheader("📋 Detailed Risk Analysis")
        st.json(result)

        # 🔥 Trigger n8n only once if HIGH risk
        if result["risk_level"] == "HIGH":

            if "alert_triggered" not in st.session_state:
                trigger_n8n(result)
                st.session_state["alert_triggered"] = True

            st.warning("🚨 High Risk Alert Triggered")

        st.divider()

        st.subheader("🧠 What If? Simulation Mode")

        user_question = st.text_input(
            "Ask a scenario question (e.g., What happens if I stop paying after 3 years?)"
        )

        if user_question:
            simulation_result = simulate_scenario(context, user_question)
            st.write(simulation_result)

    else:
        st.error("Guardrail Validation Failed")
        st.text(result)