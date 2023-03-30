import os
from app import app, production

if __name__== '__main__':
    app.run(debug=(not production), threaded=(not production), ssl_context='adhoc' if (not production) else None)
