from flask import Flask, render_template, jsonify
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

# Path to your JSON credentials file
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Function to fetch data from Google Sheets
def fetch_data_from_google_sheets():
    try:
        # Open the Google Spreadsheet by URL
        sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1oSu7qAXOwfhuY6H29BAftbfcmpESlUFaL4hDET5rEnM/edit?gid=607551150#gid=607551150")
        
        # Select the first worksheet
        worksheet = sheet.get_worksheet(0)

        # Extract data from the sheet as a list of lists
        data = worksheet.get_all_values()

        # Manually set the column names, like you did for Excel
        columns = [
            'Project_Name', 'Total_no_file', 
            'Curation_No_of_files_Assigned', 'Curation_No_files_Submitted', 'Curation_Average_time_per_file',
            'Translation_No_of_Files_Assigned', 'Translation_No_of_Files_Submitted', 'Translation_Average_time_per_file',
            'Post_Processing_No_Ep_Assigned', 'Post_Processing_No_Ep_Submitted', 'Post_Processing_Average_time_per_Ep'
        ]

        # Ensure there are enough columns
        if len(data) < 3:
            print("Error: Not enough data rows")
            return []

        # Create DataFrame using the defined columns
        dataframe = pd.DataFrame(data[2:], columns=columns)

        # Cleaning DataFrame by replacing NaNs and 'N/A' with empty strings
        dataframe.fillna('', inplace=True)
        dataframe.replace('N/A', '', inplace=True)

        # Convert to list of dictionaries for JSON response
        project_data = dataframe.to_dict(orient='records')

        return project_data

    except Exception as e:
        print(f"Error fetching data from Google Sheets: {str(e)}")
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    # Fetch data from Google Sheets
    project_data = fetch_data_from_google_sheets()
    return jsonify(project_data)

if __name__ == '__main__':
    app.run(debug=True)
