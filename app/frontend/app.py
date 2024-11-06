import streamlit as st
import requests
from typing import List
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
from photo_handler import display_photos


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

def display_table(data, columns, key):
    if not data:
        st.info("Нет данных для отображения.")
        return None
    if not isinstance(data, list):
        st.error("Unexpected data format.")
        st.write(data)  # For debugging purposes
        return None
    df = pd.DataFrame(data).reset_index(drop=True)
    if columns:
        existing_columns = [col for col in columns if col in df.columns]
        df = df[existing_columns]
    
    # Configure AgGrid options
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True)  # Enable pagination
    gb.configure_side_bar()  # Enable sidebar
    gb.configure_default_column(enablePivot=True, enableGroup=True, enableValue=True, enableRowGroup=True)
    gb.configure_selection(selection_mode="single", use_checkbox=True)  # Enable single row selection with checkbox

    if 'index' in df.columns:
        gb.configure_column("index", hide=True)

    # Optional: Add alternating row colors for better readability
    row_highlight_js = JsCode("""
    function(params) {
        if (params.node.rowIndex % 2 === 0) {
            return {
                'background-color': '#f9f9f9'
            }
        }
    }
    """)
    #gb.configure_row_style(rowStyle=row_highlight_js)

    gridOptions = gb.build()

    grid_response = AgGrid(
        df, 
        gridOptions=gridOptions, 
        enable_enterprise_modules=True, 
        height=400, 
        fit_columns_on_grid_load=True,
        key=key,
        update_mode=GridUpdateMode.SELECTION_CHANGED
    )

    selected = grid_response.get("selected_rows", [])

    if isinstance(selected, pd.DataFrame):
        if not selected.empty:
            # Convert the first selected row to a dictionary
            return selected.iloc[0].to_dict()
        return None
    elif isinstance(selected, list):
        if selected:
            # Return the first selected row as a dictionary
            return selected[0]
        return None
    else:
    	if selected is not None:
        	st.error("Unknown selected_rows type")
        	return None

# Drill Holes Section
if category == "Скважины":
    st.header("Скважины")
    sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр"))
    
    if sub_category == "Показать всё":
        st.subheader("Все скважины")
        with st.spinner("Загрузка всех скважин..."):
            data = fetch_data("/drill_hole/")

        selected_drill_hole = display_table(data, ["id", "drill_hole", "geological_complex", "ore_zone"], key="drill_holes_all")
        
        if selected_drill_hole:
            st.success("Выбранная скважина:")
            st.json(selected_drill_hole)
            
            # Fetch and display related samples
            drill_hole_id = selected_drill_hole.get("id")
            if drill_hole_id is not None:
                st.subheader(f"Образцы в скважине ID {drill_hole_id}")
                with st.spinner("Загрузка связанных образцов..."):
                    samples_data = fetch_data(f"/samples/drill_hole/{drill_hole_id}")
                display_table(samples_data, ["id", "sample_name", "depth_m", "full_name", "texture", "structure", "ore_mineralization"], key=f"samples_in_drill_hole_{drill_hole_id}")

    
    elif sub_category == "Фильтр":
        st.subheader("Фильтр скважин")
        with st.form(key='filter_form_drill_hole'):
            drill_hole_id = st.number_input("ID скважины", min_value=0, step=1)
            drill_hole = st.text_input("Название скважины")
            geological_complex = st.text_input("Геологический комплекс")
            ore_zone = st.text_input("Рудная зона")
            submitted = st.form_submit_button("Применить фильтр")
        
        if submitted:
            params = {}
            if drill_hole_id:
                params['id'] = drill_hole_id
            if drill_hole:
                params['drill_hole'] = drill_hole
            if geological_complex:
                params['geological_complex'] = geological_complex
            if ore_zone:
                params['ore_zone'] = ore_zone
            with st.spinner("Загрузка отфильтрованных скважин..."):
                data = fetch_data("/drill_hole/by_filter", params=params)
            selected_drill_hole = display_table(data, ["id", "drill_hole", "geological_complex", "ore_zone"], key="drill_holes_filtered")
            
            if selected_drill_hole:
                st.success("Выбранная скважина:")
                st.json(selected_drill_hole)
                
                # Fetch and display related samples
                drill_hole_id = selected_drill_hole.get("id")
                if drill_hole_id:
                    st.subheader(f"Образцы в скважине ID {drill_hole_id}")
                    with st.spinner("Загрузка связанных образцов..."):
                        samples_data = fetch_data(f"/samples/drill_hole/{drill_hole_id}")
                    display_table(samples_data, ["id", "sample_name", "depth_m", "full_name", "texture", "structure", "ore_mineralization"], key=f"samples_in_drill_hole_{drill_hole_id}")

# Samples Section
elif category == "Образцы":
    st.header("Образцы")
    sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр"))
    
    if sub_category == "Показать всё":
        st.subheader("Все образцы")
        with st.spinner("Загрузка всех образцов..."):
            data = fetch_data("/samples/")
        selected_sample = display_table(data, ["id", "sample_name", "drill_hole_id", "depth_m", "full_name", "texture", "structure", "ore_mineralization"], key="samples_all")
        
        if selected_sample:
            st.success("Выбранный образец:")
            st.json(selected_sample)
            
            sample_id = selected_sample.get("id")
            if sample_id:
                # Allow user to choose which related data to load
                st.subheader(f"Связанные данные для образца ID {sample_id}")
                related_data_options = st.multiselect(
                    "Выберите связанные данные для отображения:",
                    ["Photos", "MineralComposition", "OreMineralization", "Vein", "Metasomatite", "RareOreMineralization", "AccessoryMineral"]
                )
                
                for data_option in related_data_options:
                    if data_option == "Photos":
                        st.subheader("Photos")
                        with st.spinner("Loading Photos..."):
                                photos_data = fetch_data("/additional_models/photos/by_filter", params={"sample_id": sample_id})
                                if photos_data:
                                    display_photos(photos_data)  # Use the function from photo_handler.py
                                else:
                                    st.info("No photos available for this sample.")
                    
                    elif data_option == "MineralComposition":
                        st.subheader("Mineral Composition")
                        with st.spinner("Загрузка минералогических составов..."):
                            mineral_comp_data = fetch_data("/additional_models/mineral_composition/by_filter", params={"sample_id": sample_id})
                        display_table(mineral_comp_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"mineral_comp_sample_{sample_id}")
                    
                    elif data_option == "OreMineralization":
                        st.subheader("Ore Mineralization")
                        with st.spinner("Загрузка рудной минерализации..."):
                            ore_min_data = fetch_data("/additional_models/ore_mineralization/by_filter", params={"sample_id": sample_id})
                        display_table(ore_min_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"ore_min_sample_{sample_id}")
                    
                    elif data_option == "Vein":
                        st.subheader("Vein")
                        with st.spinner("Загрузка жил..."):
                            veins_data = fetch_data("/additional_models/vein/by_filter", params={"sample_id": sample_id})
                        display_table(veins_data, ["id", "vein_name", "percentage"], key=f"veins_sample_{sample_id}")
                    
                    elif data_option == "Metasomatite":
                        st.subheader("Metasomatite")
                        with st.spinner("Загрузка метасоматитов..."):
                            metasomatites_data = fetch_data("/additional_models/metasomatite/by_filter", params={"sample_id": sample_id})
                        display_table(metasomatites_data, ["id", "metasomatite_type", "percentage"], key=f"metasomatites_sample_{sample_id}")
                    
                    elif data_option == "RareOreMineralization":
                        st.subheader("Rare Ore Mineralization")
                        with st.spinner("Загрузка редкой рудной минерализации..."):
                            rare_ore_data = fetch_data("/additional_models/rare_ore_mineralization/by_filter", params={"sample_id": sample_id})
                        display_table(rare_ore_data, ["id", "rare_ore_mineral"], key=f"rare_ore_sample_{sample_id}")
                    
                    elif data_option == "AccessoryMineral":
                        st.subheader("Accessory Mineral")
                        with st.spinner("Загрузка вспомогательных минералов..."):
                            accessory_min_data = fetch_data("/additional_models/accessory_mineral/by_filter", params={"sample_id": sample_id})
                        display_table(accessory_min_data, ["id", "accessory_mineral"], key=f"accessory_min_sample_{sample_id}")
    
    elif sub_category == "Фильтр":
        st.subheader("Фильтр образцов")
        with st.form(key='filter_form_sample'):
            sample_id = st.number_input("ID образца", min_value=0, step=1)
            sample_name = st.text_input("Название образца")
            drill_hole_id = st.number_input("ID скважины", min_value=0, step=1)
            depth_m = st.number_input("Глубина (м)", min_value=0.0, step=0.1)
            full_name = st.text_input("Полное название")
            texture = st.text_input("Текстура")
            structure = st.text_input("Структура")
            ore_mineralization = st.text_input("Рудная минерализация")
            submitted = st.form_submit_button("Применить фильтр")
        
        if submitted:
            params = {}
            if sample_id:
                params['id'] = sample_id
            if sample_name:
                params['sample_name'] = sample_name
            if drill_hole_id:
                params['drill_hole_id'] = drill_hole_id
            if depth_m:
                params['depth_m'] = depth_m
            if full_name:
                params['full_name'] = full_name
            if texture:
                params['texture'] = texture
            if structure:
                params['structure'] = structure
            if ore_mineralization:
                params['ore_mineralization'] = ore_mineralization
            with st.spinner("Загрузка отфильтрованных образцов..."):
                data = fetch_data("/samples/by_filter", params=params)
            if isinstance(data, dict) and 'message' in data:
                st.info(data['message'])
            else:
                selected_sample = display_table(data, ["id", "sample_name", "drill_hole_id", "depth_m", "full_name", "texture", "structure", "ore_mineralization"], key="samples_filtered")
                
                if selected_sample:
                    st.success("Выбранный образец:")
                    st.json(selected_sample)
                    
                    sample_id = selected_sample.get("id")
                    if sample_id:
                        # Allow user to choose which related data to load
                        st.subheader(f"Связанные данные для образца ID {sample_id}")
                        related_data_options = st.multiselect(
                            "Выберите связанные данные для отображения:",
                            ["Photos", "MineralComposition", "OreMineralization", "Vein", "Metasomatite", "RareOreMineralization", "AccessoryMineral"]
                        )
                        
                        for data_option in related_data_options:
                            if data_option == "Photos":
                                st.subheader("Photos")
                                with st.spinner("Загрузка фотографий..."):
                                    photos_data = fetch_data("/additional_models/photos/by_filter", params={"sample_id": sample_id})
                                display_table(photos_data, ["id", "macro", "straight_light", "reflected_light"], key=f"photos_sample_{sample_id}")
                            
                            elif data_option == "MineralComposition":
                                st.subheader("Mineral Composition")
                                with st.spinner("Загрузка минералогических составов..."):
                                    mineral_comp_data = fetch_data("/additional_models/mineral_composition/by_filter", params={"sample_id": sample_id})
                                display_table(mineral_comp_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"mineral_comp_sample_{sample_id}")
                            
                            elif data_option == "OreMineralization":
                                st.subheader("Ore Mineralization")
                                with st.spinner("Загрузка рудной минерализации..."):
                                    ore_min_data = fetch_data("/additional_models/ore_mineralization/by_filter", params={"sample_id": sample_id})
                                display_table(ore_min_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"ore_min_sample_{sample_id}")
                            
                            elif data_option == "Vein":
                                st.subheader("Vein")
                                with st.spinner("Загрузка жил..."):
                                    veins_data = fetch_data("/additional_models/vein/by_filter", params={"sample_id": sample_id})
                                display_table(veins_data, ["id", "vein_name", "percentage"], key=f"veins_sample_{sample_id}")
                            
                            elif data_option == "Metasomatite":
                                st.subheader("Metasomatite")
                                with st.spinner("Загрузка метасоматитов..."):
                                    metasomatites_data = fetch_data("/additional_models/metasomatite/by_filter", params={"sample_id": sample_id})
                                display_table(metasomatites_data, ["id", "metasomatite_type", "percentage"], key=f"metasomatites_sample_{sample_id}")
                            
                            elif data_option == "RareOreMineralization":
                                st.subheader("Rare Ore Mineralization")
                                with st.spinner("Загрузка редкой рудной минерализации..."):
                                    rare_ore_data = fetch_data("/additional_models/rare_ore_mineralization/by_filter", params={"sample_id": sample_id})
                                display_table(rare_ore_data, ["id", "rare_ore_mineral"], key=f"rare_ore_sample_{sample_id}")
                            
                            elif data_option == "AccessoryMineral":
                                st.subheader("Accessory Mineral")
                                with st.spinner("Загрузка вспомогательных минералов..."):
                                    accessory_min_data = fetch_data("/additional_models/accessory_mineral/by_filter", params={"sample_id": sample_id})
                                display_table(accessory_min_data, ["id", "accessory_mineral"], key=f"accessory_min_sample_{sample_id}")
