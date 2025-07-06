import axios from 'axios';

export async function fetchInvestigations() {
  const response = await axios.get('/api/v1/investigations');
  return response.data;
} 