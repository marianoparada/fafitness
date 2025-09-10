import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ConfigPage from './pages/ConfigPage';
import WorkoutPage from './pages/WorkoutPage';
import VideoPage from './pages/VideoPage';

function App() {
  return (
    <Router>
      <div className="bg-black text-white min-h-screen">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/config" element={<ConfigPage />} />
          <Route path="/workout" element={<WorkoutPage />} />
          <Route path="/video" element={<VideoPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
