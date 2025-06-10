import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message, Select, Tag, Switch } from 'antd';
import API from '../../services/api';

const { TextArea } = Input;

const ResponseManager = ({ intentId }) => {
  const [responses, setResponses] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  const fetchResponses = async () => {
    try {
      const response = await API.get('/responses/', { params: { intent_id: intentId } });
      setResponses(response.data);
    } catch (error) {
      message.error('Error al cargar respuestas');
    }
  };

  const handleSubmit = async (values) => {
    try {
      values.intent = intentId;
      if (values.conditions) {
        try {
          values.conditions = JSON.parse(values.conditions);
        } catch {
          values.conditions = null;
        }
      }
      await API.post('/responses/', values);
      message.success('Respuesta guardada');
      fetchResponses();
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      message.error('Error al guardar');
    }
  };

  const setAsDefault = async (responseId) => {
    try {
      await API.patch(`/intents/${intentId}/set-default-response/`, { response_id: responseId });
      message.success('Respuesta por defecto actualizada');
      fetchResponses();
    } catch (error) {
      message.error('Error al actualizar');
    }
  };

  const columns = [
    {
      title: 'Texto',
      dataIndex: 'text',
      key: 'text',
      render: (text, record) => (
        <div>
          {text} {record.is_default && <Tag color="green">Default</Tag>}
        </div>
      ),
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_, record) => (
        <Switch
          checked={record.is_default}
          onChange={() => setAsDefault(record.id)}
          disabled={record.is_default}
        />
      ),
    },
  ];

  useEffect(() => fetchResponses(), [intentId]);

  return (
    <div>
      <Button type="primary" onClick={() => setIsModalVisible(true)} className="mb-4">
        Añadir Respuesta
      </Button>

      <Table
        columns={columns}
        dataSource={responses}
        rowKey="id"
      />

      <Modal
        title="Nueva Respuesta"
        visible={isModalVisible}
        onCancel={() => setIsModalVisible(false)}
        onOk={() => form.submit()}
      >
        <Form form={form} onFinish={handleSubmit}>
          <Form.Item name="text" label="Texto" rules={[{ required: true }]}>
            <TextArea rows={3} />
          </Form.Item>
          <Form.Item name="conditions" label="Condiciones (JSON)">
            <Input placeholder='Ej: {"context_key": "value"}' />
          </Form.Item>
          <Form.Item name="is_default" label="Por defecto" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default ResponseManager;