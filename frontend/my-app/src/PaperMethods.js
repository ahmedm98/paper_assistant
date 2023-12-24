import React, { useState } from 'react';


function PaperList({ papers, onDelete }) {
  console.log('Rendering papers:', papers);
  const [selectedPaper, setSelectedPaper] = useState(null);

  const handleRowClick = (paperName) => {
    setSelectedPaper(paperName);
  };

  const handleDelete = () => {
    if (selectedPaper) {
      onDelete(selectedPaper);
      setSelectedPaper(null); 
    }
  };

  return (
    <div>
      <table>
        <thead>
          <tr>
            <th>Paper Name</th>
          </tr>
        </thead>
        <tbody>
          {papers.map((paper, index) => (
            <tr key={index} onClick={() => handleRowClick(paper)}>
              <td>{paper}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {selectedPaper && (
        <div>
          <button onClick={handleDelete}>Delete {selectedPaper}</button>
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


export {PaperList, PdfUpload};


