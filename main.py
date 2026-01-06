from app import app, db
from app.models import User

with app.app_context():
    db.create_all()

if __name__ == '__main__': # После первого запуска эту строку можно удалить
    app.run(debug=True) # После первого запуска эту строку можно удалить
