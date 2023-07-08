from typing import Tuple
from io import BytesIO

from flask import Flask, send_file, request
from werkzeug.exceptions import HTTPException

from util.managers import StorageManager

sm = StorageManager()

# ---------- init ---------- #

app = Flask(__name__)

# ---------- fn ---------- #


def get_send_file(status: bool, _file: Tuple[bytes, str]):
    res = None

    try:
        if not status:
            raise FileExistsError

        _ctx, _mimetype = _file
        res = send_file(BytesIO(_ctx), mimetype=_mimetype)

    except Exception as e:
        print(e)

    return res


# ---------- Flask ---------- #


@app.route('/', methods=['GET'])
def fn_root():
    return '/'


@app.route('/api', methods=['GET'])
def fn_api():
    return '/api'


## --- date --- ##


@app.route('/api/dates', methods=['GET'])
def fn_dates():

    status, files = sm.get_dates()

    res = {
        'status': status,
        'files': files,
    }

    code = 200
    if not status:
        code = 404
    return res, code


@app.route('/api/date/<date_str>', methods=['GET'])
def fn_date(date_str):

    status, files = sm.get_date(date_str)

    res = {
        'status': status,
        'files': files,
    }

    code = 200
    if not status:
        code = 404
    return res, code


@app.route('/api/date/<date_str>/<csv_str>', methods=['GET'])
def fn_data_csv(date_str, csv_str):

    status, _file = sm.get_csv(date_str, csv_str)

    res = {
        'status': status,
        'files': _file,
    }

    code = 200
    if not status:
        code = 404
    return res, code


## --- symbol --- ##


@app.route('/api/symbols', methods=['GET'])
def fn_symbols():

    status, files = sm.get_symbols()

    res = {
        'status': status,
        'files': files,
    }

    code = 200
    if not status:
        code = 404
    return res, code


@app.route('/api/symbol/<symbol_str>', methods=['GET'])
def fn_symbol(symbol_str):

    _download = request.args.get("download") == '1'
    _overwrite = request.args.get("overwrite") == '1'

    print('download', _download)
    print('overwrite', _overwrite)

    status, files = sm.get_symbol(symbol_str, _download, _overwrite)

    res = get_send_file(status, files)

    if res is None:
        code = 404
        return str(code), code

    return res


## --- file --- ##


@app.route('/api/get_file', methods=['GET'])
def fn_get_file():
    # potential web exploitation

    file_name = request.args.get("file_name")
    print(file_name)

    status, _files = sm.get_file(file_name)

    res = get_send_file(status, _files)

    if res is None:
        code = 404
        return str(code), code

    return res


# ---------- errorhandler ---------- #


@app.errorhandler(Exception)
def handle_error(e):
    code = ''
    if isinstance(e, HTTPException):
        print('handle_error', e)
        code = e.code
    return str(code), code


# ---------- main ---------- #


def main():
    app.run(debug=False, host='0.0.0.0', port=5000)
    return


if __name__ == '__main__':
    print('server init')
    main()
