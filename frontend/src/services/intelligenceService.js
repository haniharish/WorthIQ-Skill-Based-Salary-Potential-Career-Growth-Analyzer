import api from './api';

export const intelligenceService = {
  // Module A: SHAP Explainability
  async getPredictionExplanation(predictionId) {
    const response = await api.get(`/intelligence/explanations/${predictionId}/`);
    return response.data;
  },

  async getGlobalExplanation() {
    const response = await api.get('/intelligence/explanations/global/');
    return response.data;
  },

  // Module B: Skill Intelligence & Co-occurrence
  async getSkills() {
    const response = await api.get('/intelligence/skills/');
    return response.data;
  },

  async getSkillImpact(params = {}) {
    const response = await api.get('/intelligence/skills/impact/', { params });
    return response.data;
  },

  async getSkillCoOccurrence(skill = '', limit = 25) {
    const response = await api.get('/intelligence/skills/co-occurrence/', {
      params: { skill, limit },
    });
    return response.data;
  },

  async compareSkills(counterfactualData) {
    const response = await api.post('/intelligence/skills/compare/', counterfactualData);
    return response.data;
  },

  // Module C: Job Role Matching
  async getJobRoles() {
    const response = await api.get('/intelligence/roles/');
    return response.data;
  },

  async getJobRoleDetail(id) {
    const response = await api.get(`/intelligence/roles/${id}/`);
    return response.data;
  },

  async matchJobRoles(skills = [], experience = 0.0) {
    const response = await api.post('/intelligence/roles/match/', { skills, experience });
    return response.data;
  },

  async getRoleRecommendations() {
    const response = await api.get('/intelligence/roles/recommendations/');
    return response.data;
  },

  // Module D: Career Growth Roadmaps
  async getRoadmaps() {
    const response = await api.get('/intelligence/roadmaps/');
    return response.data;
  },

  async generateRoadmap(roadmapData) {
    const response = await api.post('/intelligence/roadmaps/generate/', roadmapData);
    return response.data;
  },

  async getRoadmapDetail(id) {
    const response = await api.get(`/intelligence/roadmaps/${id}/`);
    return response.data;
  },

  async updateRoadmapProgress(id, progressData) {
    const response = await api.patch(`/intelligence/roadmaps/${id}/progress/`, progressData);
    return response.data;
  },

  async deleteRoadmap(id) {
    const response = await api.delete(`/intelligence/roadmaps/${id}/`);
    return response.data;
  },
};

export default intelligenceService;
