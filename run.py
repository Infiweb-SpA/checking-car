from app import create_app, db

app = create_app()

# Esto crea las tablas en la base de datos la primera vez que lo corres
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)