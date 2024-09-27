import React, { useState, useEffect, useCallback } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Grid,
  Button,
  LinearProgress,
  Snackbar,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Box
} from '@mui/material';
import DomainIcon from '@mui/icons-material/Domain';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import RefreshIcon from '@mui/icons-material/Refresh';
import { PieChart, Pie, Cell, Tooltip, Legend, BarChart, Bar, XAxis, YAxis, CartesianGrid, ResponsiveContainer } from 'recharts';
import ScanHistoryTable from './components/ScanHistoryTable';
import DomainTrendChart from './components/DomainTrendChart';
import ScanForm from './components/ScanForm';

const httpStatusData = [
  { name: '200 OK', value: 12 },
  { name: '404 Not Found', value: 4 },
  { name: '500 Internal Server Error', value: 2 },
];

const domainStatusData = [
  { name: 'Active', value: 12 },
  { name: 'Closed', value: 5 },
];

const initialErrorLogs = [
  { timestamp: '2024-09-12 14:32:00', message: 'Connection Timeout', level: 'Critical' },
  { timestamp: '2024-09-12 15:05:12', message: 'Failed to resolve domain', level: 'Error' },
];

const COLORS = ['#00C49F', '#FF8042', '#FF3333'];

const Dashboard = () => {
  const [progress, setProgress] = useState(0);
  const [openAlert, setOpenAlert] = useState(false);
  const [errorLogs, setErrorLogs] = useState(initialErrorLogs);
  const [activeDomains, setActiveDomains] = useState(12);
  const [criticalErrors, setCriticalErrors] = useState(2);

  const simulateScan = useCallback(() => {
    setProgress(0);
    const timer = setInterval(() => {
      setProgress((prevProgress) => {
        if (prevProgress >= 100) {
          clearInterval(timer);
          return 100;
        }
        return prevProgress + 10;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    const cleanup = simulateScan();
    return cleanup;
  }, [simulateScan]);

  const triggerErrorAlert = () => {
    setOpenAlert(true);
    setCriticalErrors((prev) => prev + 1);
    setErrorLogs((prev) => [
      { timestamp: new Date().toLocaleString(), message: 'New Critical Error', level: 'Critical' },
      ...prev,
    ]);
  };

  const handleCloseAlert = (event, reason) => {
    if (reason === 'clickaway') {
      return;
    }
    setOpenAlert(false);
  };

  const refreshDashboard = () => {
    setActiveDomains(Math.floor(Math.random() * 20) + 10);
    setCriticalErrors(Math.floor(Math.random() * 5));
    simulateScan();
  };

  return (
    <Grid container spacing={2} sx={{ padding: '20px' }}>
      {/* Welcome Section */}
      <Grid item xs={12}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h2" sx={{ color: '#1B9CFC' }}>
              Welcome to the Cyber Admin Dashboard
            </Typography>
            <Typography variant="body1" sx={{ color: '#ffffff' }}>
              Monitor your system and manage users in a sleek, futuristic interface.
            </Typography>
            <Button variant="contained" color="primary" startIcon={<RefreshIcon />} onClick={refreshDashboard} sx={{ marginTop: '10px' }}>
              Refresh Dashboard
            </Button>
          </CardContent>
        </Card>
      </Grid>

      {/* Domain Scanner Section     656565 */}
      <Grid item xs={12}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff'}}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Domain Scanner
            </Typography>
            <ScanForm />
          </CardContent>
        </Card>
      </Grid>

      {/* Domain Trend Section */}
      <Grid item xs={12}>
        <DomainTrendChart />
      </Grid>

      {/* HTTP Status Distribution (Pie Chart) */}
      <Grid item xs={12} md={6}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              HTTP Status Distribution
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={httpStatusData}
                  cx="50%"
                  cy="50%"
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
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>

      {/* Domain Status Bar Chart (Active vs Closed) */}
      <Grid item xs={12} md={6}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Domain Status (Active vs Closed)
            </Typography>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart
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
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </Grid>

      {/* Error Logs Table */}
      <Grid item xs={12}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
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
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              Scan History
            </Typography>
            <ScanHistoryTable />
          </CardContent>
        </Card>
      </Grid>

      {/* Real-time Error Alert (Snackbar) */}
      <Snackbar open={openAlert} autoHideDuration={6000} onClose={handleCloseAlert}>
        <Alert onClose={handleCloseAlert} severity="error" sx={{ width: '100%' }}>
          Critical: New Error Detected
        </Alert>
      </Snackbar>
    </Grid>
  );
};

export default Dashboard;
