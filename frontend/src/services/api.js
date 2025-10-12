/**
 * API client for CodeCollab backend
 * Connects to the simple_api_server.py backend
 */

import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Process task endpoint (main swarm processing)
export const processTask = async (description, githubUrl = '', requirements = '') => {
  const response = await api.post('/process', {
    task: description,
    github_url: githubUrl,
    requirements: requirements
  });
  return response.data;
};

// Get task history
export const listTasks = async () => {
  const response = await api.get('/history');
  return response.data;
};

// Get agents info
export const getAgents = async () => {
  const response = await api.get('/agents');
  return response.data;
};

// Health check
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

// Get system status
export const getSystemStatus = async () => {
  try {
    const health = await healthCheck();
    return {
      status: health.swarm_available ? 'healthy' : 'degraded',
      version: '1.0.0',
      swarm_available: health.swarm_available,
      agents_count: health.agents_count,
      tasks: {},
      payments: {}
    };
  } catch (error) {
    return {
      status: 'error',
      version: '1.0.0',
      tasks: {},
      payments: {}
    };
  }
};

export default api;