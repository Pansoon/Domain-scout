import React, { useState } from 'react';
import { TextField, Button, Grid, Card, CardContent, Typography, FormControl, InputLabel, Select, MenuItem, CircularProgress, Box, RadioGroup, FormControlLabel, Radio, Dialog, DialogTitle, DialogContent, DialogActions } from '@mui/material';

// Simulated scan functions (based on Code 2 logic)
const resolveDomainToIP = (domain) => {
  return domain === 'example.com' ? '93.184.216.34' : '192.168.0.1'; // Mock data
};

const scanPorts = (ip) => {
  return { 80: 'open', 443: 'open', 22: 'closed' }; // Mock data
};

const getHTTPStatus = (domain) => {
  return domain === 'example.com' ? '200 OK' : '404 Not Found'; // Mock data
};

const loadConfig = () => {
  // Simulate loading a config file
  return { ports: [80, 443, 22], reportType: 'text' };
};

// Main ScanForm Component
const ScanForm = () => {
  const [domain, setDomain] = useState('');
  const [scanType, setScanType] = useState('quick');
  const [isLoading, setIsLoading] = useState(false);
  const [scanResults, setScanResults] = useState(null);
  const [reportType, setReportType] = useState('text');
  const [config, setConfig] = useState(null);
  const [helpOpen, setHelpOpen] = useState(false);

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    setTimeout(() => {
      const ipAddress = resolveDomainToIP(domain);
      const portStatus = scanPorts(ipAddress);
      const httpStatus = getHTTPStatus(domain);

      const results = {
        domain,
        ipAddress,
        portStatus,
        httpStatus,
      };

      setScanResults(results);
      setIsLoading(false);
    }, 2000); // Simulate delay
  };

  // Handle loading domains from a file
  const handleLoadFile = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const fileContents = e.target.result;
        setDomain(fileContents.replace(/\n/g, ', ').trim()); // Replace new lines with commas
      };
      reader.readAsText(file);
    }
  };

  // Handle loading config file
  const handleLoadConfig = () => {
    const loadedConfig = loadConfig();
    setConfig(loadedConfig);
    alert('Config loaded');
  };

  // Handle clearing results
  const handleClearResults = () => {
    setScanResults(null);
    setDomain('');
  };

  // Handle showing help dialog
  const handleHelpClick = () => {
    setHelpOpen(true);
  };

  const handleHelpClose = () => {
    setHelpOpen(false);
  };

  return (
    <Card sx={{
      backgroundColor: '#1e1e1e',
      color: '#ffffff',
      boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
      padding: '20px',
    }}>
      <CardContent>
        <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
          Enter Domain to Scan
        </Typography>
        <form onSubmit={handleSubmit}>
          <Grid container spacing={2}>
            {/* Domain Name Input */}
            <Grid item xs={12}>
              <TextField
                label="Domain Name(s)"
                variant="outlined"
                fullWidth
                value={domain}
                onChange={(e) => setDomain(e.target.value)}
                sx={{ backgroundColor: '#31363F', borderRadius: '5px' }}
                required
              />
            </Grid>

            {/* Load from File Button */}
            <Grid item xs={12}>
              <Button variant="contained" component="label" fullWidth>
                Load from File
                <input
                  type="file"
                  hidden
                  accept=".txt"
                  onChange={handleLoadFile}
                />
              </Button>
            </Grid>

            {/* Report Type Selector */}
            <Grid item xs={12}>
              <FormControl component="fieldset" fullWidth>
                <Typography sx={{ color: '#18ffff', marginBottom: '10px' }}>Report Type</Typography>
                <RadioGroup row value={reportType} onChange={(e) => setReportType(e.target.value)}>
                  <FormControlLabel value="text" control={<Radio />} label="Text" />
                  <FormControlLabel value="pdf" control={<Radio />} label="PDF" />
                </RadioGroup>
              </FormControl>
            </Grid>

            {/* Load Config Button */}
            <Grid item xs={12}>
              <Button variant="contained" onClick={handleLoadConfig} fullWidth>
                Load Config
              </Button>
            </Grid>

            {/* Scan Type Selector */}
            <Grid item xs={12}>
              <FormControl fullWidth>
                <InputLabel id="scan-type-label" sx={{ color: '#18ffff' }}>Scan Type</InputLabel>
                <Select
                  labelId="scan-type-label"
                  id="scan-type"
                  value={scanType}
                  label="Scan Type"
                  onChange={(e) => setScanType(e.target.value)}
                  sx={{ backgroundColor: '#31363F', borderRadius: '5px' }}
                >
                  <MenuItem value="quick">Quick Scan</MenuItem>
                  <MenuItem value="detailed">Detailed Scan</MenuItem>
                </Select>
              </FormControl>
            </Grid>

            {/* Fast Scan and Detailed Scan Buttons */}
            <Grid item xs={6}>
              <Button type="submit" variant="contained" color="primary" fullWidth disabled={isLoading}>
                {isLoading ? 'Scanning...' : 'Fast Scan'}
              </Button>
            </Grid>
            <Grid item xs={6}>
              <Button type="submit" variant="contained" color="secondary" fullWidth disabled={isLoading}>
                {isLoading ? 'Scanning...' : 'Detailed Scan'}
              </Button>
            </Grid>

            {/* Clear Results Button */}
            <Grid item xs={12}>
              <Button variant="contained" color="warning" onClick={handleClearResults} fullWidth>
                Clear Results
              </Button>
            </Grid>

            {/* Help Button */}
            <Grid item xs={12}>
              <Button variant="contained" color="info" onClick={handleHelpClick} fullWidth>
                Help
              </Button>
            </Grid>

          </Grid>
        </form>

        {/* Loading Spinner */}
        {isLoading && (
          <Box display="flex" justifyContent="center" alignItems="center" mt={4}>
            <CircularProgress color="secondary" />
          </Box>
        )}

        {/* Display Scan Results */}
        {scanResults && (
          <Box mt={4}>
            <Typography variant="h6" sx={{ color: '#18ffff' }}>Scan Results:</Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>Domain: {scanResults.domain}</Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>IP Address: {scanResults.ipAddress}</Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>HTTP Status: {scanResults.httpStatus}</Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>Port Status:</Typography>
            <ul>
              {Object.entries(scanResults.portStatus).map(([port, status]) => (
                <li key={port} style={{ color: '#ffffff' }}>Port {port}: {status}</li>
              ))}
            </ul>
          </Box>
        )}

        {/* Help Dialog */}
        <Dialog open={helpOpen} onClose={handleHelpClose}>
          <DialogTitle>Help</DialogTitle>
          <DialogContent>
            <Typography>Enter one or more domain names, separated by commas.</Typography>
            <Typography>You can also load a list of domains from a text file, select the report type, and start a scan.</Typography>
          </DialogContent>
          <DialogActions>
            <Button onClick={handleHelpClose} color="primary">Close</Button>
          </DialogActions>
        </Dialog>
      </CardContent>
    </Card>
  );
};

export default ScanForm;
