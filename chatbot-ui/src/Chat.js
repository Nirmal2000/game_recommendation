// Chat.js
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';

const socket = io('http://127.0.0.1:5000'); // Adjust the URL to match your Flask server

const Chat = () => {
  const [message, setMessage] = useState('');
  const [chatHistory, setChatHistory] = useState([]);

  useEffect(() => {
    const handleAnswer = (data) => {
      setChatHistory((prevHistory) => [...prevHistory, { message: data.answer, sender: 'bot' }]);
    };
  
    socket.on('answer', handleAnswer);
  
    return () => {
      socket.off('answer', handleAnswer);
    };
  }, []);

  const sendMessage = () => {
    socket.emit('ask_question', { question: message });
    setChatHistory((prevHistory) => [...prevHistory, { message, sender: 'user' }]);
    setMessage('');
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((chat, index) => (
          <div key={index} className={`chat-message ${chat.sender}`}>
            {chat.message}
          </div>
        ))}
      </div>
      <div className="chat-input">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
        />
        <button onClick={sendMessage}>Send</button>
      </div>
    </div>
  );
};

export default Chat;
