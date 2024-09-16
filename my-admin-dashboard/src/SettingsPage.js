import React from 'react';
import { Card, CardContent, Typography, Button, TextField } from '@mui/material';

const SettingsPage = () => (
  <Card sx={{
    backgroundColor: '#1e1e1e',
    color: '#00e676',
    padding: '20px',
    textAlign: 'center'
  }}>
    <CardContent>
      <Typography variant="h2">Settings</Typography>
      <TextField label="API URL" variant="outlined" sx={{ mt: 2, width: '100%' }} />
      <TextField label="Scan Interval" variant="outlined" sx={{ mt: 2, width: '100%' }} />
      <Button variant="contained" sx={{ mt: 2 }}>Save Settings</Button>
    </CardContent>
  </Card>
);

export default SettingsPage;
