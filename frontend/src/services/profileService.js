import api from './api';

export const profileService = {
  async getProfile() {
    try {
      const response = await api.get('/profile/');
      return response.data;
    } catch (error) {
      if (error.response && error.response.status === 404) {
        return null;
      }
      throw error;
    }
  },

  async createProfile(profileData) {
    const response = await api.post('/profile/', profileData);
    return response.data;
  },

  async updateProfile(profileData) {
    const response = await api.put('/profile/', profileData);
    return response.data;
  },

  async patchProfile(partialData) {
    const response = await api.patch('/profile/', partialData);
    return response.data;
  },

  async getSkills(search = '') {
    const params = search ? { search } : {};
    const response = await api.get('/profile/skills/', { params });
    return response.data;
  },
};
