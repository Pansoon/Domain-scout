// src/components/ErrorLogTable.js

import React, { useState } from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';

// Sample error logs data
const initialErrorLogs = [
  { timestamp: '2024-09-12 14:32:00', message: 'Connection Timeout', level: 'Critical' },
  { timestamp: '2024-09-12 15:05:12', message: 'Failed to resolve domain', level: 'Error' },
];

const ErrorLogTable = () => {
  const [errorLogs, setErrorLogs] = useState(initialErrorLogs);

  return (
    <TableContainer component={Paper} sx={{ backgroundColor: '#1e1e1e', color: '#ffffff' }}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell sx={{ color: '#18ffff' }}>Timestamp</TableCell>
            <TableCell sx={{ color: '#18ffff' }}>Error Message</TableCell>
            <TableCell sx={{ color: '#18ffff' }}>Error Level</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {errorLogs.map((log, index) => (
            <TableRow key={index}>
              <TableCell sx={{ color: '#ffffff' }}>{log.timestamp}</TableCell>
              <TableCell sx={{ color: '#ffffff' }}>{log.message}</TableCell>
              <TableCell sx={{ color: log.level === 'Critical' ? '#ff0033' : '#ffc107' }}>
                {log.level}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

export default ErrorLogTable;
