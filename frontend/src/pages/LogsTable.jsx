
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const LogsTable = () => {
  const [logs, setLogs] = useState([]);
  const [filteredLogs, setFilteredLogs] = useState([]);
  const [sourceFilter, setSourceFilter] = useState('');
  const [senderFilter, setSenderFilter] = useState('');

  useEffect(() => {
    fetchLogs();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [sourceFilter, senderFilter, logs]);

  const fetchLogs = async () => {
    try {
      const response = await axios.get('/api/logs/');
      setLogs(response.data);
    } catch (error) {
      console.error('Error fetching logs:', error);
    }
  };

  const applyFilters = () => {
    let filtered = logs;
    if (sourceFilter) {
      filtered = filtered.filter(log => log.source.toLowerCase().includes(sourceFilter.toLowerCase()));
    }
    if (senderFilter) {
      filtered = filtered.filter(log => log.sender.toLowerCase().includes(senderFilter.toLowerCase()));
    }
    setFilteredLogs(filtered);
  };

  const exportToCSV = () => {
    const headers = ['ID', 'Source', 'Sender', 'Message', 'Direction', 'Timestamp'];
    const rows = filteredLogs.map(log => [
      log.id,
      log.source,
      log.sender,
      log.message.replace(/\n/g, ' '),
      log.direction,
      log.timestamp
    ]);

    let csvContent = 'data:text/csv;charset=utf-8,';
    csvContent += headers.join(',') + '\n';
    rows.forEach(row => {
      csvContent += row.map(field => `"${String(field).replace(/"/g, '""')}"`).join(',') + '\n';
    });

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'external_message_logs.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <h2>External Message Logs</h2>
      <div style={{ marginBottom: '10px' }}>
        <label>Source: </label>
        <input value={sourceFilter} onChange={e => setSourceFilter(e.target.value)} />
        <label style={{ marginLeft: '10px' }}>Sender: </label>
        <input value={senderFilter} onChange={e => setSenderFilter(e.target.value)} />
        <button onClick={exportToCSV} style={{ marginLeft: '10px' }}>Export CSV</button>
      </div>
      <table border="1" cellPadding="5">
        <thead>
          <tr>
            <th>ID</th>
            <th>Source</th>
            <th>Sender</th>
            <th>Message</th>
            <th>Direction</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          {filteredLogs.map(log => (
            <tr key={log.id}>
              <td>{log.id}</td>
              <td>{log.source}</td>
              <td>{log.sender}</td>
              <td>{log.message}</td>
              <td>{log.direction}</td>
              <td>{log.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LogsTable;
