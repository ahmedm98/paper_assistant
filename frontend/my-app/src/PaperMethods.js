import React, { useState } from 'react';


function PaperList({ papers, onDelete, onShowSummary }) {
  console.log('Rendering papers:', papers);
  const [selectedPaper, setSelectedPaper] = useState(null);

  const handleRowClick = (paper) => {
    setSelectedPaper(paper);
  };

  const handleDelete = () => {
    if (selectedPaper) {
      onDelete(selectedPaper);
      setSelectedPaper(null); 
    }
  };

  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Your papers</th>
          </tr>
        </thead>
        <tbody>
          {papers.map((paper, index) => (
            <tr key={index} onClick={() => handleRowClick(paper)}>
              <td>{paper.name}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {selectedPaper && (
        <div className="button-container">
          <button onClick={() => onShowSummary(selectedPaper)}> Show Summary {selectedPaper.name} </button>
          <button onClick={() => handleDelete(selectedPaper)}>Delete {selectedPaper.name}</button>
        </div>
      )}
    </div>
  );
}


function PdfUpload({onUploadSuccess}) {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/uploadpdf', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        onUploadSuccess();
        const data = await response.json();
        alert(`File uploaded successfully. File ID: ${data.id}`);
      } else {
        alert('Failed to upload file.');
      }
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept="application/pdf" />
      <button onClick={handleUpload}>Upload PDF</button>
    </div>
  );
}


function SearchBar({ onSearch, onReset }) {
  const [searchText, setSearchText] = useState('');
  const [k, setK] = useState(2); // Default value for k

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(searchText, k);
  };

  return (
    <form onSubmit={handleSubmit} className="search-form">
      <textarea 
        value={searchText} 
        onChange={(e) => setSearchText(e.target.value)} 
        placeholder="Enter search text"
        rows={4}
        className="search-input"
      />
      <input 
        type="number" 
        value={k} 
        onChange={(e) => setK(e.target.value)} 
        min="1"
        className="search-number"
      />
      <div className="search-buttons">

        <button type="submit">Search</button>
        <button type="button" onClick={onReset}>Reset</button> {/* Reset button */}
      </div>

    </form>
  );
}

export {PaperList, PdfUpload, SearchBar};


