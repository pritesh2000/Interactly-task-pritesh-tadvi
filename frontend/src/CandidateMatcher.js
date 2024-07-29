import React, { useState } from 'react';
import axios from 'axios';

function CandidateMatcher() {
    const [jobDescription, setJobDescription] = useState('');
    const [response, setResponse] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!jobDescription.trim()) {
            alert("Please enter a job description.");
            return;
        }
        setLoading(true);
        try {
            const result = await axios.post('http://localhost:5000/match_candidates', { job_description: jobDescription });
            setResponse(result.data.matched_candidates);
        } catch (error) {
            console.error("Error fetching candidates:", error);
            alert("There was an error fetching candidates. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    const clearResults = () => {
        setResponse([]);
        setJobDescription('');
    };

    return (
        <div>
            <h1>Candidate Matcher</h1>
            <form onSubmit={handleSubmit}>
                <textarea 
                    value={jobDescription} 
                    onChange={(e) => setJobDescription(e.target.value)} 
                    placeholder="Enter job description" 
                />
                <button type="submit" disabled={loading}>
                    {loading ? 'Matching...' : 'Match Candidates'}
                </button>
                <button type="button" onClick={clearResults}>Clear Results</button>
            </form>
            <div>
                <h2>Matched Candidates:</h2>
                {response.map((candidate, index) => (
                    <div key={index} className="candidate-card">
                        <h3>Name: {candidate.name}</h3>
                        <p><strong>Skills:</strong> {candidate.skills}</p>
                        <p><strong>Experience:</strong> {candidate.experience}</p>
                        <p><strong>Contact:</strong> {candidate.contact}</p>
                        <p><strong>Location:</strong> {candidate.location}</p>
                        <hr/>
                        
                    </div>
                ))}
            </div>
        </div>
    );
}

export default CandidateMatcher;
