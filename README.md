To run (for now):

poetry install
docker compose up --build
poetry run uvicorn app.main:app --reload
poetry run streamlit run app/frontend/app.py

for initial database filling:
poetry run app/scripts/load_data.py
poetry run app/scripts/load_photos.py

TODO: everything via docker
