import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form, Input, message } from 'antd';
import api from '../../services/api';

const IntentManager = () => {
  const [intents, setIntents] = useState([]);
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    fetchIntents();
  }, []);

  const fetchIntents = async () => {
    try {
      const response = await api.get('/bot_management/intents/');
      setIntents(response.data);
    } catch (error) {
      message.error('Error al cargar intenciones');
    }
  };

  const handleSubmit = async (values) => {
    try {
      await api.post('/bot_management/intents/upsert/', values);
      message.success('Intención guardada correctamente');
      fetchIntents();
      setIsModalVisible(false);
      form.resetFields();
    } catch (error) {
      message.error('Error al guardar la intención');
    }
  };

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Frases de Entrenamiento',
      dataIndex: 'training_phrases',
      key: 'training_phrases',
      render: phrases => phrases.join(', '),
    },
    {
      title: 'Acciones',
      key: 'actions',
      render: (_, record) => (
        <Button type="link" onClick={() => {
          form.setFieldsValue(record);
          setIsModalVisible(true);
        }}>
          Editar
        </Button>
      ),
    },
  ];

  return (
    <div>
      <Button type="primary" onClick={() => setIsModalVisible(true)}>
        Nueva Intención
      </Button>
      
      <Table 
        columns={columns} 
        dataSource={intents} 
        rowKey="id" 
      />
      
      <Modal
        title="Gestionar Intención"
        visible={isModalVisible}
        onCancel={() => {
          setIsModalVisible(false);
          form.resetFields();
        }}
        onOk={() => form.submit()}
      >
        <Form form={form} onFinish={handleSubmit}>
          <Form.Item name="id" hidden>
            <Input />
          </Form.Item>
          <Form.Item
            name="name"
            label="Nombre"
            rules={[{ required: true }]}
          >
            <Input />
          </Form.Item>
          <Form.Item
            name="training_phrases"
            label="Frases de Entrenamiento"
          >
            <Input.TextArea 
              placeholder="Ingresa frases separadas por comas" 
              autoSize={{ minRows: 3, maxRows: 6 }}
            />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default IntentManager;