import React from 'react';
import FeaturePlaceholder from './FeaturePlaceholder';
import { Compass } from 'lucide-react';

export const CareerRoadmapPage = () => {
  return (
    <FeaturePlaceholder
      title="Dynamic Career Growth Roadmap"
      phaseNumber="5"
      icon={Compass}
      description="Algorithmic sequential learning trajectories designed to bridge you from your current market valuation to target salary tiers."
      plannedFeatures={[
        'Directed acyclic graph (DAG) of prerequisite skills.',
        'Target salary milestones (e.g. ₹12 LPA -> ₹20 LPA path).',
        'Time-to-proficiency estimation for recommended technologies.',
        'Curated documentation and project milestone trackers.',
      ]}
    />
  );
};

export default CareerRoadmapPage;
