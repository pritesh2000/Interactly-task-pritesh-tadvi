# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS  
import pandas as pd
from elasticsearch_client import ElasticsearchClient
from model import Model

app = Flask(__name__)
CORS(app)

# Load the candidate data
candidates_df = pd.read_csv('rag_data.csv')
candidates_df["ID"] = range(len(candidates_df))

# Initialize Elasticsearch client and model
es_client = ElasticsearchClient()
es_client.index_candidates(candidates_df)  # Index candidates on startup
model = Model('./fine_tuned_model', './fine_tuned_model')

@app.route('/match_candidates', methods=['POST'])
def match_candidates():
    data = request.json
    job_description = data.get('job_description', '')

    # Step 1: Retrieve candidates
    retrieved_candidates = es_client.retrieve_candidates(job_description)
    
    # Step 2: Generate response
    response = model.generate_response(job_description, retrieved_candidates)
    
    return jsonify({"matched_candidates": response})

if __name__ == "__main__":
    app.run(debug=True)
