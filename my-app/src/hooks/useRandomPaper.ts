import { useQuery } from '@tanstack/react-query';
import { getRandomSelection } from '../services/api';

export const useRandomPaper = () => {
  return useQuery({
    queryKey: ['randomPaper'],
    queryFn: getRandomSelection,
  });
};