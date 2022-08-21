# version: 0.7

from app_flask import *
from app_dash import *

app = create_flask()
dashapp = create_dash(app)

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8080)
