from attendenceSystem import app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman

# if __name__ == '__main__':
#     app.run(debug=True, host="192.168.1.2")


if __name__ == '__main__':
    app.run(ssl_context='adhoc')