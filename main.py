from flask import Flask, jsonify
import os
import csv
from datetime import datetime

app = Flask(__name__)

# Check if the data file exists.
if not os.path.exists('data/hn_logs.tsv'):
    raise FileNotFoundError("Data file not found. Please check the 'data/hn_logs.tsv' file.")

# Store the data in a list.
data = []
with open('data/hn_logs.tsv', newline='', encoding='utf-8') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if len(row) == 2:  # Ensure the row has two columns
            try:
                # Convert the timestamp to a datetime object.
                timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                query = row[1]
                data.append((timestamp, query))
            except ValueError:
                # Skip rows with invalid date formats.
                continue

# Cache to store previous query counts
cache = {}

@app.route('/')
def home():
    return "Posteffect.ai Backend Assignment"

# Function to return the number of queries based on the date prefix from the user
@app.route('/queries/count/<date_prefix>', methods=['GET'])
def query_count(date_prefix):
    # Input validation: Ensure that the date prefix is at least 4 characters long.
    if len(date_prefix) < 4:
        return jsonify({'error': 'Invalid date format. Please enter a year or a longer date prefix.'}), 400

    # Check if the result is already in the cache
    if date_prefix in cache:
        return jsonify({'count': cache[date_prefix]})

    # Filtering the data.
    filtered_queries = set()  # Use a set to ensure the uniqueness of queries.
    for timestamp, query in data:
        # Convert the timestamp to a string and check with the prefix.
        if timestamp.strftime('%Y-%m-%d %H:%M:%S').startswith(date_prefix):
            filtered_queries.add(query)

    # Error handling: If no data is found, return a message.
    if not filtered_queries:
        return jsonify({'count': 0, 'message': f'No queries found starting with {date_prefix}.'}), 404

    # Cache the result
    cache[date_prefix] = len(filtered_queries)

    # Return the count of unique queries.
    return jsonify({'count': len(filtered_queries)})

# Start the server.
if __name__ == '__main__':
    app.run(debug=True)
