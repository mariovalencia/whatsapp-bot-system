import { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic } from 'antd';
import API from '../../services/api';
import IntentList from './IntentList';
import IntentForm from './IntentForm';
import ModelTrainer from './ModelTrainer';
import IntentTester from './IntentTester'; // Lo crearemos nuevo

export default function BotManager() {
  const [intents, setIntents] = useState([]);
  const [trainingStatus, setTrainingStatus] = useState(null);
  const [botStats, setBotStats] = useState(null);

  const refreshIntents = () => {
    API.get('/intents/').then(res => setIntents(res.data));
    API.get('/bot-stats/').then(res => setBotStats(res.data));
  };

  const trainModel = () => {
    setTrainingStatus('Entrenando...');
    API.post('/train-nlp/').then(() => {
      setTrainingStatus('Modelo actualizado');
      refreshIntents();
    });
  };

  useEffect(() => refreshIntents(), []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-6">Administrador del Bot</h1>
      
      {/* Panel de estadísticas */}
      <Row gutter={16} className="mb-6">
        <Col span={6}>
          <Card>
            <Statistic 
              title="Intenciones" 
              value={botStats?.intents_count || 0} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="Frases entrenamiento" 
              value={botStats?.training_phrases || 0} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="Precisión" 
              value={botStats?.accuracy ? `${(botStats.accuracy * 100).toFixed(1)}%` : 'N/A'} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic 
              title="Últ. entrenamiento" 
              value={botStats?.last_trained || 'N/A'} 
            />
          </Card>
        </Col>
      </Row>

      {/* Probador de intenciones */}
      <Card title="Probador de Intenciones" className="mb-6">
        <IntentTester />
      </Card>

      {/* Entrenamiento del modelo */}
      <Card title="Entrenamiento del Modelo" className="mb-6">
        <ModelTrainer 
          status={trainingStatus} 
          onTrain={trainModel} 
        />
      </Card>

      {/* Gestión de intenciones */}
      <Row gutter={16}>
        <Col span={12}>
          <Card title="Añadir Nueva Intención">
            <IntentForm onSuccess={refreshIntents} />
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Lista de Intenciones">
            <IntentList intents={intents} onDelete={refreshIntents} />
          </Card>
        </Col>
      </Row>
    </div>
  );
}