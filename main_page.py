import pandas as pd
import streamlit as st
import datetime
import google_sheet_upload

upload=google_sheet_upload.get_worksheet('櫃位', 'sheet1')

his_med=pd.read_pickle('files/his_med.pkl')

egname_list=his_med['商品名'].to_list()

st.title('櫃位確認')

egname=st.selectbox('商品名：', egname_list, index=None)

site=st.text_input('櫃位：')

check=st.write()

if st.button('送出'):
    diacode=his_med[his_med['商品名']==egname]['醫令碼'].iloc[0]
    result_dict={'醫令碼':diacode,
                 '櫃位':str(site).upper(),
                 '建立時間':str(datetime.datetime.now()),}
    google_sheet_upload.append_dict(upload, result_dict, list(result_dict.keys()))
    site=st.write(result_dict)