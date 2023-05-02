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


Google Authentication Instructions:

To enable google authentication, register the application as a client to google on:
1) https://console.developers.google.com/apis/credentials

2) Select 'Create credentials' > 'OAuth Client ID'

3) Select 'Web Application' and title the client 'Lloyd Website'

4) Set 'Authorized JavaScript origins' to
    https://127.0.0.1:5000
    https://localhost:5000
    https://lloyd.caltech.edu

5) Set 'Authorized redirect URIs' to
    https://127.0.0.1:5000/lloyd/Glogin/callback
    https://localhost:5000/lloyd/Glogin/callback
    https://lloyd.caltech.edu/lloyd/Glogin/callback

6) Hit 'Create' and save the tokens in a file named secrets.py'.
   The file should contain the following fields:
        Google_ID = (enter token from website)
        Google_Client = (enter token from website)
        Google_URL = (enter token from website)

7) DO NOT PUSH secrets.py to github or any public repository. Instead,
   add secrets.py to .gitignore.
