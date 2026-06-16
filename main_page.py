import pandas as pd
import streamlit as st
import datetime
import google_sheet_upload

sidebar_choice = st.sidebar.radio("選擇項目：", ["櫃位確認", "潑灑箱盤點"])

if sidebar_choice=='櫃位確認':
    upload=google_sheet_upload.get_worksheet('櫃位', 'sheet1')

    his_med=pd.read_pickle('files/his_med.pkl')

    his_med=his_med[his_med['DC_TYPE']!='YYY'] #篩選未DC品項

    egname_list=his_med['商品名'].to_list()

    st.title('櫃位確認')

    egname=st.selectbox('商品名：', egname_list, index=None)

    site=st.text_input('櫃位：')

    check=st.write()

    if st.button('送出'):
        diacode=his_med[his_med['商品名']==egname]['醫令碼'].iloc[0]
        df=google_sheet_upload.read_dataframe(upload)
        if df[(df['醫令碼']==diacode) & (df['櫃位']==str(site).upper())].empty==True:
            st.write('建立資料')
            result_dict={'醫令碼':diacode,
                    '櫃位':str(site).upper(),
                    '建立時間':str(datetime.datetime.now()),}
            google_sheet_upload.append_dict(upload, result_dict, list(result_dict.keys()))
            site=st.write(result_dict)
        else:
            st.write('已存在相同資料，跳過')
elif sidebar_choice=='潑灑箱盤點':
    st.title('潑灑箱盤點')
    nurse_station=st.selectbox('護理站：', ['膀胱功能室','3病房準備室','4病房護理站','5病房庫房','6病房庫房','7病房準備室','8病房準備室'], index=None)
    item_dict={'意外潑灑的處理單張': 1,
               '警示牌 (或封鎖線)': 1,
               '護目鏡 (或拋棄式面罩)': 1,
               'N95口罩': 1,
               '拋棄式手套': 2,
               '拋棄式防水隔離衣 (若隔離衣無附帽，則另須備拋棄式帽套)': 1,
               '帽套': 0,
               '拋棄式鞋套': 1,
               '吸水巾或吸水墊': 2,
               '丟棄式毛巾(或廢布)': 2,
               '漂白水': 1,
               '生物醫療廢棄物塑膠袋': 2,
               '可密閉硬塑膠容器': 1,
               '拋棄式杓子與畚箕': 1}
    
    default_data=list()
    for k, v in item_dict.items():
        default_data.append({"品項": k, "最少量": v, "效期": '', '實際數量': 0},)
    
    df = pd.DataFrame(default_data)
    edited_df = st.data_editor(
        df,
        column_config={
            '品項':st.column_config.SelectboxColumn(
                "品項",
                options=item_dict.keys(),),
            '效期': st.column_config.DatetimeColumn(
            "Appointment",
            min_value=datetime.date(2020, 6, 1),
            max_value=datetime.date(2050, 1, 1),
            format="YYYY/MM/DD",),
            },
        num_rows="dynamic")
    
    if st.button('送出'):
        print(df)