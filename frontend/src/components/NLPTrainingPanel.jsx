import React, { useState } from 'react';
import { Button, Card, Progress, message } from 'antd';
import api from '../services/api';

const NLPTrainingPanel = () => {
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);

  const trainModel = async () => {
    setLoading(true);
    setProgress(0);
    
    try {
      const { data } = await api.post('/bot/train/');
      message.success(data.status);
      
      // Simular progreso (en producción usar WebSockets)
      const interval = setInterval(() => {
        setProgress(p => {
          if (p >= 100) {
            clearInterval(interval);
            setLoading(false);
            return 100;
          }
          return p + 10;
        });
      }, 500);
      
    } catch (error) {
      message.error('Error al entrenar el modelo');
      setLoading(false);
    }
  };

  return (
    <Card title="Entrenamiento del Modelo NLP" bordered={false}>
      <div style={{ marginBottom: 16 }}>
        <Button 
          type="primary" 
          onClick={trainModel}
          loading={loading}
        >
          Entrenar Modelo
        </Button>
      </div>
      
      {loading && (
        <Progress percent={progress} status="active" />
      )}
      
      <div style={{ marginTop: 16 }}>
        <p>Último entrenamiento: {new Date().toLocaleString()}</p>
        <p>Precisión actual: 85% (estimado)</p>
      </div>
    </Card>
  );
};