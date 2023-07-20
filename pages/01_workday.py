import streamlit as st
import pandas as pd
import base64
import configparser
from datetime import datetime, timedelta
import csv

st.set_page_config(layout="wide")

"""
### 翌営業日計算

「翌営業日計算」ツールは、週末と指定された祝日を考慮して次の営業日を算出するStreamlitアプリです。
開始日と終了日を選択し、対応する日付範囲の次の営業日を含むCSVファイルを生成します。

* カスタム祝日はconfig.iniファイルに設定可能で、土日と祝日を除いた次の営業日を計算します。
* 生成されたCSVファイルは、ダウンロードリンクをクリックすることでダウンロード可能です。

"""
def get_holidays():
    # 创建一个ConfigParser对象
    config = configparser.ConfigParser()
    # 读取配置文件
    config.read('configdata/config.ini',encoding='utf-8')

    # 将数据加载到内存中
    data = {}

    # 遍历配置文件的所有节(section)
    for section in config.sections():
        # 获取节(section)下的所有选项(option)和值(value)
        options = config.options(section)
        values = [config.get(section, option) for option in options]

        # 将选项和值组成字典，存入data字典
        data[section] = dict(zip(options, values))
    holidaylist = data['section3'].values()
    holidays = [datetime.strptime(date_str, '%Y-%m-%d').date() for date_str in holidaylist]
    return holidays

def main():
    start_date = st.date_input('Start Date',value=datetime.strptime("2022-01-01", '%Y-%m-%d').date())
    end_date = st.date_input('End Date',value=datetime.strptime("2022-12-31", '%Y-%m-%d').date())

    if st.button('Create CSV'):
        generate_csv(start_date, end_date)
        
def next_business_day(start_date):
    # 祝日を考慮して翌営業日を計算
    holidays = get_holidays()
    next_day = start_date + timedelta(days=1)
    while next_day.weekday() in [5, 6] or next_day in holidays:
        #print("next_day.weekday() in [5, 6] or next_day in holidays")
        next_day += timedelta(days=1)
    return next_day
        
def generate_csv(start_date, end_date):
    date_list = []
    current_date = start_date
    while current_date <= end_date:
        next_biz_day = next_business_day(current_date)
        date_list.append([current_date,next_biz_day])
        current_date += timedelta(days=1)
    df = pd.DataFrame(date_list, columns=['CurDate','NextWorkDate'])
    
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="nextworkdaylist.csv">Click to download CSV file</a>'
    st.markdown(href, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
