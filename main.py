#Install libs that are not preinstalled
import streamlit as st
import pandas as pd
import json
import numpy as np
import requests
import warnings
import os
import io
import base64
warnings.filterwarnings('ignore')
st.set_page_config(page_title="API Example SIPmath™ 3.0 Library Generator", page_icon=None, layout="wide", initial_sidebar_state="auto", menu_items=None)
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.cache(allow_output_mutation=True)
def get_img_with_href(local_img_path, target_url):
    img_format = os.path.splitext(local_img_path)[-1].replace('.', '')
    bin_str = get_base64_of_bin_file(local_img_path)
    html_code = f'''
        <a href="{target_url}">
            <img src="data:image/{img_format};base64,{bin_str}" height="125"; />
        </a>'''
    return html_code
# path = os.path.dirname(__file__)
path = "."
   
PM_logo = get_img_with_href(path+'/images/PM_logo.png','https://www.probabilitymanagement.org/')
Metalog_Distribution = get_img_with_href(path+'/images/Metalog Distribution.png','https://www.probabilitymanagement.org/metalog')
HDR_Generator = get_img_with_href(path+'/images/HDR Generator.png','https://www.probabilitymanagement.org/hdr')
SIPmath_Standard = get_img_with_href(path+'/images/SIPmath Standard.png','https://www.probabilitymanagement.org/sipmath')
# image = Image.open('PM_logo_transparent.png')
images_container = st.container()
images_cols = images_container.columns([13,11,3,3,3])

images_cols[0].markdown(PM_logo, unsafe_allow_html=True)
images_cols[4].markdown(Metalog_Distribution, unsafe_allow_html=True)
images_cols[1].header("API Example SIPmath™ 3.0 Library Generator")
images_cols[3].markdown(HDR_Generator, unsafe_allow_html=True)
images_cols[2].markdown(SIPmath_Standard, unsafe_allow_html=True)
main_container = st.empty()
empty_table = st.empty()
table_container = empty_table.container()
api_url = "http://gsxwmkizyo.us17.qoddiapp.com/sipmath-json"

st.sidebar.header('User Inputs')

# Collects user input features into dataframe
data_type = st.sidebar.radio('Input Data Type', ('Excel File',), index=0)
data_type_str = data_type.split()[0].lower()


if data_type == 'Excel File':
    uploaded_file = st.sidebar.file_uploader("Upload an Excel file", type=["xls","xlsx"],accept_multiple_files=False)
    payload = {}
    if uploaded_file != None:
        input_df = None
        uploaded_file = uploaded_file if isinstance(uploaded_file, list) else [uploaded_file]
        for i,file in enumerate(uploaded_file):
            reading_engine = "openpyxl" if file.name[-1] == 'x' else 'xlrd'
            input_df = pd.read_excel(file, engine = reading_engine).fillna('')
            # [for x in i]
            name = file.name.replace(file.name.split('.')[-1],"")
            # with main_contanier.container():
            table_container.subheader(f"Preview for {name}")
            payload['filename'] = input_df.columns[1]
            payload['author'] = input_df.iat[0,1]
            input_df.columns = input_df.columns.str.replace(r"Unnamed\: \d*", "", regex=True)
            # table_container.write(input_df.columns)
            input_df.iloc[2:, 3] = np.where(input_df.iloc[2:, 2] == 'u', "", np.where(input_df.iloc[2:, 2] == 'su', "", input_df.iloc[2:, 3]))
            input_df.iloc[2:, 7] = np.where(input_df.iloc[2:, 2] == 'u', "", np.where(input_df.iloc[2:, 2] == 'sl', "", input_df.iloc[2:, 7]))
            table_container.write(input_df.to_html(index=False), unsafe_allow_html=True)
            table_container.write("If data was read correctly. Click the 'Get SIPmath' button.")
            input_df = pd.DataFrame(input_df.iloc[2:,:].to_numpy(),columns = input_df.iloc[1,:].values)
            payload["variable_name"] = input_df.iloc[:,0].to_list()
            payload["probs"] = [[low_prob, 0.5, 1.0 - low_prob] for low_prob in input_df.iloc[:,1].to_list()]
            payload["boundedness"] = input_df.iloc[:,2].to_list()
            bounds = []
            for i, boundness in enumerate(payload["boundedness"]):
                if boundness == 'b':
                    bounds.append(input_df.iloc[i,[3,7]].to_list())
                elif boundness == 'sl':
                    bounds.append([input_df.iat[i,3]])
                elif boundness == 'su':
                    bounds.append([input_df.iat[i,7]])
                else:
                    bounds.append([0,1])
            payload["bounds"] = bounds
            payload["data"] = input_df.iloc[:,4:7].to_numpy().tolist()
            payload["term_saved"] = [len(payload["probs"][0])] * len(payload["probs"])
            payload["seeds"] = input_df.iloc[:,8:-1].values.tolist()
            print(payload)
            if st.sidebar.button('Get SIPmath'):
                r = requests.post(api_url, json=payload)
                if r.ok:
                    returned_Sipmath = r.json()
                    table_container.download_button(f"Download {returned_Sipmath['name']}", json.dumps(returned_Sipmath, indent=4), returned_Sipmath['name'])
                    table_container.write(f"Preview of {returned_Sipmath['name']}:")
                    table_container.json(returned_Sipmath)

    else:
        input_df = pd.DataFrame()