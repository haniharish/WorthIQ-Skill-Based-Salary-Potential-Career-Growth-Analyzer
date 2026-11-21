import api from './api';

export const authService = {
  async register(userData) {
    const response = await api.post('/auth/register/', userData);
    return response.data;
  },

  async login(credentials) {
    const response = await api.post('/auth/login/', credentials);
    return response.data;
  },

  async logout(refreshToken) {
    try {
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (err) {
      console.warn('Logout endpoint call failed, proceeding with local cleanup', err);
    }
  },

  async getCurrentUser() {
    const response = await api.get('/auth/me/');
    return response.data;
  },
};
