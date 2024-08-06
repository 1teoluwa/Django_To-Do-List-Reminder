# Django To-Do-List-Reminder

The app is a To-Do List needed with a reminder feature using Celery and .

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/django-project.git
```
Next step is to install the requirements.txt
```bash
pip install -r requirements.txt
```
Activate the virtual environment:
```bash
source itevenv/bin/activate
```

Activate the celery on a different terminal using:
```bash
celery -A core worker --loglevel=info
```

Run the app:
```bash
python manage.py runserver
```

