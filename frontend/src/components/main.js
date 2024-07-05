import React, { useState } from 'react';
import axios from 'axios';
import  "../App.css"

function App() {
  const [file, setFile] = useState(null);
  const [userMessage, setUserMessage] = useState('');
  const [chatMessages, setChatMessages] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert('Please select a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:8000/process-document', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setChatMessages([...chatMessages, { sender: 'bot', text: response.data.botResponse }]);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Error uploading file');
    }
  };

  const handleSendMessage = async () => {
    if (!userMessage.trim()) {
      alert('Please enter a message');
      return;
    }

    try {
      const response = await axios.post('http://localhost:8000/process-message', new URLSearchParams({ userMessage }), {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });
      setChatMessages([...chatMessages, { sender: 'user', text: userMessage }, { sender: 'bot', text: response.data.botResponse }]);
      setUserMessage('');
    } catch (error) {
      console.error('Error sending message:', error);
      alert('Error sending message');
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="upload-section">
          <input type="file" accept="application/pdf" onChange={handleFileChange} />
          <br/>
          <button className="upload-button" onClick={handleUpload}>Upload PDF</button>
        </div>
        <div className="chat-messages">
          {chatMessages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <strong>{message.sender === 'user' ? 'You' : 'Bot'}: </strong>
              <span>{message.text}</span>
            </div>
          ))}
        </div>
      </div>
      <div className="input-container">
        <input
          type="text"
          value={userMessage}
          onChange={(e) => setUserMessage(e.target.value)}
          placeholder="Ask a question about the PDF"
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;