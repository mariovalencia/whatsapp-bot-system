import { useState } from 'react';
import { Button, Modal, Typography, Spin, message } from 'antd';
import API from '../../services/api';

const { Paragraph } = Typography;

export default function ModelEvaluator() {
  const [visible, setVisible] = useState(false);
  const [report, setReport] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchReport = async () => {
    setLoading(true);
    try {
      const res = await API.get('/evaluate/');
      setReport(res.data.report);
      setVisible(true);
    } catch (error) {
      message.error('Error al obtener el reporte del modelo');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button onClick={fetchReport} type="default">
        Evaluar Modelo NLP
      </Button>
      <Modal
        title="Reporte de Evaluación del Modelo"
        open={visible}
        onCancel={() => setVisible(false)}
        footer={null}
        width={800}
      >
        {loading ? (
          <Spin />
        ) : (
          <Paragraph style={{ whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            {report}
          </Paragraph>
        )}
      </Modal>
    </>
  );
}
