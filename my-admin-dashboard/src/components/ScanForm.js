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
import axios from 'axios';

export default function DomainScanner() {
  const [domain, setDomain] = useState('');
  const [scanType, setScanType] = useState('quick');
  const [isLoading, setIsLoading] = useState(false);
  const [scanResults, setScanResults] = useState(null);
  const [reportType, setReportType] = useState('text');
  const [autoScanInterval, setAutoScanInterval] = useState(1);
  const [helpOpen, setHelpOpen] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Make a POST request to the Flask API to run the Python script with the domain
      const response = await axios.post('http://127.0.0.1:5000/run-python', {
        domains: domain.split(',').map(d => d.trim()), // Send the input domains as an array
        scanType: scanType, 
        reportType: reportType, 
        //autoScanInterval: autoScanInterval,
      });
      
      // Assuming the response contains the aggregated results from aggregation.py
      const results = response.data;
  
      // Store the results
      setScanResults({
        // Adjust how you store results based on the response structure
        domain: results.domain,
        ipAddress: results.ipAddress,
        httpStatus: results.httpStatus,
        portStatus: results.portStatus,
      });
    } catch (error) {
      console.error('Error running Python script:', error);
      alert('Error running scan. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  


  const handleLoadFile = (event) => {
    const file = event.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const fileContents = e.target?.result;
        if (typeof fileContents === 'string') {
          setDomain(fileContents.replace(/\n/g, ', ').trim());
        }
      };
      reader.readAsText(file);
    }
  };

  const handleClearResults = () => {
    setScanResults(null);
    setDomain('');
  };

  const handleHelpClick = () => setHelpOpen(true);
  const handleHelpClose = () => setHelpOpen(false);

  return (
    <Card
      sx={{
        maxWidth: '1200px',
        margin: 'auto',
        backgroundColor: '#1e1e1e',
        padding: 3,
        borderRadius: 2,
        color: '#ffffff',
        boxShadow: 'none',
        border: 'none',
      }}
    >
      <CardContent>
        <Typography variant="h5" gutterBottom sx={{ textAlign: 'center', fontWeight: 'bold', color: '#18ffff' }}>
          Domain Scanner
        </Typography>

        <Grid container spacing={4}>
          {/* Left Column */}
          <Grid item xs={12} md={6}>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={3}>
                <Grid item xs={12}>
                  <Grid container spacing={2} alignItems="flex-end">
                    <Grid item xs={8}>
                      <TextField
                        label="Domain Name(s)"
                        variant="outlined"
                        fullWidth
                        value={domain}
                        onChange={(e) => setDomain(e.target.value)}
                        sx={{
                          backgroundColor: '#2e2e2e',
                          borderRadius: 1,
                          '& .MuiOutlinedInput-root': {
                            height: '48px',
                          },
                        }}
                        InputLabelProps={{
                          style: { color: '#18ffff' },
                        }}
                        InputProps={{
                          style: { color: '#ffffff' },
                        }}
                        required
                      />
                    </Grid>
                    <Grid item xs={4} justifyContent="center">
                      <Button
                        variant="contained"
                        component="label"
                        fullWidth
                        sx={{
                          backgroundColor: '#00C49F',
                          color: '#ffffff',
                          height: '48px',
                          maxWidth: '300px', // Optional: limit button width
                          textAlign: 'center', // Center the text horizontally
                          justifyContent: 'center', // Ensure content is centered
                        }}
                      >
                        Load from File
                        <input type="file" hidden accept=".txt" onChange={handleLoadFile} />
                      </Button>

                    </Grid>
                  </Grid>
                </Grid>

                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel sx={{ color: '#18ffff' }}>Scan Type</InputLabel>
                    <Select
                      value={scanType}
                      onChange={(e) => setScanType(e.target.value)}
                      sx={{
                        backgroundColor: '#2e2e2e',
                        borderRadius: 1,
                        color: '#ffffff',
                        height: '48px',
                      }}
                      inputProps={{
                        sx: { color: '#ffffff', height: '48px' },
                      }}
                    >
                      <MenuItem value="quick">Quick Scan</MenuItem>
                      <MenuItem value="detailed">Detailed Scan</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>

                <Grid item xs={12}>
                  <Typography variant="subtitle1" gutterBottom sx={{ color: '#18ffff' }}>
                    Report Type
                  </Typography>
                  <RadioGroup
                    row
                    value={reportType}
                    onChange={(e) => setReportType(e.target.value)}
                  >
                    <FormControlLabel
                      value="text"
                      control={<Radio sx={{ color: '#18ffff' }} />}
                      label="Text"
                      sx={{ color: '#ffffff' }}
                    />
                    <FormControlLabel
                      value="pdf"
                      control={<Radio sx={{ color: '#18ffff' }} />}
                      label="PDF"
                      sx={{ color: '#ffffff' }}
                    />
                  </RadioGroup>
                </Grid>

                <Grid item xs={12}>
                  <FormControl fullWidth>
                    <InputLabel sx={{ color: '#18ffff' }}>Select Auto Scan Interval (hours)</InputLabel>
                    <Select
                      value={autoScanInterval}
                      onChange={(e) => setAutoScanInterval(Number(e.target.value))}
                      sx={{
                        backgroundColor: '#31363F',
                        borderRadius: '5px',
                        color: '#ffffff',
                        height: '48px'
                      }}
                      inputProps={{
                        sx: {
                          color: '#ffffff',
                          height: '48px'
                        }
                      }}
                    >
                      {Array.from({ length: 24 }, (_, i) => i + 1).map((hour) => (
                        <MenuItem key={hour} value={hour}>
                          {hour} hour{hour > 1 ? 's' : ''}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                  <Typography sx={{ marginTop: 2, color: '#ffffff' }}>
                    Selected Interval: {autoScanInterval} hour(s)
                  </Typography>
                </Grid>

                <Grid item xs={12} md={6}>
                  <Button
                    type="submit"
                    variant="contained"
                    fullWidth
                    sx={{
                      backgroundColor: '#00C49F',
                      color: '#fff',
                      height: '48px'
                    }}
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
                    sx={{
                      backgroundColor: '#FF3333',
                      color: '#fff',
                      height: '48px'
                    }}
                    onClick={handleClearResults}
                  >
                    Clear Results
                  </Button>
                </Grid>
              </Grid>
            </form>
          </Grid>

          {/* Right Column */}
          <Grid item xs={12} md={6}>
            <Typography variant="h6" gutterBottom sx={{ color: '#18ffff' }}>
              Scan Results
            </Typography>
            <Box
              sx={{
                padding: 2,
                backgroundColor: '#2e2e2e',
                borderRadius: 1,
                minHeight: '400px',
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
                <Typography>No results yet. Start a scan to see the results.</Typography>
              )}
            </Box>
          </Grid>
        </Grid>
      </CardContent>

      <Dialog open={helpOpen} onClose={handleHelpClose}>
        <DialogTitle sx={{ color: '#18ffff' }}>Help</DialogTitle>
        <DialogContent>
          <Typography variant="body1" sx={{ color: '#ffffff' }}>
            Enter the domain name(s) you want to scan. You can load domain names from a text file as well. Choose the scan type and report format before starting the scan.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleHelpClose} sx={{ color: '#18ffff' }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Card>
  );
}