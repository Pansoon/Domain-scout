import React, { useState, useEffect } from 'react';
import { Card, CardContent, Typography, Grid, Button, LinearProgress, Snackbar, Alert, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import DomainIcon from '@mui/icons-material/Domain';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import ScanHistoryTable from './components/ScanHistoryTable';
import ScanForm from './components/ScanForm';  // Import the ScanForm component
import { PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';

// Sample data for HTTP Status Distribution
const httpStatusData = [
  { name: '200 OK', value: 12 },
  { name: '404 Not Found', value: 4 },
  { name: '500 Internal Server Error', value: 2 },
];

// Sample data for Active vs. Closed domains
const domainStatusData = [
  { name: 'Active', value: 12 },
  { name: 'Closed', value: 5 },
];

// Sample error logs data (for error logging table)
const initialErrorLogs = [
  { timestamp: '2024-09-12 14:32:00', message: 'Connection Timeout', level: 'Critical' },
  { timestamp: '2024-09-12 15:05:12', message: 'Failed to resolve domain', level: 'Error' },
];

// Colors for Pie Chart
const COLORS = ['#00C49F', '#FF8042', '#FF3333'];

const Dashboard = () => {
  // State to manage the real-time progress of the scan
  const [progress, setProgress] = useState(0);
  const [openAlert, setOpenAlert] = useState(false);
  const [errorLogs, setErrorLogs] = useState(initialErrorLogs);

  // State for domain scanning form
  const [domainToScan, setDomainToScan] = useState('');
  const [scanType, setScanType] = useState('');

  useEffect(() => {
    // Simulate progress of the scan every second
    const timer = setInterval(() => {
      setProgress((prevProgress) => (prevProgress >= 100 ? 0 : prevProgress + 10));
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  // Trigger a critical error alert
  const triggerErrorAlert = () => {
    setOpenAlert(true);
  };

  // Handle alert close
  const handleCloseAlert = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenAlert(false);
  };

  // Handle form submission and trigger scan
  const handleFormSubmit = ({ domain, scanType }) => {
    setDomainToScan(domain);
    setScanType(scanType);
    console.log(`Starting a ${scanType} scan for ${domain}`);
    // You can add logic here to actually start the scan
  };

  return (
    <Grid container spacing={2} sx={{ padding: '20px' }}>

      {/* Welcome Section */}
      <Grid item xs={12}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h2" sx={{ color: '#1B9CFC' }}>
              Welcome to the Cyber Admin Dashboard
            </Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>
              Monitor your system and manage users in a sleek, futuristic interface.
            </Typography>
          </CardContent>
        </Card>
      </Grid>

      {/* User Input Form for Domain Scanning */}
      <Grid item xs={12}>
        <ScanForm onSubmit={handleFormSubmit} />
      </Grid>

      {/* Active Domains Section */}
      <Grid item xs={6}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(27, 156, 252, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <DomainIcon sx={{ color: '#1B9CFC', fontSize: 50 }} />
            <Typography variant="h4" sx={{ color: '#18ffff' }}>
              Active Domains
            </Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>
              12 Domains Active
            </Typography>
            <Button variant="contained" color="primary" sx={{ marginTop: '10px' }}>
              View Details
            </Button>
          </CardContent>
        </Card>
      </Grid>

      {/* Errors Section */}
      <Grid item xs={6}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(255, 0, 51, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <ErrorOutlineIcon sx={{ color: '#ff0033', fontSize: 50 }} />
            <Typography variant="h4" sx={{ color: '#18ffff' }}>
              Errors Logged
            </Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>
              2 Critical Errors
            </Typography>
            <Button variant="contained" color="secondary" sx={{ marginTop: '10px' }} onClick={triggerErrorAlert}>
              Trigger Error Alert
            </Button>
          </CardContent>
        </Card>
      </Grid>

      {/* Real-time Scan Progress Section */}
      <Grid item xs={12}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff' }}>
              Scan Progress: {progress}%
            </Typography>
            <LinearProgress variant="determinate" value={progress} sx={{ marginTop: '20px', height: '10px', backgroundColor: '#333' }} />
          </CardContent>
        </Card>
      </Grid>

      {/* HTTP Status Distribution (Pie Chart) */}
      <Grid item xs={6}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              HTTP Status Distribution
            </Typography>
            <PieChart width={400} height={400}>
              <Pie
                data={httpStatusData}
                cx={200}
                cy={200}
                innerRadius={60}
                outerRadius={100}
                fill="#8884d8"
                paddingAngle={5}
                dataKey="value"
              >
                {httpStatusData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </CardContent>
        </Card>
      </Grid>

      {/* Domain Status Bar Chart (Active vs Closed) */}
      <Grid item xs={6}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Domain Status (Active vs Closed)
            </Typography>
            <BarChart
              width={500}
              height={300}
              data={domainStatusData}
              margin={{
                top: 20, right: 30, left: 20, bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="value" fill="#1B9CFC" />
            </BarChart>
          </CardContent>
        </Card>
      </Grid>

      {/* Error Logs Table */}
      <Grid item xs={12}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Error Logs
            </Typography>
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
          </CardContent>
        </Card>
      </Grid>

      {/* Scan History Section */}
      <Grid item xs={12}>
        <Card sx={{
          backgroundColor: '#1e1e1e',
          color: '#ffffff',
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',
          padding: '20px',
          textAlign: 'center'
        }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Scan History
            </Typography>
            {/* Insert Scan History Table */}
            <ScanHistoryTable />
          </CardContent>
        </Card>
      </Grid>

      {/* Real-time Error Alert (Snackbar) */}
      <Snackbar open={openAlert} autoHideDuration={6000} onClose={handleCloseAlert}>
        <Alert onClose={handleCloseAlert} severity="error" sx={{ width: '100%' }}>
          Critical: Connection Timeout
        </Alert>
      </Snackbar>

    </Grid>
  );
};

export default Dashboard;
