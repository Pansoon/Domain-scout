import React, { useState, useCallback } from 'react';
import { Button, Typography, Card, CardContent } from '@mui/material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import Papa from 'papaparse';
import { v4 as uuidv4 } from 'uuid';

const CustomTooltip = React.memo(({ active, payload, label }) => {
  if (active && payload && payload.length) {
    const { name, value } = payload[0];
    return (
      <div style={{ backgroundColor: '#fff', padding: '10px', border: '1px solid #ccc' }}>
        <p>{`Date: ${label}`}</p>
        <p>{`${name}: ${value}`}</p>
      </div>
    );
  }
  return null;
});


const DomainTrendChart = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [filePath, setFilePath] = useState('');
  const [data, setData] = useState([]);
  const [domains, setDomains] = useState([]);
  const [colors, setColors] = useState({}); // State to store the colors for each domain
  const [loading, setLoading] = useState(false);

// Function to extract domain from URL (after the last ".")
const extractDomain = useCallback((url) => {
  if (!url || typeof url !== 'string') {
    console.error('Invalid URL:', url); // Optional: log for debugging purposes
    return 'Unknown';  // Return a default value if URL is invalid
  }

  const domainParts = url.split('.');
  return domainParts.length > 1 ? domainParts.slice(-2).join('.') : url;
}, []);


  // Generate a random color for a domain (only once)
  const getColorForDomain = (domain) => {
    if (!colors[domain]) {
      setColors((prevColors) => ({
        ...prevColors,
        [domain]: `#${Math.floor(Math.random() * 16777215).toString(16)}`,
      }));
    }
    return colors[domain];
  };

  // Function to handle CSV file selection
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setLoading(true); // Set loading state
      setSelectedFile(file);
      setFilePath(file.name);
      parseCSVFile(file);
    }
  };

  // Function to parse the selected CSV file and group by domain, filling missing dates
  const parseCSVFile = useCallback((file) => {
    if (!file) return;

    Papa.parse(file, {
      header: true,
      complete: (result) => {
        const groupedData = {};
        const domainSet = new Set();
        const allDates = new Set(); // To store all unique dates for all domains

        result.data.forEach((row) => {
          const domain = extractDomain(row['Domain Name']);
          const isActive = row['Port Status']?.includes('Open');

          if (!groupedData[domain]) {
            groupedData[domain] = {};
          }

          domainSet.add(domain); // Track unique domains

          // Add the scan date to the set of all dates
          const scanDate = row['Scan Date'];
          allDates.add(scanDate);

          // If site is active, increment the count for that domain on that date
          if (!groupedData[domain][scanDate]) {
            groupedData[domain][scanDate] = 0;
          }
          if (isActive) {
            groupedData[domain][scanDate] += 1;
          }
        });

        // Fill in missing dates for all domains with 0 activity
        allDates.forEach((date) => {
          Object.keys(groupedData).forEach((domain) => {
            if (!groupedData[domain][date]) {
              groupedData[domain][date] = 0; // If no data for that date, set it to 0
            }
          });
        });

        // Transform grouped data into chart-friendly format
        const transformedData = [];
        allDates.forEach((date) => {
          const dateEntry = { date };
          Object.keys(groupedData).forEach((domain) => {
            dateEntry[domain] = groupedData[domain][date]; // Add domain's data for the specific date
          });
          transformedData.push(dateEntry);
        });

        // Sort data by date to avoid rendering issues (important)
        transformedData.sort((a, b) => new Date(a.date) - new Date(b.date));

        setDomains([...domainSet]); // Set the list of unique domains
        setData(transformedData);
        setLoading(false); // Set loading to false once data is ready
      },
    });
  }, [extractDomain]);

  // Function to handle the refresh button click
  const handleRefresh = () => {
    if (selectedFile) {
      setLoading(true); // Set loading state
      parseCSVFile(selectedFile); // Re-parse the currently selected file
    }
  };

  return (
    <Card sx={{ backgroundColor: '#1e1e1e', color: '#ffffff', padding: '20px', textAlign: 'center' }}>
      <CardContent>
        <Typography variant="h4" sx={{ color: '#18ffff', marginBottom: '20px' }}>
          Domain Trend
        </Typography>

        {/* File Selection Button */}
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
          disabled={!selectedFile} // Disable refresh if no file is selected
        >
          Refresh Chart
        </Button>

        {loading && <p>Loading data...</p>}

        {/* Render the chart if data exists */}
        {!loading && data.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip content={<CustomTooltip />} isAnimationActive={false} />
              <Legend />
              {/* Dynamically render a Line for each domain */}
              {domains.map((domain) => (
                <Line
                  key={uuidv4()}
                  type="monotone"
                  dataKey={domain}
                  name={domain}
                  stroke={getColorForDomain(domain)} // Use stored color for each domain
                  strokeWidth={3} // Increase the thickness of the lines
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
