import streamlit as st
import json
import requests

from config import Backend_URL

st.title("Your AI Assistant")

# Taking user input
k = st.slider("Pick the number of papers to be suggested",1,5,3)

text = st.text_area('Your Paragraph',height=100)


inputs= {
        "paragraph": text,
        "k": k
    }


if st.button("search"):
    col1, col2 = st.columns([3,1],gap="large")
    
    data = json.dumps(inputs) #convert input to json
    res = requests.post(url=Backend_URL,data=data) #send input to backend

    
    output=json.loads(res.content) #reconvert backend response from json to dict
    with col1:
        st.subheader("Papers")
        
        for i in range(len(output["papers"])):
            st.write(output["papers"][i])

    with col2:
        st.subheader("Scores")
        for i in range(len(output["scores"])):
            st.write(output["scores"][i])

    with st.expander("See summaries"):
        
        for i in range(len(output["papers"])):
            st.subheader(output["papers"][i])
            st.write(output["summaries"][i])

    with st.expander("See Abstracts"):
        
        for i in range(len(output["papers"])):
            st.subheader(output["papers"][i])
            st.write(output["abstracts"][i])
    