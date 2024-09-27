import React from 'react';
import { List, Datagrid, TextField, DateField } from 'react-admin';
import { Box, Typography } from '@mui/material';

export const ScanHistoryList = () => (
  <Box sx={{ padding: '20px' }}>
    <Typography variant="h1">Scan History</Typography>
    <List>
      <Datagrid rowClick="edit" sx={{
        backgroundColor: '#1e1e1e',
        color: '#00e676',
        '& .RaDatagrid-headerCell': {
          backgroundColor: '#00e676',
          color: '#000000',
        },
        '& .RaDatagrid-row': {
          borderBottom: '1px solid #00e676',
        },
      }}>
        <TextField source="id" label="Scan ID" />
        <TextField source="domain" label="Domain" />
        <DateField source="scan_date" label="Scan Date" />
        <TextField source="status" label="Status" />
        <TextField source="result" label="Result" />
      </Datagrid>
    </List>
  </Box>
);
