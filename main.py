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
# images_container
# images_container.image(image, unsafe_allow_html=True)
main_container = st.empty()
empty_table = st.empty()
table_container = empty_table.container()
slider_container = st.empty().container()
graphs_container = st.empty().container()
graphs_container_main = st.empty().container()
api_url = "http://gsxwmkizyo.us17.qoddiapp.com/sipmath-json"
#Taken from the metalog
# @st.cache(suppress_st_warning=True)

# def input_data(name,i,df,probs=None):
#     if probs is None:
#         probs = np.nan
#         max_val = 16
#         default_val = 5
#         input_data_type = 'csv'
#         data_columns = df.columns
#         table_container.write("If the data above appears correct, enter your parameters in the sidebar for this file.")
#     else:
#         max_val = df.shape[0]
#         default_val = max_val
#         input_data_type = 'quantile'
#         data_columns = df.columns
    
#     with st.sidebar.expander("Output Options"):
#         filename_container = st.container()
#         file_name_no_ext, file_ext = filename_container.columns(2)
#         filename = file_name_no_ext.text_input(f'Filename {i+1}', name,key=f"{name}_{i}_filename") + '.SIPmath'
#         file_ext.write('File Extension')
#         file_ext.write('.SIPmath')
#         author = st.text_input(f'Author for {filename}', 'Unknown',key=f"{name}_author")
#         # if data_type_str != "quantile":
#         dependent_name = 'Guassian Copula' if data_type_str == "csv" else "Correlation Matrix"
#         dependence = st.selectbox('Dependence', ('independent',dependent_name),key=f"{name}_{i}_dependence")
#         correlation_df = None
#         if dependence == "Correlation Matrix":
#           number_variables = len(data_columns)
#           print(number_variables)
#           correlation_container = slider_container.columns(number_variables)
#           if 'quantiles_data' in st.session_state and 'correlations' in st.session_state['quantiles_data']:
#             saved_df = st.session_state['quantiles_data']['correlations']
#             for row in df.columns:
#               for col in df.columns:
#                 print("value in saved_df is",saved_df.loc[row,col])
#                 st.session_state[f"{row} vs {col}"] = saved_df.loc[col,row]
#           corrs_data = [[float(correlation_container[i-1].number_input(f'{df.columns[j]} vs {df.columns[i-1]} ', 
#                value = 1.0 if j+1 == i else 0.0,
#                format = "%f",
#                # step = 0.1
#                 on_change = update_correlations,
#                 args = (f"{df.columns[j]} vs {df.columns[i-1]}",),
#                 key=f"{df.columns[j]} vs {df.columns[i-1]}"))  for j in range(i)] for i in range(1,number_variables+1)]
#           print("corrs_data", corrs_data)
#           correlation_df = pd.DataFrame(corrs_data,columns=df.columns,index=df.columns)
#           st.session_state['quantiles_data']['correlations'] = correlation_df
#           check_correlation_df = correlation_df.fillna(correlation_df.T)
#           print("check_correlation_df",check_correlation_df)
#           correlation_check_run = True
#           if correlation_container[number_variables-1].button('Store Correlation', key='correlation_done'):
#             print('ran correlation check')
#             print(np.linalg.eigvals(check_correlation_df.to_numpy()))
#             correlation_check_run = np.all(np.linalg.eigvals(check_correlation_df.to_numpy()) > 0)
#             if not correlation_check_run:
#               correlation_container[0].warning("The correlation matrix needs to be feasible.")
#               # st.stop()
            
#           print(correlation_df)
#             # pass
#         if dependence != 'independent':
#             dependence = 'dependent'
#         # else:
#             # dependence = 'independent'
#         # boundedness = st.selectbox('Boundedness', ("'u' - unbounded", 
#                                                            # "'sl' - semi-bounded lower", 
#                                                            # "'su' - semi-bounded upper",
#                                                            # "'b' - bounded on both sides"),key=f"{name}_boundedness")
                                                           
#         # if boundedness == "'b' - bounded on both sides":
#             # #convert to float and list
#             # boundsl = st.text_input('Lower Bound', '0',key=f"{name}_lower")
#             # boundsu = st.text_input('Upper Bound', '1',key=f"{name}_upper")
#             # bounds = [float(boundsl),float(boundsu)]
#         # elif boundedness.find("lower") != -1:
#             # bounds = [float(st.text_input('Lower Bound', '0',key=f"{name}_lower"))]
#         # elif boundedness.find("upper") != -1:
#             # bounds = [float(st.text_input('Upper Bound', '1',key=f"{name}_upper"))]
#         # else:
#             # bounds = [0,1]
            
#         # boundedness = boundedness.strip().split(" - ")[0].replace("'","")
#         # if max_val > 3:
#             # term_saved = st.slider('Term Saved',3,max_val,default_val,key=f"{name}_term_saved")
#         # else:
#              # term_saved = 3
#         if 'mfitted' in st.session_state:
#             fit_data = [not st.session_state['mfitted'][input_data_type][x]['fit'] is None
#                                 for x in data_columns 
#                                     if x in st.session_state['mfitted'][input_data_type]]     
#             # for x in data_columns:
#                 # if x in st.session_state['mfitted'][input_data_type]:
#                     # st.session_state['mfitted'][input_data_type][x]['options']['seeds'] = st.session_state['quantiles_data'][x]['seeds']
                                                     
#             seeds_data = ['seeds' in st.session_state['mfitted'][input_data_type][x]['options'] 
#                                         for x in data_columns 
#                                             if x in st.session_state['mfitted'][input_data_type]] 
#         # print("fit_data",fit_data)
#         # print("seeds_data",seeds_data)
#          # ###### I need to fix the problem by adjusting csv to variable then select it based on if probs is None or not.
#         if 'mfitted' in st.session_state and all(fit_data) and all(seeds_data):
#             term_saved = [st.session_state['mfitted'][input_data_type][x]['options']['terms'] if x in st.session_state['mfitted'][input_data_type] else None for x in data_columns]
#             print("term_saved is ",type(term_saved[0]))
#             if all(term_saved) and "--------Enter number of terms--------" not in term_saved:
#                 print(f'Writing SIPmath with data_columns as {data_columns}')
#                 boundedness = [st.session_state['mfitted'][input_data_type][x]['options']['boundedness'] if x in st.session_state['mfitted'][input_data_type] else None for x in data_columns]
#                 bounds = [[y for y in st.session_state['mfitted'][input_data_type][x]['options']['bounds']] if x in st.session_state['mfitted'][input_data_type] else None for x in data_columns]
#                 print(bounds)
#                 preview_options = pd.DataFrame(term_saved, index = data_columns, columns = ['Term'])
#                 preview_options['Boundedness'] = boundedness
#                 preview_options['Lower Bounds'] = [float(x[0]) if y == 'b'  or y == 'sl' else np.nan for x,y in zip(bounds,boundedness) ]
#                 preview_options['Upper Bounds'] = [float(x[-1]) if y == 'b'  or y == 'su' else np.nan for x,y in zip(bounds,boundedness) ]
#                 print(preview_options['Term'])
#                 for coeff_num in range(int(preview_options['Term'].max())):
#                     # preview_options[f'A {coeff_num + 1}'] = [st.session_state['mfitted'][input_data_type][x]['fit']['A'].iloc[coeff_num,st.session_state['mfitted'][input_data_type][x]['options']['terms'] - 1] for x in data_columns]
#                     preview_options[f'A {coeff_num + 1}'] = [st.session_state['mfitted'][input_data_type][x]['fit']['A'].iloc[coeff_num,st.session_state['mfitted'][input_data_type][x]['options']['terms'] - 1] 
#                                                                                 if st.session_state['mfitted'][input_data_type][x]['fit']['A'].shape[0] > coeff_num else None for x in data_columns]
#                 # preview_options = preview_options.T
#                 table_container.write(preview_options)
#                 converted_seeds = [{k:convert_to_number(v) for k,v in st.session_state['mfitted'][input_data_type][x]['options']['seeds'].items()} for x in data_columns ]
#                 print("converted_seeds is",converted_seeds)
#                 if st.button(f'Convert to {filename.split(".")[0]} SIPmath Json?',key=f"{filename.split('.')[0]}_term_saved"):
#                     table_container.subheader("Preview and Download the JSON file below.")
#                     data_dict_for_JSON = dict(boundedness=boundedness,
#                                    bounds=bounds,
#                                    term_saved=term_saved)
#                     print("probs in JSON", probs)
#                     PySIP.Json(SIPdata=df,
#                                    file_name=filename,
#                                    author=author,
#                                    dependence=dependence,
#                                    setupInputs=data_dict_for_JSON,
#                                    seeds = converted_seeds,
#                                    probs=probs,
#                                    quantile_corr_matrix = correlation_df)
                                   
#                     with open(filename) as f:
#                         st.download_button(
#                                 label=f"Download {filename}",
#                                 data=f,
#                                 file_name=filename
#                                 )
#                 # st.text("Copy the link below to paste into SIPmath.")
#                 # with open(filename, 'rb') as f:
#                     # st.write(sent_to_pastebin(filename,f.read()).text.replace("https://pastebin.com/","https://pastebin.com/raw/"))
#                     table_container.text("Mouse over the text then click on the clipboard icon to copy to your clipboard.")
#                     with open(filename, 'rb') as f:
#                         table_container.json(json.load(f))
#         else:
#             st.warning(f'{filename}.SIPmath cannot be saved until all variables have been configured.')

#st.title('SIPmath JSON Creator')
st.sidebar.header('User Input Parameters')

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
                    table_container.download_button(f"Download {returned_Sipmath['name']}", str(returned_Sipmath), returned_Sipmath['name'])
                    table_container.write(f"Preview of {returned_Sipmath['name']}:")
                    table_container.json(returned_Sipmath)


    else:
        input_df = pd.DataFrame()