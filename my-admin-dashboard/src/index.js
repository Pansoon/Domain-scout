import React from 'react';
import ReactDOM from 'react-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import App from './App';

const theme = createTheme({
  palette: {
    mode: 'dark',  // Use dark mode for the cyber theme
    primary: {
      main: '#1B9CFC',  // Neon blue for primary color
    },
    secondary: {
      main: '#18ffff',  // Neon cyan for secondary color (can be kept as is)
    },
    background: {
      default: '#121212',  // Very dark background for the cyber theme
      paper: '#1e1e1e',  // Slightly lighter for cards, panels
    },
    text: {
      primary: '#ffffff',  // White text for better contrast
      secondary: '#1B9CFC',  // Grey text for secondary elements
    },
  },
  typography: {
    fontFamily: '"Roboto Mono", monospace',  // Sleek monospace font
    h1: {
      fontSize: '2.5rem',
      fontWeight: 700,
      color: '#00e676',
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 600,
      color: '#18ffff',
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      color: '#ffffff',
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',  // Slightly rounded buttons
          textTransform: 'none',  // Avoid uppercase button text
          boxShadow: '0 3px 5px 2px rgba(0, 230, 118, .3)',  // Neon glow effect
        },
      },
    },
  },
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <CssBaseline />
    <App />
  </ThemeProvider>,
  document.getElementById('root')
);
