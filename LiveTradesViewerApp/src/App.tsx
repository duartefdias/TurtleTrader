import React from 'react';
import logo from './logo.svg';
import './App.css';

import { StockChart } from './components/StockChart';

export const App = () => {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <StockChart />
      </header>
    </div>
  );
}

