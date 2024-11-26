# run.py
from dotenv import load_dotenv
load_dotenv()  # This should be before importing create_app()

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
