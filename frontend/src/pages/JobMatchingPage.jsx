import React from 'react';
import FeaturePlaceholder from './FeaturePlaceholder';
import { Briefcase } from 'lucide-react';

export const JobMatchingPage = () => {
  return (
    <FeaturePlaceholder
      title="Intelligent Job Role Matching"
      phaseNumber="4"
      icon={Briefcase}
      description="NLP and TF-IDF similarity matching comparing your candidate profile against active market job specifications and descriptions."
      plannedFeatures={[
        'TF-IDF & Cosine similarity scoring across verified job descriptions.',
        'Skill coverage gap identification per target role.',
        'Readiness percentage score and missing prerequisite flagging.',
        'Market demand ranking by geographic region.',
      ]}
    />
  );
};

export default JobMatchingPage;
