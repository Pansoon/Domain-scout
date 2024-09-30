import React from 'react';
import { Grid, Card, CardContent, Typography } from '@mui/material';
import { PieChart, Pie, Tooltip, Legend, Cell, ResponsiveContainer } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042'];

const HTTPStatusDistribution = ({ httpStatusData }) => {
  // Handle the case where httpStatusData is undefined or null
  if (!httpStatusData || httpStatusData.length === 0) {
    return (
      <Grid item xs={12} md={6}>
        <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
              HTTP Status Distribution
            </Typography>
            <Typography variant="h6" sx={{ color: '#ff5252' }}>
              No data available
            </Typography>
          </CardContent>
        </Card>
      </Grid>
    );
  }

  return (
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
  );
};

export default HTTPStatusDistribution;
