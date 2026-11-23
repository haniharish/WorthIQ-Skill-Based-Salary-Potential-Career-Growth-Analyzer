import api from './api';

export const resumeService = {
  // Upload resume document (PDF or DOCX)
  uploadResume: async (file, onUploadProgress = null) => {
    const formData = new FormData();
    formData.append('file', file);

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    };

    if (onUploadProgress) {
      config.onUploadProgress = onUploadProgress;
    }

    const response = await api.post('/resumes/upload/', formData, config);
    return response.data;
  },

  // List all uploaded resumes
  getResumes: async () => {
    const response = await api.get('/resumes/');
    return response.data;
  },

  // Get single resume document details
  getResumeById: async (id) => {
    const response = await api.get(`/resumes/${id}/`);
    return response.data;
  },

  // Get full extraction results & profile comparison
  getResumeResults: async (id) => {
    const response = await api.get(`/resumes/${id}/results/`);
    return response.data;
  },

  // Apply confirmed extracted skills / candidate info to user profile
  applyToProfile: async (id, confirmedData) => {
    const response = await api.post(`/resumes/${id}/apply-to-profile/`, confirmedData);
    return response.data;
  },

  // Delete resume
  deleteResume: async (id) => {
    const response = await api.delete(`/resumes/${id}/`);
    return response.data;
  },
};

export default resumeService;
