# model.py
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import joblib

class Model:
    def __init__(self, model_path, tokenizer_path):
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)

    def generate_response(self, job_description, candidates):
        input_texts = [job_description]
        for candidate in candidates:
            input_texts.append(f"Name: {candidate['name']}, Skills: {candidate['skills']}, Experience: {candidate['experience']}, Projects: {candidate['projects']}, Comments: {candidate['comments']}, Score: {candidate['score']}")
        
        inputs = self.tokenizer(input_texts, return_tensors="pt", truncation=True, padding=True)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        labels = torch.argmax(probabilities, dim=1)

        label_encoder = joblib.load("label_encoder.pkl")
        labels = label_encoder.inverse_transform(labels)
        
        for candidate, label in zip(candidates, labels):
            candidate["category"] = label

        return candidates
