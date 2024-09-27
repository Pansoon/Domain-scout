// src/components/RealTimeAlert.js

import React, { useState } from 'react';
import { Snackbar, Alert } from '@mui/material';

// Sample error data that could trigger a real-time alert
const sampleError = {
  message: 'Critical: Connection Timeout',
  level: 'Critical',
};

const RealTimeAlert = () => {
  const [open, setOpen] = useState(false);

  // Simulate triggering an alert for a critical error
  const handleCriticalError = () => {
    if (sampleError.level === 'Critical') {
      setOpen(true);
    }
  };

  const handleClose = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpen(false);
  };

  return (
    <div>
      {/* Simulate an event triggering a critical error */}
      <button onClick={handleCriticalError}>Trigger Critical Error</button>

      <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
          {sampleError.message}
        </Alert>
      </Snackbar>
    </div>
  );
};

export default RealTimeAlert;
