import streamlit as st
import requests
from typing import List
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder


API_BASE_URL = "http://localhost:8000"


st.set_page_config(
    page_title="Работа с геологическими образцами",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title("Работа с геологическими образцами")
st.write("test")


st.sidebar.header("Категория")
category = st.sidebar.radio("Выберите категорию:", ("Скважины", "Образцы"))

def fetch_data(endpoint, params=None):
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        st.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        st.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        st.error(f"OOps: Something Else: {err}")
    return None

# Function to display data in a nice table using AgGrid
def display_table(data, columns):
    if not data:
        st.info("No data to display.")
        return
    df = pd.DataFrame(data)
    if columns:
        df = df[columns]
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)
    gb.configure_side_bar()
    gb.configure_default_column(enablePivot=True, enableGroup=True, enableValue=True, enableRowGroup=True)
    gridOptions = gb.build()
    AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, height=400, fit_columns_on_grid_load=True)

# Drill Holes Section
if category == "Скважины":
    st.header("Скважины")
    sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр"))
    
    if sub_category == "Показать всё":
        st.subheader("Все скважины")
        data = fetch_data("/drill_hole/")
        display_table(data, ["id", "drill_hole", "geological_complex", "ore_zone"])  # Update columns as per your model
    elif sub_category == "Фильтр":
        st.subheader("Фильтр")
        with st.form(key='filter_form_drill_hole'):
            drill_hole_id = st.number_input("ID", min_value=0, step=1)
            drill_hole = st.text_input("Скважина")
            geological_complex = st.text_input("Комплекс")
            ore_zone = st.text_input("Рудная зона")
            submitted = st.form_submit_button("Применить фильтр")
        
        if submitted:
            params = {}
            if drill_hole_id:
                params['id'] = drill_hole_id
            if geological_complex:
                params['geological_complex'] = geological_complex
            if drill_hole:
                params['drill_hole'] = drill_hole
            if ore_zone:
                params['ore_zone'] = ore_zone
            data = fetch_data("/drill_hole/by_filter", params=params)
            display_table(data, ["id", "drill_hole", "geological_complex", "ore_zone"])  # Update columns as per your model

# Samples Section
elif category == "Образцы":
    st.header("Образцы")
    sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр"))
    
    if sub_category == "Показать всё":
        st.subheader("Все образцы")
        data = fetch_data("/samples/")
        display_table(data, ["id", "sample_name", "drill_hole_id", "depth_m", "rock_type"])  # Update columns as per your model
    elif sub_category == "Фильтр":
        st.subheader("Filter Samples")
        with st.form(key='filter_form_sample'):
            sample_id = st.number_input("ID", min_value=0, step=1)
            sample_name = st.text_input("Образец")
            drill_hole_id = st.number_input("ID скважины", min_value=0, step=1)
            rock_type = st.text_input("Тип")
            submitted = st.form_submit_button("Применить")
        
        if submitted:
            params = {}
            if sample_id:
                params['id'] = sample_id
            if sample_name:
                params['sample_name'] = sample_name
            if drill_hole_id:
                params['drill_hole_id'] = drill_hole_id
            if rock_type:
                params['rock_type'] = rock_type
            data = fetch_data("/samples/by_filter", params=params)
            if isinstance(data, dict) and 'message' in data:
                st.info(data['message'])
            else:
                display_table(data, ["id", "sample_name", "drill_hole_id", "depth_m", "rock_type"])  # Update columns as per your model