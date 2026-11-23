import { profileService } from './profileService';
import { predictionService } from './predictionService';
import { intelligenceService } from './intelligenceService';

export const dashboardService = {
  /**
   * Fetches unified dashboard payload from real backend APIs.
   * Handles partial failures gracefully to ensure dashboard always renders available insights.
   */
  async getDashboardData() {
    const results = {
      profile: null,
      latestPrediction: null,
      predictionHistory: [],
      matchedRoles: [],
      roadmaps: [],
      modelInfo: null,
      stats: {
        totalEvaluations: 0,
        skillCount: 0,
        matchedRoleCount: 0,
        roadmapProgressPct: 0,
      },
    };

    // 1. Fetch Profile
    try {
      const profile = await profileService.getProfile();
      results.profile = profile;
      if (profile?.skills) {
        results.stats.skillCount = profile.skills.length;
      }
    } catch (err) {
      console.warn('Dashboard: Failed to fetch profile', err);
    }

    // 2. Fetch Prediction History
    try {
      const historyData = await predictionService.getPredictionHistory(1);
      if (historyData?.results?.length > 0) {
        results.latestPrediction = historyData.results[0];
        results.predictionHistory = historyData.results;
        results.stats.totalEvaluations = historyData.count || historyData.results.length;
      }
    } catch (err) {
      console.warn('Dashboard: Failed to fetch prediction history', err);
    }

    // 3. Fetch Matched Roles (based on profile skills if available)
    try {
      const skills = results.profile?.skills?.map((s) => s.name) || [
        'Python',
        'SQL',
        'Git',
        'REST APIs',
      ];
      const exp = results.profile?.years_of_experience || 2.0;
      const matchData = await intelligenceService.matchJobRoles(skills, exp);
      if (matchData?.matches) {
        results.matchedRoles = matchData.matches;
        results.stats.matchedRoleCount = matchData.matches.length;
      }
    } catch (err) {
      console.warn('Dashboard: Failed to fetch matched roles', err);
    }

    // 4. Fetch Roadmaps
    try {
      const roadmapsData = await intelligenceService.getRoadmaps();
      const list = roadmapsData?.results || (Array.isArray(roadmapsData) ? roadmapsData : []);
      results.roadmaps = list;
      if (list.length > 0) {
        results.stats.roadmapProgressPct = list[0].overall_progress_pct || 0;
      }
    } catch (err) {
      console.warn('Dashboard: Failed to fetch roadmaps', err);
    }

    // 5. Fetch Model Governance Info
    try {
      const modelInfo = await predictionService.getModelInfo();
      results.modelInfo = modelInfo;
    } catch (err) {
      console.warn('Dashboard: Failed to fetch model info', err);
    }

    return results;
  },
};

export default dashboardService;
