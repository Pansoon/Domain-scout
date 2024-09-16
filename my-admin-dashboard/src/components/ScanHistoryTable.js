import React from 'react';
import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Button } from '@mui/material';
import ScanHistoryTable from './components/ScanHistoryTable'; // Correct import


const scanData = [
  { domain: 'example.com', lastActive: '2024-09-10', httpStatus: '200 OK', portStatus: '80 Open', status: 'active' },
  { domain: 'example.xyz', lastActive: '2024-09-08', httpStatus: '404 Not Found', portStatus: '80 Closed', status: 'closed' }
];

const ScanHistoryTable = () => (
  <TableContainer component={Paper} sx={{ backgroundColor: '#1e1e1e', color: '#ffffff' }}>
    <Table>
      <TableHead>
        <TableRow>
          <TableCell sx={{ color: '#18ffff' }}>Domain Name</TableCell>
          <TableCell sx={{ color: '#18ffff' }}>Last Active</TableCell>
          <TableCell sx={{ color: '#18ffff' }}>HTTP Status</TableCell>
          <TableCell sx={{ color: '#18ffff' }}>Port Status</TableCell>
          <TableCell sx={{ color: '#18ffff' }}>Status</TableCell>
          <TableCell sx={{ color: '#18ffff' }}>Actions</TableCell>
        </TableRow>
      </TableHead>
      <TableBody>
        {scanData.map((row) => (
          <TableRow key={row.domain}>
            <TableCell sx={{ color: '#ffffff' }}>{row.domain}</TableCell>
            <TableCell sx={{ color: '#ffffff' }}>{row.lastActive}</TableCell>
            <TableCell sx={{ color: '#ffffff' }}>{row.httpStatus}</TableCell>
            <TableCell sx={{ color: '#ffffff' }}>{row.portStatus}</TableCell>
            <TableCell sx={{ color: row.status === 'active' ? '#1B9CFC' : '#ff0033' }}>
              {row.status === 'active' ? 'Active' : 'Closed'}
            </TableCell>
            <TableCell>
              <Button variant="contained" color="primary">View</Button>
              <Button variant="contained" color="secondary" sx={{ marginLeft: '10px' }}>Rescan</Button>
            </TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  </TableContainer>
);
