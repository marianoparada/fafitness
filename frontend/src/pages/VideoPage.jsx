import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';

function VideoPage() {
  const [video, setVideo] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchVideo = async () => {
      try {
        const response = await fetch('/api/v1/links/random');
        if (!response.ok) {
          throw new Error('Error al cargar el video.');
        }
        const data = await response.json();
        setVideo(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchVideo();
  }, []);

  // Function to extract YouTube video ID from URL
  const getYouTubeId = (url) => {
    try {
      const urlObj = new URL(url);
      if (urlObj.hostname === 'youtu.be') {
        return urlObj.pathname.slice(1);
      }
      return urlObj.searchParams.get('v');
    } catch (e) {
      return null;
    }
  };

  const videoId = video ? getYouTubeId(video.link) : null;

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-black text-white p-4">
      <div className="w-full max-w-2xl">
        <Link to="/" className="text-yellow-400 hover:text-yellow-300 mb-4 inline-block">&larr; Volver al Inicio</Link>

        {isLoading && <p className="text-center">Cargando video...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}

        {video && videoId && (
          <div className="bg-gray-900 p-4 rounded-lg">
            <div className="aspect-w-16 aspect-h-9 mb-4">
              <iframe
                src={`https://www.youtube.com/embed/${videoId}`}
                title={video.comentario}
                frameBorder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowFullScreen
                className="w-full h-full rounded-lg"
              ></iframe>
            </div>
            <h1 className="text-2xl font-bold">{video.comentario}</h1>
            <p className="text-gray-400">por {video.propietario}</p>
          </div>
        )}
      </div>
    </div>
  );
}

export default VideoPage;
