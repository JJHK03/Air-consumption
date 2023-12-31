import streamlit as st
import pandas as pd
import time


st.title('測定結果')

try:

    uploaded_file = st.file_uploader("ログをアップロードしてください。")
    if uploaded_file is not None:
        df = pd.read_csv(
            uploaded_file
            )
        st.markdown('### ログ（先頭5件）')
        st.write(df.head(5))
    else :
        st.markdown('Not uploaded')
        
    latest_iteration = st.empty()
    bar = st.progress(0)

    for i in range(100):
        latest_iteration.text(f'Iteration {i + 1}')
        bar.progress(i + 1)
        time.sleep(0.01)


    # st.write('瞬間流量,圧力,積算流量')
    tab1, tab2, tab3, tab4, tab5, tab6= st.tabs(["瞬間流量", "積算流量", "圧力","コスト","CO2排出量","電力量"])

    def edit_df(df):
        drop_col = ['DataType','StatusCode','ServerTimeStamp']
        df = df.drop(drop_col,axis = 1)
        df['SourceTimeStamp'] = df['SourceTimeStamp'].str[11:-1]#タイムスタンプの桁数調整
        return df


    df = edit_df(df)


    df2 = df[df['PrimaryKey'].isin([2])]#流量用データの中の数字でソートする
    df2 = df2.rename(columns={'Value':'瞬間流量L/min','SourceTimeStamp':'Time'})# 流量用inplace=Trueは設定せず
    drop_col1 = ['PrimaryKey']
    df2 = df2.drop(drop_col1, axis = 1)
    df2 = df2.set_index('Time')
    df2_mean = df2.mean()
    



    df['Value'] = df['Value']/1000#圧力の桁数調整
    df3=df[df['PrimaryKey'].isin([3])]#圧力用データの中の数字でソートする
    df3 = df3.rename(columns={'Value':'Mpa','SourceTimeStamp':'Time'})# 圧力用inplace=Trueは設定せず
    drop_col1 = ['PrimaryKey']
    df3 = df3.drop(drop_col1,axis = 1)
    df3 = df3.set_index('Time')

    df['Value'] = df['Value']*10000#積算流量の桁数調整
    df1=df[df['PrimaryKey'].isin([1])]#積算流量用データの中の数字でソートする

    df1 = df1.rename(columns={'Value':'積算流量L','SourceTimeStamp':'Time'})# 積算流量用inplace=Trueは設定せず
    drop_col1 = ['PrimaryKey']
    df1 = df1.drop(drop_col1,axis = 1)
    df1 = df1.set_index('Time')


    with tab1:
        st.header("瞬間流量をグラフで表示")
        df2
        st.bar_chart(df2)
        low_flow = float(st.number_input("低流量時の流量を記入してください:L/min"))
        df2_1 = df2[df2['瞬間流量L/min']<= low_flow]
        st.bar_chart(df2_1)
        df2_1mean = df2_1.mean()
        st.write('低流量平均流量',float(df2_1mean))
        df2_2 = df2[df2['瞬間流量L/min']>= low_flow]
        df2_2mean = df2_2.mean()
        st.write('通常流量平均流量',float(df2_2mean))
        
    with tab2:
        st.header("積算流量")
        df1
        st.bar_chart(df1)

    with tab3:
        st.header("圧力")
        df3
        st.bar_chart(df3)
    with tab4:
        
        air_cost = float(st.number_input('エアコスト(¥/m3)はいくら？'))
        st.write('エアコスト', air_cost,'円')
        
        Ope_hour = int(st.number_input('稼働時間は1日何時間？'))
        st.write("稼働時間： ", Ope_hour,"時間")
        
        
        Ope_ratio = st.number_input('一日の設備稼働率は？')
        st.write('設備稼働率', Ope_ratio, '%')
        st.write('時間',int(Ope_hour)*60*(int(Ope_ratio)/100),'(分)/日')
        
        Ope_days = st.number_input('年間稼働日は？')
        st.write('年間稼働日', Ope_days, '日')
        
        
        st.header("全体のコスト")
        
        #消費流量
        air_consum = float(float(df2_mean)*60*int(Ope_hour)*(int(Ope_ratio)/100)/1000)
        st.write('消費流量','{:.2f}'.format(air_consum),'m3')
        

        #Cost
        cost = float(air_consum)*float(air_cost)
        st.write('一日あたりのエアコスト','{:.2f}'.format(cost),'円')
        
        cost_1 = float(cost)*int(Ope_days)
        st.write('年間コスト''{:.2f}'.format(cost_1),'円')
        
        
        st.header("低流量時のコスト")
        
        #消費流量
        air_consum2 = float(float(df2_1mean)*60*int(Ope_hour)*(int(Ope_ratio)/100)/1000)
        st.write('消費流量','{:.2f}'.format(air_consum2),'m3')

        #Cost
        cost2 = float(air_consum2)*float(air_cost)
        st.write('一日あたりのエアコスト','{:.2f}'.format(cost2), '円')
        
        cost_2 = float(cost2)*int(Ope_days)
        st.write('年間コスト''{:.2f}'.format(cost_2),'円')
        
        
        st.header("通常流量時のコスト")
        
        #消費流量
        air_consum3 = float(float(df2_2mean)*60*int(Ope_hour)*(int(Ope_ratio)/100)/1000)
        st.write('消費流量','{:.2f}'.format(air_consum3),'m3')

        #Cost
        cost3 = float(air_consum3)*float(air_cost)
        st.write('一日あたりのエアコスト','{:.2f}'.format(cost3), '円')
        
        cost_3 = float(cost3)*int(Ope_days)
        st.write('年間コスト''{:.2f}'.format(cost_3),'円')
        
    with tab5:
        st.header("全体のCO2排出量")
        emitted_CO2 = 0.0586
        A_emitted_CO2 = float(air_consum)*float(emitted_CO2)
        st.write('一に当たり排出量''{:.2f}'.format(A_emitted_CO2), 'KgCO2/m3')
        
        A_emitted_CO2_year = float(A_emitted_CO2)*float(Ope_days)
        st.write('年間排出量''{:.2f}'.format(A_emitted_CO2_year), 'KgCO2/m3')
        
        st.header("一日あたり低流量時のCO2排出量")
        emitted_CO2_1 = 0.0586
        A_emitted_CO2_1 = float(air_consum2)*float(emitted_CO2_1)
        st.write('{:.2f}'.format(A_emitted_CO2_1), 'KgCO2/m3')
        
        
        
        st.header("一日あたり通常流量時のCO2排出量")
        emitted_CO2_2 = 0.0586
        A_emitted_CO2_2 = float(air_consum3)*float(emitted_CO2_2)
        st.write('{:.2f}'.format(A_emitted_CO2_2), 'KgCO2/m3')
        
    with tab6:
        st.header("全体の電力量")
        power_consump = 0.100
        A_power_consump  = float(air_consum)*float(power_consump)
        st.write('一に当たり電力量''{:.2f}'.format(A_power_consump), 'kWh/m3')
        
        A_power_consump_year = float(A_emitted_CO2)*float(Ope_days)
        st.write('年間電力量''{:.2f}'.format(A_power_consump_year), 'kWh/m3')
        
        st.header("一日あたり低流量時の電力量")
        power_consump_1 = 0.100
        A_power_consump_1 = float(air_consum2)*float(power_consump_1)
        st.write('{:.2f}'.format(A_power_consump_1), 'kWh/m3')
        
        
        
        st.header("一日あたり通常流量時の電力量")
        power_consump_2 = 0.100
        A_power_consump_2 = float(air_consum3)*float(power_consump_2)
        st.write('{:.2f}'.format(A_power_consump_2), 'kWh/m3')
    
    
except:
    st.error("Oh......error")