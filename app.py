from flask import Flask, jsonify, request, render_template
import pandas as pd
import counts

app = Flask(__name__)

# Load your Excel file here, as before
df = pd.read_excel('last_50_rows.xlsx')
types = df.dtypes.apply(lambda x: x.name).to_dict()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_columns', methods=['GET'])
def get_columns():
    columns = df.columns.tolist()
    return jsonify(columns)

@app.route('/get_unique_values', methods=['POST'])
def get_unique_values():
    column = request.json['column']
    unique_values = df[column].dropna().unique().tolist()
    return jsonify(unique_values)

@app.route('/finalize_selections', methods=['POST'])
def finalize_selections():
    data = request.json
    print("Finalized selections:", data['selections'])
    print("Finalized target column:", data['targetColumn'])
    selections = data['selections']
    for column in selections.keys():
        selections[column] = counts.types_to_ints(types,column,selections[column])
    target = data['targetColumn']
    answers = counts.count_variable(df,target,selections)
    string_keys_dictionary = {str(key): value for key, value in answers.items()}
    return string_keys_dictionary


@app.route('/set_target_column', methods=['POST'])
def set_target_column():
    target_column = request.json['targetColumn']
    # Process the target column as needed, e.g., filter the DataFrame or perform analysis
    return jsonify({'status': 'success', 'targetColumn': target_column})



if __name__ == '__main__':
    app.run(debug=True)
