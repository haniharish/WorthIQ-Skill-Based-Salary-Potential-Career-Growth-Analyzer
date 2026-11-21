import React from 'react';
import FeaturePlaceholder from './FeaturePlaceholder';
import { BookmarkCheck } from 'lucide-react';

export const SavedReportsPage = () => {
  return (
    <FeaturePlaceholder
      title="Saved Reports & History"
      phaseNumber="1-2"
      icon={BookmarkCheck}
      description="Archive of your historical salary evaluations, simulation comparisons, and downloaded career milestone assessments."
      plannedFeatures={[
        'Exportable PDF reports for salary appraisals and career reviews.',
        'Historical compensation trajectory tracking over time.',
        'Target goal tracking and skill acquisition timestamps.',
      ]}
    />
  );
};

export default SavedReportsPage;
