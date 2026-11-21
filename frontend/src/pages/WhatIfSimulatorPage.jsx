import React from 'react';
import FeaturePlaceholder from './FeaturePlaceholder';
import { Sliders } from 'lucide-react';

export const WhatIfSimulatorPage = () => {
  return (
    <FeaturePlaceholder
      title="What-If Salary Simulation Lab"
      phaseNumber="6"
      icon={Sliders}
      description="Interactive sandbox allowing engineers to add hypothetical skills, adjust years of experience, or switch job domains to observe predicted salary changes in real time."
      plannedFeatures={[
        'Interactive skill add/remove playground with instant recalculation.',
        'Experience slider showing annual compensation growth curve.',
        'Location mobility analysis (e.g. Remote vs Bengaluru vs Hyderabad).',
        'Side-by-side simulation comparison export.',
      ]}
    />
  );
};

export default WhatIfSimulatorPage;
