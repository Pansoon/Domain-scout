import React from 'react';
import { Card, CardContent, Typography, Grid, Button } from '@mui/material';
import DomainIcon from '@mui/icons-material/Domain';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';
import CircularProgress from '@mui/material/CircularProgress';
import ScanHistoryTable from './components/ScanHistoryTable';

const Dashboard = () => (
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
          <Button variant="contained" color="secondary" sx={{ marginTop: '10px' }}>
            View Logs
          </Button>
        </CardContent>
      </Card>
    </Grid>

    {/* Loading Progress Section */}
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
            Scanning in Progress
          </Typography>
          <CircularProgress sx={{ color: '#1B9CFC', marginTop: '20px' }} />
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

  </Grid>
);

export default Dashboard;
