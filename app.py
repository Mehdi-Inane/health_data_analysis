import pandas as pd
from flask import Flask, render_template, request, jsonify


# Assuming the Excel file is 'data.xlsx'
df = pd.read_excel('last_50_rows.xlsx')

app = Flask(__name__)

@app.route('/get_columns', methods=['GET'])
def get_columns():
    columns = df.columns.tolist()
    return jsonify(columns)


@app.route('/get_unique_values', methods=['POST'])
def get_unique_values():
    column = request.json['column']
    unique_values = df[column].unique().tolist()
    return jsonify(unique_values)
