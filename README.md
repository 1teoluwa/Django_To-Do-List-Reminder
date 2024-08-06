# Django To-Do-List-Reminder

The app is a To-Do List with features like;
- Reminder of task through emails using Celery.
- Group Task; Creating a task for a group
- Chat with Group members

This is achieved through Celery and Web-socket.

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
