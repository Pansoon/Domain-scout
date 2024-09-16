import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';  // Ensure this is a default import

test('renders cyber admin dashboard', () => {
  render(<App />);
  const linkElement = screen.getByText(/Cyber Admin Dashboard/i);
  expect(linkElement).toBeInTheDocument();
});
