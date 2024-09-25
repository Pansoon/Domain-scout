import React, { useState } from 'react';
import { Button, Typography, Card, CardContent } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Papa from 'papaparse';
import { v4 as uuidv4 } from 'uuid';

// Custom Tooltip
const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
        <p>{`Date: ${label}`}</p>
        <p>{`${payload[0].name}: ${payload[0].value}`}</p>
      </div>
    );
  }
  return null;
};

const DomainTrendChart = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePath, setFilePath] = useState('');
  const [data, setData] = useState([]);
  const [tlds, setTLDs] = useState([]);
  const [loading, setLoading] = useState(false);

  // Extract the TLD from the domain name
  const extractTLD = (url) => {
    if (!url || typeof url !== 'string') {
      return 'Unknown';
    }
    const domainParts = url.split('.');
    return domainParts.length > 1 ? domainParts.slice(-1).join('.') : url;
  };

  // Handle CSV file selection and parsing
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true);
      setSelectedFile(file);
      setFilePath(file.name);
      parseCSVFile(file);
    }
  };

  // Parse CSV file and update state
  const parseCSVFile = (file) => {
    if (!file) return;

    Papa.parse(file, {
      header: true,
      complete: (result) => {
        const groupedData = {};
        const tldSet = new Set();
        const allDates = new Set();

        result.data.forEach((row) => {
          const tld = extractTLD(row['Domain Name']);
          if (!groupedData[tld]) {
            groupedData[tld] = {};
          }

          tldSet.add(tld);
          const scanDate = row['Scan Date'];
          allDates.add(scanDate);

          if (!groupedData[tld][scanDate]) {
            groupedData[tld][scanDate] = 0;
          }
          groupedData[tld][scanDate] += 1;
        });

        // Fill missing dates with zeroes for all TLDs
        allDates.forEach((date) => {
          tldSet.forEach((tld) => {
            if (!groupedData[tld][date]) {
              groupedData[tld][date] = 0;
            }
          });
        });

        const transformedData = [];
        allDates.forEach((date) => {
          const dateEntry = { date };
          tldSet.forEach((tld) => {
            dateEntry[tld] = groupedData[tld][date];
          });
          transformedData.push(dateEntry);
        });

        transformedData.sort((a, b) => new Date(a.date) - new Date(b.date));

        setData(transformedData);
        setTLDs([...tldSet]);
        setLoading(false);
      },
    });
  };

  // Refresh the chart by re-parsing the file
  const handleRefresh = () => {
    if (selectedFile) {
      setLoading(true);
      parseCSVFile(selectedFile);
    }
  };

  return (
    <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
      <CardContent>
        <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
          Domain Trend by TLD
        </Typography>

        {/* File Selection */}
        <Button
          variant="contained"
          component="label"
          color="secondary"
          sx={{ marginBottom: '10px' }}
        >
          Choose File
          <input
            type="file"
            accept=".csv"
            hidden
            onChange={handleFileChange}
          />
        </Button>
        {filePath && (
          <Typography variant="body2" sx={{ color: '#ffffff', marginLeft: '10px', display: 'inline-block' }}>
            {filePath}
          </Typography>
        )}

        {/* Refresh Button */}
        <Button
          variant="contained"
          color="primary"
          onClick={handleRefresh}
          sx={{ marginBottom: '20px' }}
          disabled={!selectedFile}
        >
          Refresh Chart
        </Button>

        {loading && <p>Loading data...</p>}

        {/* Render Chart */}
        {!loading && data.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} />
              <Legend />
              {tlds.map((tld) => (
                <Line
                  key={uuidv4()}
                  type="monotone"
                  dataKey={tld}
                  name={tld}
                  stroke={`#${Math.floor(Math.random() * 16777215).toString(16)}`} // Random color
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        ) : (
          !loading && (
            <Typography variant="body1" sx={{ color: '#ffffff' }}>
              No data available to display.
            </Typography>
          )
        )}
      </CardContent>
    </Card>
  );
};

export default DomainTrendChart;
