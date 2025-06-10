import { useState } from 'react';
import { Button, Input, message, Card, Row, Col } from 'antd';
import API from '../../services/api';

const { TextArea } = Input;

export default function IntentTester() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const testIntent = async () => {
    if (!input.trim()) {
      message.warning('Ingresa un mensaje para probar');
      return;
    }

    setLoading(true);
    try {
      const response = await API.post('/ask/', { message: input });
      setResult(response.data);
    } catch (error) {
      message.error('Error al probar el mensaje');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Row gutter={16}>
        <Col span={18}>
          <TextArea
            rows={4}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Escribe un mensaje para probar la intención..."
          />
        </Col>
        <Col span={6}>
          <Button 
            type="primary" 
            onClick={testIntent}
            loading={loading}
            block
            style={{ height: '100%' }}
          >
            Probar Intención
          </Button>
        </Col>
      </Row>

      {result && (
        <Card className="mt-4">
          <div className="space-y-2">
            <p><strong>Intención detectada:</strong> {result.intent || 'No reconocida'}</p>
            <p><strong>Confianza:</strong> {result.confidence ? `${(result.confidence * 100).toFixed(2)}%` : 'N/A'}</p>
            <p><strong>Respuesta:</strong> {result.response}</p>
          </div>
        </Card>
      )}
    </div>
  );
}