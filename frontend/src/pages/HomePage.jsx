import React from 'react';
import { Link } from 'react-router-dom';

function HomePage() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4">
      <header className="text-center mb-12">
        <h1 className="text-5xl font-bold text-yellow-400">FA FITNESS</h1>
        <p className="text-lg text-gray-300 mt-2">Tu entrenador personal</p>
      </header>

      <main className="w-full max-w-xs">
        <div className="flex flex-col space-y-4">
          <Link to="/config">
            <button className="w-full bg-yellow-400 text-black font-bold py-4 px-6 rounded-lg text-xl hover:bg-yellow-300 transition-colors">
              Generar Rutina
            </button>
          </Link>
          <Link to="/video">
            <button className="w-full bg-gray-700 text-white font-bold py-4 px-6 rounded-lg text-xl hover:bg-gray-600 transition-colors">
              Entrenar con Video
            </button>
          </Link>
        </div>
      </main>

      <footer className="text-center mt-12 text-gray-500">
        <p>&copy; 2024 FA FITNESS. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
}

export default HomePage;
