# version: 0.7

from flask import Flask, render_template
import pandas as pd
import numpy as np


def create_flask():
    # start app setting
    app = Flask(__name__)

    @app.route('/score')
    def score_page():
        # file read
        try:
            fileName = '../post_files/TotalScoreList.csv'
            csv_data = pd.read_csv(fileName, dtype={'num_followers': np.int64})
        except:
            csv_data = ''  # fail to read file
        # data process
        csv_d = csv_data[csv_data["StockNumber"].str.contains(".1d") == True]
        csv_wk = csv_data[csv_data["StockNumber"].str.contains(".1wk") == True]
        csv_mo = csv_data[csv_data["StockNumber"].str.contains(".1mo") == True]
        # data concat
        _pg_tables = [csv_d.to_html() + csv_wk.to_html() + csv_mo.to_html()]
        return render_template('table.html', pg_tables=_pg_tables)

    @app.route('/refresh')
    def refresh_page():
        try:
            return render_template('refresh.html')
        finally:
            from subprocess import Popen
            # call without waiting
            try:
                Popen(["python3", "core_worker.py"])
            except:
                Popen(["python", "core_worker.py"])
        return

    @app.errorhandler(Exception)
    def redir_page(e):
        return render_template('redir.html')

    return app
