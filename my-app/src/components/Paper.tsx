import React from 'react';
import { useRandomPaper } from '../hooks/useRandomPaper';
import { Paper as PaperType } from '../types/index';

export const Paper = () => {
  const { data, isLoading, isError, refetch } = useRandomPaper();

  if (isLoading) return <div>Loading...</div>;
  if (isError) return <div>Error fetching paper</div>;

  return (
    <div>
      <h2>{data?.title}</h2>
      {/* Add more paper details here */}
      <button onClick={() => refetch()}>Get Another Paper</button>
    </div>
  );
};