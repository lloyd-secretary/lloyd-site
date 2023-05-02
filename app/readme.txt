Backend/Database instructions (For Linux/Mac. May be different for Windows)

1) cd into root directory (lloyd.caltech.edu)
2) create a virtualenv (google it if u don't know how)
3) run "pip install -r requirements.txt"

( Steps 4 - 7 optional if you aren't using login )
4) Create the sqlite database by running "python db_create.py"
5) To add users, run python.
6) Add users. Example:

>> from app import db
>> from app.models import User
>> user1 = User(username="test", password="pswd")
>> db.session.add(user1)
>> db.session.commit()

Now the user has been added.

7) Examples of queries:

User.query.all()
User.query.filter_by(username="user").first()
User.query.get(id)

8) run "python run.py"
9) Go to "localhost:5000" on your browser. Enjoy :)