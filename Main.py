import streamlit as st 
import numpy as np
import pandas as pd
import time

st.title('Streamlit Test 測定結果')

#中身をかく
# st.write('Interactive Widge')
st.write('Progress bar')
'Start'

# text = st.sidebar.text_input('Tell me waht you like')
# condition = st.sidebar.slider('How are you',0,100,50)


# 'Your hobby:',text
# 'Condition:',condition

latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
    latest_iteration.text(f'Iteration {i + 1}')
    bar.progress(i + 1)
    time.sleep(0.1)

uploaded_file = st.file_uploader("アクセスログをアップロードしてください。")
if uploaded_file is not None:
    df = pd.read_csv(
        uploaded_file
        )
    st.markdown('### アクセスログ（先頭5件）')
    st.write(df.head(5))
else :
    st.markdown('Not uploaded')
    
# latest_iteration = st.empty()
# bar = st.progress(0)

# for i in range(100):
#     latest_iteration.text(f'Iteration {i + 1}')
#     bar.progress(i + 1)
#     time.sleep(0.1)



left_column,right_column = st.columns(2)
button = left_column.button('右カラムに文字を表示')
if button:
    right_column.write('ここは右カラム')

st.snow()






# text = st.text_input('Tell me waht you like')
# condition = st.slider('How are you',0,100,50)


# 'Your hobby:',text
# 'Condition:',condition

