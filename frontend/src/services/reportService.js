import api from './api';

export const reportService = {
  // Get all reports for user with optional ?type= filter
  getReports: async (type = null) => {
    const params = type ? { type } : {};
    const response = await api.get('/reports/', { params });
    return response.data;
  },

  // Get report detail
  getReportById: async (id) => {
    const response = await api.get(`/reports/${id}/`);
    return response.data;
  },

  // Generate a new report snapshot
  generateReport: async (reportData) => {
    const response = await api.post('/reports/generate/', reportData);
    return response.data;
  },

  // Download PDF report
  downloadReportPdf: async (id, title = 'WorthIQ_Report') => {
    const response = await api.get(`/reports/${id}/download/`, {
      responseType: 'blob',
    });
    
    // Create download link
    const blob = new Blob([response.data], { type: 'application/pdf' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `${title.replace(/[^a-zA-Z0-9_-]/g, '_')}_${id}.pdf`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  },

  // Export CSV (type='predictions' or type='scenarios')
  exportCsv: async (exportType = 'predictions') => {
    const response = await api.get('/reports/export/csv/', {
      params: { type: exportType },
      responseType: 'blob',
    });

    const blob = new Blob([response.data], { type: 'text/csv;charset=utf-8;' });
    const downloadUrl = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = downloadUrl;
    link.setAttribute('download', `WorthIQ_${exportType}_export_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    link.parentNode.removeChild(link);
    window.URL.revokeObjectURL(downloadUrl);
  },

  // Delete report
  deleteReport: async (id) => {
    const response = await api.delete(`/reports/${id}/`);
    return response.data;
  },
};

export default reportService;
