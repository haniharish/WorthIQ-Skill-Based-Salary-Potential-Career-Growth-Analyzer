import api from './api';

export const scenarioService = {
  // Get all saved scenarios for current user
  getScenarios: async () => {
    const response = await api.get('/scenarios/');
    return response.data;
  },

  // Get single scenario by ID
  getScenarioById: async (id) => {
    const response = await api.get(`/scenarios/${id}/`);
    return response.data;
  },

  // Create a new scenario
  createScenario: async (scenarioData) => {
    const response = await api.post('/scenarios/', scenarioData);
    return response.data;
  },

  // Update existing scenario
  updateScenario: async (id, scenarioData) => {
    const response = await api.put(`/scenarios/${id}/`, scenarioData);
    return response.data;
  },

  // Delete scenario
  deleteScenario: async (id) => {
    const response = await api.delete(`/scenarios/${id}/`);
    return response.data;
  },

  // Duplicate scenario
  duplicateScenario: async (id) => {
    const response = await api.post(`/scenarios/${id}/duplicate/`);
    return response.data;
  },

  // Simulate prediction for unsaved profile inputs
  simulatePrediction: async (scenarioInputs) => {
    const response = await api.post('/scenarios/predict/', scenarioInputs);
    return response.data;
  },

  // Compare multiple scenarios (by IDs or inline custom profiles)
  compareScenarios: async (payload) => {
    const response = await api.post('/scenarios/compare/', payload);
    return response.data;
  },
};

export default scenarioService;
