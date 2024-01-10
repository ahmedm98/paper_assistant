import './App.css';
import React, { useCallback, useEffect, useState } from "react";
import {PaperList,PdfUpload,SearchBar, QuestionBox} from './PaperMethods';


function App() {
    const url = "http://127.0.0.1:8000/"
    const [selectedPaper, setSelectedPaper] = useState(null);

    const [papers, setPapers] = useState([]);
    
    const fetchPapers = useCallback(() => {
        fetch(url+"get_papers")
        .then(response => response.json())
        .then(data => setPapers(data))
        .catch(error => console.error('Error fetching papers:',error))
    },[url]);

    useEffect(() => {
        fetchPapers();
    },[fetchPapers]);

    const handleDeletePaper = async (paper) => {
        fetch(url+"deletepdf", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(paper),
        })
        .then(async response => {
          const data = await response.json();

          if (!response.ok) {
            throw new Error(data.message || 'Failed to delete paper');
          } else {
            alert(`Deletion message: ${data.message}`);
          }
          fetchPapers();  // Refresh the paper list
        })
        .catch(error => console.error('Error deleting paper:', error));
      };


    const handleSearch = (text, k) => {
        fetch(url + "get_top_k", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ text, k }),
        })
        .then(response => response.json())
        .then(data => setPapers(data))
        .catch(error => console.error('Error fetching search results:', error));
      };
    const handleShowSummary = (paper) => {
        setSelectedPaper(paper);
      };
    
    const [answer, setAnswer] = useState("");
    const [isLoading, setIsLoading] = useState(false);

    const handleSubmitQuestion = async (question) => {
      setIsLoading(true); // Start loading
      const payload = { text: question };
      try {
        const response = await fetch("http://127.0.0.1:8000/get_rag", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        const data = await response.json();
        setAnswer(data); // Update the answer state with the response
      } catch (error) {
        console.error('Error submitting question:', error);
        setAnswer(""); // Reset answer in case of error
      }finally {
        setIsLoading(false); // Stop loading regardless of the outcome
      }
    };


    return (
        <div className="app-container">
          <div className="papers-container">
            <h1>APP</h1>
            <PdfUpload onUploadSuccess={fetchPapers} />
            <SearchBar onSearch={handleSearch} onReset={fetchPapers} />
            <PaperList papers={papers} onDelete={handleDeletePaper} onShowSummary={handleShowSummary} />
          </div>
          <div className="summary-container">
            {selectedPaper && <div><h2>Summary of {selectedPaper.name}</h2><p>{selectedPaper.summary}</p></div>}
          </div>
          <div className="question-container">
            <QuestionBox onSubmitQuestion={handleSubmitQuestion} isLoading={isLoading} />

              <h3>Answer:</h3>
              <p>{answer}</p>
          </div>

      </div>
      );
}

export default App;