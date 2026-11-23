import api from './api';

export const predictionService = {
  /**
   * Request real-time machine learning salary prediction.
   * @param {Object} predictionData - { job_role, years_of_experience, location, education, skills }
   * @returns {Promise<Object>} API prediction response payload
   */
  async createSalaryPrediction(predictionData) {
    const response = await api.post('/predictions/salary/', predictionData);
    return response.data;
  },

  /**
   * Fetch paginated salary prediction history for the authenticated user.
   * @param {number} page - Current page number
   * @returns {Promise<Object>} Paginated prediction records { count, next, previous, results }
   */
  async getPredictionHistory(page = 1) {
    const response = await api.get('/predictions/history/', {
      params: { page },
    });
    return response.data;
  },

  /**
   * Fetch details of a single historical prediction.
   * @param {number|string} id - Prediction ID
   * @returns {Promise<Object>} Single prediction record
   */
  async getPredictionDetail(id) {
    const response = await api.get(`/predictions/history/${id}/`);
    return response.data;
  },

  /**
   * Fetch governance and evaluation metadata of current ML models.
   * @returns {Promise<Object>} Model governance details
   */
  async getModelInfo() {
    const response = await api.get('/predictions/model-info/');
    return response.data;
  },
};
