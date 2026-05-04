import streamlit as st
import google.generativeai as genai
from PIL import Image

st.title("AI Teacher Assistant")
api_key = st.text_input("Enter your Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    tab1, tab2 = st.tabs(["Grade My Work", "Generate Quiz"])

    with tab1:
        st.header("Grade My Work")
        uploaded_doc = st.file_uploader("Upload student document", type=["txt", "pdf"], key="grader")
        mark_scheme = st.text_area("Paste the Mark Scheme here:")
        if st.button("Grade Document"):
            if uploaded_doc and mark_scheme:
                doc_content = uploaded_doc.read().decode("utf-8")
                prompt = f"Grade this document based on the mark scheme. Provide feedback and a score.\n\nMark Scheme: {mark_scheme}\n\nDocument: {doc_content}"
                response = model.generate_content(prompt)
                st.write(response.text)
            else:
                st.warning("Please upload a document and paste the mark scheme.")

    with tab2:
        st.header("Generate Quiz")
        quiz_files = st.file_uploader("Upload materials (images/text)", type=["jpg", "png", "txt"], accept_multiple_files=True)
        num_questions = st.slider("How many questions?", 1, 10, 5)
        if st.button("Generate Quiz"):
            if quiz_files:
                model_input = [f"Create a {num_questions}-question quiz. If images are present, ask about them."]
                for file in quiz_files:
                    if file.type.startswith("image"):
                        img = Image.open(file)
                        model_input.append(img)
                    else:
                        model_input.append(file.read().decode("utf-8"))
                response = model.generate_content(model_input)
                st.write(response.text)
