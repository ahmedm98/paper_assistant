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
  const [selectedFiles, setSelectedFiles] = useState([]);

  const [isUploading, setIsUploading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFiles(Array.from(event.target.files));
  };

  const handleUpload = async () => {
    if (!selectedFiles) {
      alert('Please select files first!');
      return;
    }
    setIsUploading(true); // Start uploading

    for (const file of selectedFiles) {
      const formData = new FormData();
      formData.append('file', file);

      try {
        const response = await fetch('http://localhost:8000/uploadpdf', {
          method: 'POST',
          body: formData,
        });

        if (response.ok) {
          const data = await response.json();
          console.log(`File uploaded successfully. File ID: ${data.id}`);
        } else {
          console.error('Failed to upload file:', file.name);
        }
      } catch (error) {
        console.error('Error uploading file:', error);
      }}
    setIsUploading(false); // End uploading
    onUploadSuccess();



  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} accept="application/pdf" multiple/>
      <button onClick={handleUpload} disabled={isUploading}> Upload PDF</button>
      {isUploading && <div>Processing...</div>} {/* Display when uploading */}
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


