import React, { useState, useEffect } from 'react';
import { useLocation, Link } from 'react-router-dom';

function WorkoutPage() {
  const location = useLocation();
  const { routine, config } = location.state || { routine: [], config: {} };

  const [currentIndex, setCurrentIndex] = useState(0);
  const [isPaused, setIsPaused] = useState(false);
  const [isResting, setIsResting] = useState(false);

  // Combine routine and rests into a single timeline
  const [timeline, setTimeline] = useState([]);

  useEffect(() => {
    if (routine.length > 0) {
      const newTimeline = [];
      routine.forEach((exercise, index) => {
        newTimeline.push({ type: 'exercise', ...exercise });
        if (index < routine.length - 1) {
          newTimeline.push({ type: 'rest', duration: config.tiempo_descanso });
        }
      });
      setTimeline(newTimeline);
    }
  }, [routine, config]);

  const [timeLeft, setTimeLeft] = useState(0);

  useEffect(() => {
    if (timeline.length > 0) {
      setTimeLeft(timeline[currentIndex].duration);
    }
  }, [timeline, currentIndex]);


  useEffect(() => {
    if (isPaused || timeline.length === 0) return;

    if (timeLeft <= 0) {
      if (currentIndex < timeline.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        // Workout finished
      }
      return;
    }

    const intervalId = setInterval(() => {
      setTimeLeft(timeLeft - 1);
    }, 1000);

    return () => clearInterval(intervalId);
  }, [timeLeft, isPaused, currentIndex, timeline]);

  if (timeline.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4">
        <h1 className="text-2xl mb-4">No se ha cargado ninguna rutina.</h1>
        <Link to="/config" className="bg-yellow-400 text-black font-bold py-2 px-4 rounded-lg">
          Configurar Rutina
        </Link>
      </div>
    );
  }

  const currentItem = timeline[currentIndex];

  const isFinished = currentIndex >= timeline.length -1 && timeLeft <= 0;

  if (isFinished) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4 text-center">
        <h1 className="text-4xl font-bold text-yellow-400 mb-4">¡Felicidades!</h1>
        <p className="text-xl mb-8">Has completado tu rutina.</p>
        <Link to="/">
          <button className="bg-yellow-400 text-black font-bold py-3 px-6 rounded-lg text-lg">
            Volver al Inicio
          </button>
        </Link>
      </div>
    );
  }


  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4 text-center">
      {currentItem.type === 'exercise' ? (
        <>
          <h2 className="text-xl text-gray-400">{currentItem.group}</h2>
          <h1 className="text-4xl font-bold my-2">{currentItem.name}</h1>
          <p className="text-md text-gray-300 mb-8 max-w-md">{currentItem.instruction}</p>
        </>
      ) : (
        <>
          <h1 className="text-4xl font-bold my-2 text-yellow-400">Descanso</h1>
          {timeline[currentIndex + 1] && (
            <p className="text-lg text-gray-300 mb-8">Siguiente: {timeline[currentIndex + 1].name}</p>
          )}
        </>
      )}

      <div className="relative w-48 h-48 flex items-center justify-center mb-8">
        <svg className="absolute w-full h-full" viewBox="0 0 100 100">
          <circle className="text-gray-700" strokeWidth="8" stroke="currentColor" fill="transparent" r="45" cx="50" cy="50" />
          <circle
            className="text-yellow-400"
            strokeWidth="8"
            strokeDasharray={2 * Math.PI * 45}
            strokeDashoffset={((currentItem.duration - timeLeft) / currentItem.duration) * (2 * Math.PI * 45)}
            strokeLinecap="round"
            stroke="currentColor"
            fill="transparent"
            r="45"
            cx="50"
            cy="50"
            transform="rotate(-90 50 50)"
          />
        </svg>
        <span className="text-5xl font-bold">{timeLeft}</span>
      </div>

      <div className="flex space-x-4">
        <button onClick={() => setIsPaused(!isPaused)} className="bg-gray-700 text-white font-bold py-3 px-8 rounded-lg text-lg">
          {isPaused ? 'Reanudar' : 'Pausar'}
        </button>
      </div>
    </div>
  );
}

export default WorkoutPage;
