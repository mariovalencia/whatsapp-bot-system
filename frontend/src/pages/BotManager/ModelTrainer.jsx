import { useState, useEffect } from 'react';
import { Button, message, Spin } from 'antd';
import API from '../../services/api';

export default function ModelTrainer({ status, onTrain }) {
  const [taskId, setTaskId] = useState(null);
  const [taskStatus, setTaskStatus] = useState(null);
  const [loading, setLoading] = useState(false);

  const startTraining = async () => {
    setLoading(true);
    try {
      const res = await API.post('/train/');
      setTaskId(res.data.task_id);
      setTaskStatus('PENDING');
      message.info('🚀 Entrenamiento iniciado...');
    } catch (error) {
      message.error('❌ Error al iniciar entrenamiento');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (!taskId) return;

    const interval = setInterval(async () => {
      try {
        const res = await API.get(`/task-status/${taskId}/`);
        setTaskStatus(res.data.status);

        if (res.data.status === 'SUCCESS') {
          clearInterval(interval);
          const result = res.data.result;
          if (result?.status === 'warning') {
            message.warning(`⚠️ Entrenamiento finalizado con advertencias: ${result.message}`);
          } else {
            message.success(`✅ Entrenamiento exitoso: ${result.message}`);
          }
        }

        if (res.data.status === 'FAILURE') {
          clearInterval(interval);
          message.error('❌ El entrenamiento falló. Revisa los logs del backend.');
        }
      } catch {
        clearInterval(interval);
        message.error('❌ Error al consultar estado de la tarea');
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [taskId]);

  return (
    <div className="my-4 p-4 bg-gray-100 rounded">
      <Button
        onClick={startTraining}
        className="bg-blue-500 text-white px-4 py-2 rounded mr-4"
        loading={loading}
      >
        Entrenar Modelo NLP
      </Button>

      {taskStatus && (
        <p className="mt-2">
          Estado de la tarea: <strong>{taskStatus}</strong>
        </p>
      )}
    </div>
  );
}
