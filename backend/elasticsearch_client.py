# elasticsearch_client.py
from elasticsearch import Elasticsearch, helpers

class ElasticsearchClient:
    def __init__(self):
        self.es = Elasticsearch(
            ['https://localhost:9200'],
            http_auth=('elastic', 'NdRt+g_Cc+PAxT9_9QB2'),  # Replace with your username and password
            verify_certs=False
        )
        if self.es.ping():
            print("Connected to Elasticsearch!")
        else:
            print("Could not connect to Elasticsearch.")

    def generate_candidates_data(self, candidates_df):
        for _, row in candidates_df.iterrows():
            yield {
                "_index": "candidates",
                "_id": row['ID'],
                "_source": {
                    "name": row['Name'],
                    "contact": row['Contact Details'],
                    "location": row['Location'],
                    "skills": row['Job Skills'],
                    "experience": row['Experience'],
                    "projects": row["Projects"],
                    "comments": row["Comments"],
                }
            }

    def index_candidates(self, candidates_df):
        helpers.bulk(self.es, self.generate_candidates_data(candidates_df))

    def retrieve_candidates(self, job_description, top_k=10):
        query = {
            "multi_match": {
                "query": job_description,
                "fields": ["skills^2", "experience", "projects"],
                "fuzziness": "AUTO"
            }
        }
        response = self.es.search(index="candidates", query=query, size=top_k)
        candidates = []
        for hit in response['hits']['hits']:
            candidate_data = hit['_source']
            score = hit['_score']
            candidate_data['score'] = score
            candidates.append(candidate_data)
        return sorted(candidates, key=lambda x: x['score'], reverse=True)
