import React from 'react';
import { Admin, Resource } from 'react-admin';
import { ScanHistoryList } from './components/ScanHistoryList';
import DashboardIcon from '@mui/icons-material/Dashboard';
import jsonServerProvider from 'ra-data-json-server';
import Dashboard from './dashboard';
import SettingsPage from './SettingsPage';

const dataProvider = jsonServerProvider('https://jsonplaceholder.typicode.com');

const App = () => (
  <Admin
    dataProvider={dataProvider}
    dashboard={Dashboard}
    title="Cyber Admin Dashboard"
  >
    <Resource name="scanHistory" list={ScanHistoryList} icon={DashboardIcon} />
    <Resource name="settings" list={SettingsPage} />
  </Admin>
);

export default App;  // Ensure this is present
