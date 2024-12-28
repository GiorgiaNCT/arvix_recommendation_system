import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Paper } from './components/Paper';

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <div className="App">
        <h1>ArXiv Paper Recommendations</h1>
        <Paper />
      </div>
    </QueryClientProvider>
  );
}

export default App;