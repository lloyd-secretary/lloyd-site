import os
from app import app, production

# this will really only matter
if not production:
    from OpenSSL import SSL
    context = SSL.Context(SSL.PROTOCOL_TLSv1_2)
    context.use_privatekey_file('/etc/ssl/lloyd.caltech.edu.key')
    context.use_certificate_file('/etc/ssl/lloyd.caltech.edu.crt')

if __name__== '__main__':
    app.run(debug=(not production), threaded=(not production), ssl_context='adhoc' if (not production) else context)