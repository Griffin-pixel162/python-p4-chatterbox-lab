# server/seed.py
from app import app, db
from models import Message
from datetime import datetime, timezone

with app.app_context():
    db.drop_all()
    db.create_all()
    message = Message(
        body="Hello 👋",
        username="Liza",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    db.session.add(message)
    db.session.commit()
    messages = Message.query.all()
    print("Seeded database with messages:", messages)