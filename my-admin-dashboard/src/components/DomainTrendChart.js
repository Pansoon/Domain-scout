import React from 'react';
import PropTypes from 'prop-types';
import { Typography, Card, CardContent } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { v4 as uuidv4 } from 'uuid';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
        <p>{`Date: ${label}`}</p>
        {payload.map((entry, index) => (
          <p key={`item-${index}`}>{`${entry.name}: ${entry.value}`}</p>
        ))}
      </div>
    );
  }
  return null;
};

CustomTooltip.propTypes = {
  active: PropTypes.bool,
  payload: PropTypes.array,
  label: PropTypes.string,
};

const colors = ['#ff0000', '#00ff00', '#0000ff', '#ff00ff', '#00ffff', '#ffff00', '#ff8000'];

const DomainTrendChart = ({ data = [] }) => {
  // Ensure that tlds are extracted safely when data is not empty
  const tlds = data.length > 0 ? Object.keys(data[0]).filter(key => key !== 'date') : [];

  return (
    <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
      <CardContent>
        <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
          Domain Trend by TLD
        </Typography>

        {data.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {tlds.map((tld, index) => (
                <Line
                  key={uuidv4()}
                  type="monotone"
                  dataKey={tld}
                  name={tld}
                  stroke={colors[index % colors.length]}
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        ) : (
          <Typography variant="body1" sx={{ color: '#ffffff' }}>
            No data available to display.
          </Typography>
        )}
      </CardContent>
    </Card>
  );
};

DomainTrendChart.propTypes = {
  data: PropTypes.arrayOf(
    PropTypes.shape({
      date: PropTypes.string.isRequired,
      // Define dynamic TLDs shape, assuming it's numbers for each TLD
    })
  ),
};

export default DomainTrendChart;
