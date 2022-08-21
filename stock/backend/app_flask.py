# version: 1.0

import pandas as pd
import numpy as np
from flask import Flask, render_template


def create_flask():
    # start app setting
    app = Flask(__name__)

    @app.route('/score')
    def score_page():
        # file read
        try:
            fileName = "./post_files/TotalScoreList.csv"
            csv_data = pd.read_csv(fileName, dtype={'num_followers': np.int64})
        except:
            # fail to read file
            csv_data = ''
            return render_template('redir.html')
        # data process
        csv_d = csv_data[csv_data["StockNumber"].str.contains(".1d") == True]
        csv_wk = csv_data[csv_data["StockNumber"].str.contains(".1wk") == True]
        csv_mo = csv_data[csv_data["StockNumber"].str.contains(".1mo") == True]
        # data concat
        _pg_tables = [csv_d.to_html() + csv_wk.to_html() + csv_mo.to_html()]
        return render_template('table.html', pg_tables=_pg_tables)

    @app.route('/refresh')
    def refresh_page():
        ## connect api in core_worker ##
        # from core_worker import workhouse
        # workhouse(True, ['TW_my.txt', 'US_my.txt'])
        # return

        ## subprocess.Popen() ##
        try:
            return render_template('refresh.html')
        finally:
            from subprocess import Popen
            Popen(["python3",
                   "./backend/core_worker.py"])  # call without waiting

    # @app.errorhandler(Exception)
    # def error_page(e):
    #     _pg_error = str(e)
    #     return render_template('error.html', pg_error=_pg_error)

    @app.errorhandler(Exception)
    def redir_page(e):
        return render_template('redir.html')

    return app