from flask import Flask, render_template, jsonify
import pandas as pd
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    try:
        # Construct the full path to the Excel file using app.root_path
        file_path = os.path.join(app.root_path, 'static', 'DT.xlsx')

        # Read the Excel file
        dataframe = pd.read_excel(file_path)

        # Remove rows where 'Project_Name' is NaN
        dataframe = dataframe.dropna(subset=['Project_Name'])

        # Replace NaN values with empty strings
        dataframe.fillna('', inplace=True)

        # Rename columns to match the HTML template references
        dataframe.columns = [
            'Project_Name', 'Total_no_file', 
            'Curation_No_of_files_Assigned', 'Curation_No_files_Submitted', 'Curation_Average_time_per_file',
            'Translation_No_of_Files_Assigned', 'Translation_No_of_Files_Submitted', 'Translation_Average_time_per_file',
            'Post_Processing_No_Ep_Assigned', 'Post_Processing_No_Ep_Submitted', 'Post_Processing_Average_time_per_Ep'
        ]

        # Convert the dataframe to a list of dictionaries
        project_data = dataframe.to_dict(orient='records')

        return jsonify(project_data)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify([])  # Return an empty list if there's an error

if __name__ == '__main__':
    app.run(debug=True)

