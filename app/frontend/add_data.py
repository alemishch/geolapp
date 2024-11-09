import streamlit as st
import requests

def add_drill_hole():
    st.header("Добавить новую скважину")
    with st.form("add_drill_hole_form"):
        drill_hole = st.text_input("Название скважины")
        geological_complex = st.text_input("Геологический комплекс")
        ore_zone = st.text_input("Рудная зона")
        submitted = st.form_submit_button("Добавить скважину")
    
    if submitted:
        if not drill_hole.strip():
            st.error("Название скважины обязательно для заполнения.")
        else:
            payload = {
                "drill_hole": drill_hole,
                "geological_complex": geological_complex if geological_complex.strip() else None,
                "ore_zone": ore_zone if ore_zone.strip() else None
            }
            try:
                response = requests.post("http://localhost:8000/drill_hole/add/", json=payload)
                response.raise_for_status()
                st.success("Скважина успешно добавлена!")
            except requests.exceptions.HTTPError as err:
                st.error(f"Ошибка при добавлении скважины: {err.response.json().get('detail', 'Неизвестная ошибка')}")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")


def add_sample():
    st.header("Добавить новый образец")
    with st.form("add_sample_form"):
        sample_name = st.text_input("Название образца")
        drill_hole_id = st.number_input("ID скважины", min_value=1, step=1)
        depth_m = st.number_input("Глубина (м)", min_value=0.0, step=0.1)
        full_name = st.text_input("Полное название")
        texture = st.text_input("Текстура")
        structure = st.text_input("Структура")
        ore_mineralization = st.text_input("Рудная минерализация")
        # Select related data to add
        related_data = st.multiselect(
            "Выберите связанные данные для добавления:",
            ["Рудная минерализация", "Фотографии"]
        )
        uploaded_files = None
        if "Фотографии" in related_data:
            uploaded_files = st.file_uploader("Загрузить фотографии", accept_multiple_files=True, type=["jpg", "jpeg", "png"])
        submitted = st.form_submit_button("Добавить образец")
    
    if submitted:
        # Validate required fields
        if not sample_name.strip():
            st.error("Название образца обязательно для заполнения.")
        elif drill_hole_id <= 0:
            st.error("ID скважины должен быть положительным числом.")
        elif depth_m < 0.0:
            st.error("Глубина должна быть положительным числом.")
        else:
            payload = {
                "sample_name": sample_name,
                "drill_hole_id": drill_hole_id,
                "depth_m": depth_m,
                "full_name": full_name if full_name.strip() else None,
                "texture": texture if texture.strip() else None,
                "structure": structure if structure.strip() else None,
                "ore_mineralization": ore_mineralization if ore_mineralization.strip() else None
            }
            try:
                response = requests.post("http://localhost:8000/samples/add/", json=payload)
                response.raise_for_status()
                sample = response.json()
                st.success("Образец успешно добавлен!")
                
                # Handle related data
                if "Рудная минерализация" in related_data:
                    add_ore_mineralization(sample["id"])
                
                if "Фотографии" in related_data and uploaded_files:
                    add_photos(sample["id"], uploaded_files)
            except requests.exceptions.HTTPError as err:
                st.error(f"Ошибка при добавлении образца: {err.response.json().get('detail', 'Неизвестная ошибка')}")
            except Exception as e:
                st.error(f"Произошла ошибка: {e}")