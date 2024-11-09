import streamlit as st
import requests
from typing import List
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from st_aggrid.shared import JsCode
from photo_handler import display_photos
from add_data import add_drill_hole, add_sample


API_BASE_URL = "http://localhost:8000"


st.set_page_config(
	page_title="Работа с геологическими образцами",
	layout="wide",
	initial_sidebar_state="expanded"
)


st.title("Работа с геологическими образцами")

navigation = st.sidebar.radio("Меню", ["Главная", "Скважины", "Образцы"])

st.markdown(
	"""
	<style>
	.stApp {
		background-color: #f0f2f6;
	}
	.sidebar .sidebar-content {
		background-image: linear-gradient(#4B8BBE, #306998);
		color: white;
	}
	h1, h2, h3, h4, h5, h6 {
		color: #306998;
	}
	</style>
	""",
	unsafe_allow_html=True
)

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
	if "error" in data and data["error"]:
		st.info(data["message"])
		return None
	if not (isinstance(data, list) or isinstance(data, dict)):
		st.error("Неверный формат данных")
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

if navigation == "Главная":
	st.markdown(
		"""
		<h1 style='text-align: center; color: #4B8BBE;'>Добро пожаловать в Геологическую Базу Данных!</h1>
		<p style='text-align: center;'>Используйте боковую панель для навигации по разделам "Скважины" и "Образцы".</p>
		""",
		unsafe_allow_html=True
	)

elif navigation == "Скважины":
	st.header("Скважины")
	sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр", "Добавить скважину"))
	
	if sub_category == "Показать всё":
		st.subheader("Все скважины")
		with st.spinner("Загрузка всех скважин..."):
			data = fetch_data("/drill_hole/")

		selected_drill_hole = display_table(data, ["id", "drill_hole", "geological_complex", "ore_zone"], key="drill_holes_all")
		
		if selected_drill_hole:
			drill_hole_id = selected_drill_hole.get("id")
			drill_hole_name = selected_drill_hole.get("drill_hole")
			if drill_hole_id is not None:
				st.subheader(f"Образцы в скважине {drill_hole_name}")
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

	elif sub_category == "Добавить скважину":
		add_drill_hole()


# Samples Section
elif navigation == "Образцы":
	st.header("Образцы")
	sub_category = st.selectbox("Выберите действие:", ("Показать всё", "Фильтр", "Добавить образец"))

	if sub_category == "Показать всё":
		st.subheader("Все образцы")
		with st.spinner("Загрузка всех образцов..."):
			data = fetch_data("/samples/")

		selected_sample = display_table(data, ["id", "sample_name", "drill_hole_id", "depth_m", "full_name", "texture", "structure", "ore_mineralization"], key="samples_all")

		if selected_sample:
			sample_name = selected_sample.get("sample_name")
			sample_id = selected_sample.get("id")

			if sample_id:
				st.subheader(f"Связанные данные для образца {sample_name}")
				related_data_options = st.multiselect(
					"Выберите связанные данные для отображения:",
					["Фото", "Минеральный состав", "Рудная минерализация"]
				)
				
				for data_option in related_data_options:
					if data_option == "Фото":
						st.subheader("Фото")
						with st.spinner("Загрузка Фото..."):
							photos_data = fetch_data("/additional_models/photos/by_filter", params={"sample_id": sample_id})
							if photos_data:
								display_photos(photos_data)
							else:
								st.info("Нет фото для образца")
					
					elif data_option == "Минеральный состав":
						st.subheader("Минеральный состав")
						with st.spinner("Загрузка данных..."):
							mineral_comp_data = fetch_data("/additional_models/mineral_composition/by_filter", params={"sample_id": sample_id})
							accessory_min_data = fetch_data("/additional_models/accessory_mineral/by_filter", params={"sample_id": sample_id})
							veins_data = fetch_data("/additional_models/vein/by_filter", params={"sample_id": sample_id})
						
						#mineral_comp_data = sorted(mineral_comp_data, key=lambda x: x['percentage'], reverse=True)
						
						# Display tables side-by-side
						col1, col2, col3 = st.columns(3)
						with col1:
							st.write("Минералы")
							display_table(mineral_comp_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"mineral_comp_sample_{sample_id}")
						with col2:
							st.write("Акцессорные")
							display_table(accessory_min_data, ["id", "accessory_mineral"], key=f"accessory_min_sample_{sample_id}")
						with col3:
							st.write("Прожилки")
							display_table(veins_data, ["id", "vein_name", "percentage"], key=f"veins_sample_{sample_id}")
						
						
						#NO DATA YET
						#elif data_option == "Метасоматиты":
						#	st.subheader("Метасоматиты")
						#	with st.spinner("Загрузка метасоматитов..."):
						#		metasomatites_data = fetch_data("/additional_models/metasomatite/by_filter", params={"sample_id": sample_id})
						#	if metasomatites_data is not None:
						#		metasomatites_data = sorted(metasomatites_data, key=lambda x: x['percentage'], reverse=True)
						#	display_table(metasomatites_data, ["id", "metasomatite_type", "percentage"], key=f"metasomatites_sample_{sample_id}")
						
					elif data_option == "Рудная минерализация":
						st.subheader("Рудная минерализация")
						with st.spinner("Загрузка данных..."):
							ore_min_data = fetch_data("/additional_models/ore_mineralization/by_filter", params={"sample_id": sample_id})
							rare_ore_data = fetch_data("/additional_models/rare_ore_mineralization/by_filter", params={"sample_id": sample_id})
						
						# Display tables side-by-side
						col1, col2 = st.columns(2)
						with col1:
							display_table(ore_min_data, ["id", "mineral_name", "percentage", "main_secondary"], key=f"ore_min_sample_{sample_id}")
						with col2:
							display_table(rare_ore_data, ["id", "rare_ore_mineral"], key=f"rare_ore_sample_{sample_id}")

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

	elif sub_category == "Добавить образец":
		add_sample()