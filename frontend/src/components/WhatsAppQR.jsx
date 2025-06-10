import { useState, useEffect } from 'react';
import API from '../services/api';

export default function WhatsAppQR() {
  const [qr, setQr] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      API.get('/whatsapp/qr/').then(res => {
        if (res.data.qr) setQr(res.data.qr);
      });
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="qr-container">
      <pre>{qr || 'Generando QR...'}</pre>
      <p>Escanea este código con WhatsApp → Menú → Dispositivos vinculados</p>
    </div>
  );
}