import React, { useState, useCallback, useMemo } from 'react';
import PropTypes from 'prop-types';
import { Button, Typography, Card, CardContent } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Papa from 'papaparse';
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

const extractTLD = (url) => {
  if (!url || typeof url !== 'string') {
    return 'Unknown';
  }
  const domainParts = url.split('.');
  return domainParts.length > 1 ? domainParts[domainParts.length - 1] : url;
};

const DomainTrendChart = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePath, setFilePath] = useState('');
  const [data, setData] = useState([]);
  const [tlds, setTLDs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const parseCSVFile = useCallback((file) => {
    if (!file) return;

    setLoading(true);
    setError(null);
    Papa.parse(file, {
      header: true,
      complete: (result) => {
        try {
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
            if (scanDate) {
              allDates.add(scanDate);

              if (!groupedData[tld][scanDate]) {
                groupedData[tld][scanDate] = 0;
              }
              groupedData[tld][scanDate] += 1;
            }
          });

          allDates.forEach((date) => {
            tldSet.forEach((tld) => {
              if (!groupedData[tld][date]) {
                groupedData[tld][date] = 0;
              }
            });
          });

          const transformedData = Array.from(allDates).map((date) => {
            const dateEntry = { date };
            tldSet.forEach((tld) => {
              dateEntry[tld] = groupedData[tld][date];
            });
            return dateEntry;
          });

          transformedData.sort((a, b) => new Date(a.date) - new Date(b.date));

          setData(transformedData);
          setTLDs(Array.from(tldSet));
        } catch (err) {
          console.error('Error parsing CSV:', err);
          setError('Error parsing CSV file. Please check the file format and try again.');
        } finally {
          setLoading(false);
        }
      },
      error: (err) => {
        console.error('Papa Parse error:', err);
        setError('Error parsing CSV file. Please check the file format and try again.');
        setLoading(false);
      },
    });
  }, []);

  const handleFileChange = useCallback((event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFilePath(file.name);
      parseCSVFile(file);
    }
  }, [parseCSVFile]);

  const handleRefresh = useCallback(() => {
    if (selectedFile) {
      parseCSVFile(selectedFile);
    }
  }, [selectedFile, parseCSVFile]);

  const chartData = useMemo(() => data, [data]);

  return (
    <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
      <CardContent>
        <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
          Domain Trend by TLD
        </Typography>

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

        <Button
          variant="contained"
          color="primary"
          onClick={handleRefresh}
          sx={{ marginBottom: '20px', marginLeft: '10px' }}
          disabled={!selectedFile}
        >
          Refresh Chart
        </Button>

        {loading && <Typography variant="body1">Loading data...</Typography>}
        {error && <Typography variant="body1" color="error">{error}</Typography>}

        {!loading && !error && chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
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
          !loading && !error && (
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