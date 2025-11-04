import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <div className="min-h-screen app-bg text-gray-100 font-sans">
      <App />
    </div>
  </React.StrictMode>,
)

