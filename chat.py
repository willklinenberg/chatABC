import openai
import streamlit as st
import docx2txt
import numpy as np
import pandas as pd
import promptlayer


promptlayer.api_key = st.secrets["promptlayer_api"]

        
# Swap out your 'import openai'
openai = promptlayer.openai
openai.api_key = st.secrets["openai_api"]

file = st.file_uploader('Upload Discharge File (.docx)', type=[ 'docx'])

lang = st.selectbox('Language', options = (np.array(['English','Spanish', 'Mandarin', 'Korean', 'Hindi'])), index = 0)
# extract text
if file:
        
    text = docx2txt.process(file)

    ### language
    if lang != 'English':

        # Do something fun 🚀
        summary = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=str(text) + '\n Please translate the above discharge chart to ' + str(lang), 
        pl_tags=["name-guessing", "pipeline-2"],
        max_tokens=500
        )
        st.title('Discharge File: \n')
        st.write(summary.choices[0].text)

        lang_text = ' and translate to ' + str(lang)
    else:
        lang_text = ''
        st.title('Discharge File: \n')
        st.write(text)

    ## action items
    # Do something fun 🚀
    summary = openai.Completion.create(
    engine="text-davinci-003", 
    prompt=str(text) + '\n Place list the action items for the patient based on their discharge Notes stated above' + lang_text, 
    pl_tags=["name-guessing", "pipeline-2"],
    max_tokens=500
    )

    st.title('\n \n Action Items: \n')
    st.write(summary.choices[0].text +'\n \n')

    inst = summary.choices[0].text

    ### medication
    # Do something fun 🚀
    medication = openai.Completion.create(
    engine="text-davinci-003", 
    prompt=str(inst) + '\n Please list the medications that need to be taken based on the instructions paper above' + lang_text, 
    pl_tags=["name-guessing", "pipeline-2"],
    max_tokens=500
    )
    st.title('Medications: \n')
    st.write(medication.choices[0].text + '\n')

    ### Diet
    # Do something fun 🚀
    diet = openai.Completion.create(
    engine="text-davinci-003", 
    prompt=str(inst) + '\n Please create a list of dietary reccomendations based on the instructions paper above' + lang_text, 
    pl_tags=["name-guessing", "pipeline-2"],
    max_tokens=500
    )

    st.title('Diet Recomendations: \n')
    st.write(diet.choices[0].text + '\n')



    st.title('\n \n Calendar: \n')

    st.date_input('Select Date')
    d = {'Morning': ['Take 500 mg Metformin', '30 Min Exercise', ''], 'Evening': ['Take 500 mg Metformin', 'Take 10 mg Lisinopril', 'Take 15 mg Lipitor']}
    df = pd.DataFrame(d)
    st.write(df)

    st.title('Chat:')

    chat = st.text_input('Chat with Me!')



    if chat:
            # Do something fun 🚀
        summary = openai.Completion.create(
        engine="text-davinci-003", 
        prompt=str(inst) + '\n Please answer the following prompt based on the instructions paper above' + lang_text + ': ' + chat, 
        pl_tags=["name-guessing", "pipeline-2"],
        max_tokens=500
        )

        st.write('Answer: \n' + summary.choices[0].text)
    
    

