To create a virtual environment:
python -m venv venv

To activate the virtual environment:
In the terminal, run venv\scripts\activate

Install the packages:
pip install -r requirements.txt

Package the libraries:
pip freeze > requirements

Running the app:
python manage.py runserver

Regenerate the database ORMs:
python generateORM.py