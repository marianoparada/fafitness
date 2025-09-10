import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function ConfigPage() {
  const [tipoRutina, setTipoRutina] = useState('Rápida');
  const [duracion, setDuracion] = useState('30 segundos');
  const [tiempoDescanso, setTiempoDescanso] = useState(10);
  const [vueltas, setVueltas] = useState(3);
  const [musculo, setMusculo] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    const routineConfig = {
      tipo_rutina: tipoRutina,
      duracion: duracion,
      tiempo_descanso: tiempoDescanso,
      vueltas: vueltas,
      musculo: tipoRutina === 'Músculo' ? musculo : null,
    };

    try {
      const response = await fetch('/api/v1/routines', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(routineConfig),
      });

      if (!response.ok) {
        throw new Error('Error al generar la rutina. Inténtalo de nuevo.');
      }

      const routine = await response.json();
      navigate('/workout', { state: { routine, config: routineConfig } });

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4">
      <h1 className="text-3xl font-bold text-yellow-400 mb-8">Configura tu Rutina</h1>
      <form onSubmit={handleSubmit} className="w-full max-w-sm space-y-4">
        <div>
          <label htmlFor="tipo_rutina" className="block mb-2 text-sm font-medium text-gray-300">Tipo de Rutina</label>
          <select id="tipo_rutina" value={tipoRutina} onChange={(e) => setTipoRutina(e.target.value)} className="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block w-full p-2.5">
            <option value="Rápida">Rápida</option>
            <option value="HIIT">HIIT</option>
            <option value="Músculo">Por Músculo</option>
          </select>
        </div>

        {tipoRutina === 'Músculo' && (
          <div>
            <label htmlFor="musculo" className="block mb-2 text-sm font-medium text-gray-300">Grupo Muscular</label>
            <input type="text" id="musculo" value={musculo} onChange={(e) => setMusculo(e.target.value)} required className="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block w-full p-2.5" placeholder="Ej: Brazos, Piernas..." />
          </div>
        )}

        <div>
          <label htmlFor="duracion" className="block mb-2 text-sm font-medium text-gray-300">Duración del Ejercicio</label>
          <select id="duracion" value={duracion} onChange={(e) => setDuracion(e.target.value)} className="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block w-full p-2.5">
            <option value="30 segundos">30 segundos</option>
            <option value="40 segundos">40 segundos</option>
            <option value="Ambos aleatorios">Aleatorio</option>
          </select>
        </div>

        <div>
          <label htmlFor="tiempo_descanso" className="block mb-2 text-sm font-medium text-gray-300">Descanso (segundos)</label>
          <input type="number" id="tiempo_descanso" value={tiempoDescanso} onChange={(e) => setTiempoDescanso(parseInt(e.target.value, 10))} min="5" max="60" step="5" className="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block w-full p-2.5" />
        </div>

        <div>
          <label htmlFor="vueltas" className="block mb-2 text-sm font-medium text-gray-300">Número de Vueltas</label>
          <input type="number" id="vueltas" value={vueltas} onChange={(e) => setVueltas(parseInt(e.target.value, 10))} min="1" max="10" className="bg-gray-700 border border-gray-600 text-white text-sm rounded-lg focus:ring-yellow-500 focus:border-yellow-500 block w-full p-2.5" />
        </div>

        <button type="submit" disabled={isLoading} className="w-full bg-yellow-400 text-black font-bold py-3 px-6 rounded-lg text-lg hover:bg-yellow-300 transition-colors disabled:bg-gray-500">
          {isLoading ? 'Generando...' : 'Crear Rutina'}
        </button>

        {error && <p className="text-red-500 text-sm text-center">{error}</p>}
      </form>
    </div>
  );
}

export default ConfigPage;
