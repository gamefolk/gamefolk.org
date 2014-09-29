from gamefolk import app as application, db

if __name__ == '__main__':
    db.create_all()
    application.run(host='0.0.0.0')
