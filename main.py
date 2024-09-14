from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
    return "Posteffect.ai Backend Assignment"

df = pd.read_csv('data/hn_logs.tsv', sep='\t', header=None, names=['timestamp', 'query'])

df['timestamp'] = pd.to_datetime(df['timestamp'])

@app.route('/queries/count/<date_prefix>', methods=['GET'])
def query_count(date_prefix):
    filter_df = df[df['timestamp'].astype(str).str.startswith(date_prefix)]
    if not filter_df.empty:
        dist_queries = filter_df['query'].nunique()
        return jsonify({'count': dist_queries})
    else:
        return jsonify({'count': 0})

if __name__ == '__main__':
    app.run(debug=True)


