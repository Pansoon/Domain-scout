import React, { useState } from 'react';
import {
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Box,
  RadioGroup,
  FormControlLabel,
  Radio,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';

// Simulated scan functions (based on mock data)
const resolveDomainToIP = (domain) => {
  return domain === 'example.com' ? '93.184.216.34' : '192.168.0.1'; // Mock data
};

const scanPorts = (ip) => {
  return { 80: 'open', 443: 'open', 22: 'closed' }; // Mock data
};

const getHTTPStatus = (domain) => {
  return domain === 'example.com' ? '200 OK' : '404 Not Found'; // Mock data
};

// Main ScanForm Component
const ScanForm = () => {
  const [domain, setDomain] = useState('');
  const [scanType, setScanType] = useState('quick');
  const [isLoading, setIsLoading] = useState(false);
  const [scanResults, setScanResults] = useState(null);
  const [reportType, setReportType] = useState('text');
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
    <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', margin: 'auto', borderRadius: '15px', maxWidth: '1000px' }}>
      <CardContent>
        <Grid container spacing={9}>
          {/* Left Column: Form */}
          <Grid item xs={12} md={6}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={3} alignItems="center" justifyContent="center">
                {/* Domain Input Section */}
                <Grid item xs={12} md={8}>
                  <TextField
                    label="Domain Name(s)"
                    variant="outlined"
                    fullWidth
                    value={domain}
                    onChange={(e) => setDomain(e.target.value)}
                    sx={{ backgroundColor: '#31363F', borderRadius: '5px', color: '#ffffff' }}
                    InputLabelProps={{ style: { color: '#18ffff' } }}
                    required
                  />
                </Grid>
                <Grid item xs={12} md={4}>
                  <Button
                    variant="contained"
                    component="label"
                    fullWidth
                    sx={{ backgroundColor: '#1B9CFC', color: '#fff', textAlign: 'center', justifyContent: 'center', display: 'flex' }}
                  >
                    Load from File
                    <input type="file" hidden accept=".txt" onChange={handleLoadFile} />
                  </Button>

                </Grid>

                {/* Scan Type Section */}
                <Grid item xs={12} md={6}>
                  <FormControl fullWidth>
                    <InputLabel sx={{ color: '#18ffff' }}>Scan Type</InputLabel>
                    <Select
                      value={scanType}
                      onChange={(e) => setScanType(e.target.value)}
                      sx={{ backgroundColor: '#31363F', borderRadius: '5px', color: '#ffffff' }}
                      inputProps={{ sx: { color: '#ffffff' } }}
                    >
                      <MenuItem value="quick">Quick Scan</MenuItem>
                      <MenuItem value="detailed">Detailed Scan</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                {/* Report Type Section */}
                <Grid item xs={12} md={6}>
                  <Typography variant="h6" sx={{ color: '#18ffff', marginBottom: '10px' }}>Report Type</Typography>
                  <FormControl component="fieldset">
                    <RadioGroup row value={reportType} onChange={(e) => setReportType(e.target.value)}>
                      <FormControlLabel value="text" control={<Radio sx={{ color: '#18ffff' }} />} label="Text" />
                      <FormControlLabel value="pdf" control={<Radio sx={{ color: '#18ffff' }} />} label="PDF" />
                    </RadioGroup>
                  </FormControl>
                </Grid>

                {/* Action Buttons */}
                <Grid item xs={12} md={6}>
                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    sx={{ backgroundColor: '#00C49F', color: '#fff' }}
                    disabled={isLoading}
                  >
                    {isLoading ? (
                      <>
                        <CircularProgress size={20} sx={{ marginRight: '10px' }} />
                        Scanning...
                      </>
                    ) : (
                      'Start Scan'
                    )}
                  </Button>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Button
                    variant="contained"
                    fullWidth
                    sx={{ backgroundColor: '#FF3333', color: '#fff' }}
                    onClick={handleClearResults}
                  >
                    Clear Results
                  </Button>
                </Grid>
              </Grid>
            </form>

            {/* Help Dialog Trigger */}
            <Box mt={4} textAlign="center">
              <Button variant="contained" color="info" onClick={handleHelpClick}>
                Help
              </Button>
            </Box>

            {/* Help Dialog 54454*/}
            <Dialog open={helpOpen} onClose={handleHelpClose}>
              <DialogTitle>Help</DialogTitle>
              <DialogContent>
                <Typography>
                  Enter one or more domain names, separated by commas.
                </Typography>
                <Typography>
                  You can also load a list of domains from a text file, select the report type, and start a scan.
                </Typography>
              </DialogContent>
              <DialogActions>
                <Button onClick={handleHelpClose} color="primary">Close</Button>
              </DialogActions>
            </Dialog>
          </Grid>

          {/* Right Column: Scan Results (Always visible) */}
          <Grid item xs={12} md={6}>
            <Typography variant="h6" sx={{ color: '#18ffff', marginBottom: '10px' }}>Scan Results</Typography>
            <Box
              sx={{
                padding: '20px',
                backgroundColor: '#31363F',
                borderRadius: '5px',
                height: '250px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                color: '#ffffff',
              }}
            >
              {scanResults ? (
                <>
                  <Typography>Domain: {scanResults.domain}</Typography>
                  <Typography>IP Address: {scanResults.ipAddress}</Typography>
                  <Typography>HTTP Status: {scanResults.httpStatus}</Typography>
                  <Typography>Port Status:</Typography>
                  <ul>
                    {Object.entries(scanResults.portStatus).map(([port, status]) => (
                      <li key={port}>Port {port}: {status}</li>
                    ))}
                  </ul>
                </>
              ) : (
                <Typography>No results yet. Start a scan to see the results here.</Typography>
              )}
            </Box>
          </Grid>
        </Grid>
      </CardContent>
    </Card>
  );
};

export default ScanForm;
