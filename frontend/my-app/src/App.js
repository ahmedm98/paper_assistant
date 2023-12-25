import './App.css';
import React, { useCallback, useEffect, useState } from "react";
import {PaperList,PdfUpload} from './PaperMethods';


function App() {
    const url = "http://127.0.0.1:8000/"

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

    return (
        <div>
          <h1>APP</h1>
          <PdfUpload onUploadSuccess={fetchPapers} />
          <PaperList papers={papers} onDelete={handleDeletePaper} />
        </div>
      );
}

export default App;