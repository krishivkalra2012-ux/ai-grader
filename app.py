import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Configuration - Set this up ONCE at the start
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 2. UI Layout
st.title("AI Teacher Assistant")

tab1, tab2 = st.tabs(["Grade My Work", "Generate Quiz"])

# 3. Logic for Tab 1
with tab1:
    st.header("Grade My Work")
    uploaded_doc = st.file_uploader("Upload student document", type=["txt", "pdf"], key="grader")
    mark_scheme = st.text_area("Paste the Mark Scheme here:")
    
    if st.button("Grade Document"):
        if uploaded_doc and mark_scheme:
            # Read and process file
            doc_content = uploaded_doc.read().decode("utf-8")
            prompt = f"Grade this document based on the mark scheme. Provide feedback and a score.\n\nMark Scheme: {mark_scheme}\n\nDocument: {doc_content}"
            
            # Generate content
            try:
                response = model.generate_content(prompt)
                st.write(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
        else:
            st.warning("Please upload a document and paste the mark scheme.")

# 4. Logic for Tab 2
with tab2:
    st.header("Generate Quiz")
    st.write("Quiz generation logic coming soon!")
