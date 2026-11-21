import React from 'react';
import { Link } from 'react-router-dom';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import { ArrowLeft, Clock, Sparkles, CheckCircle2 } from 'lucide-react';

export const FeaturePlaceholder = ({
  title,
  phaseNumber,
  description,
  plannedFeatures = [],
  icon: Icon = Sparkles,
}) => {
  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <Link to="/dashboard">
          <Button variant="ghost" size="sm" icon={ArrowLeft}>
            Back to Dashboard
          </Button>
        </Link>
        <Badge variant="indigo">Scheduled for Phase {phaseNumber}</Badge>
      </div>

      <Card padding="p-8 sm:p-10" className="text-center">
        <div className="w-16 h-16 rounded-2xl bg-indigo-50 text-indigo-600 flex items-center justify-center mx-auto mb-6 shadow-xs">
          <Icon className="w-8 h-8" />
        </div>

        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          {title}
        </h1>
        <p className="mt-3 text-sm text-slate-600 max-w-xl mx-auto leading-relaxed">
          {description}
        </p>

        <div className="mt-8 p-6 rounded-2xl bg-slate-50 border border-slate-200/80 text-left max-w-2xl mx-auto">
          <div className="flex items-center gap-2 mb-4">
            <Clock className="w-4 h-4 text-indigo-600" />
            <h4 className="text-xs font-bold text-slate-900 uppercase tracking-wider">
              Phase {phaseNumber} Technical Roadmap &amp; Scope
            </h4>
          </div>

          <ul className="space-y-3">
            {plannedFeatures.map((feat, index) => (
              <li key={index} className="flex items-start gap-2.5 text-xs text-slate-700">
                <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0 mt-0.5" />
                <span>{feat}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="mt-8 flex justify-center gap-4">
          <Link to="/dashboard">
            <Button variant="primary" size="md">
              Return to Active Dashboard
            </Button>
          </Link>
          <Link to="/profile/setup">
            <Button variant="outline" size="md">
              Update Profile Skills
            </Button>
          </Link>
        </div>
      </Card>
    </div>
  );
};

export default FeaturePlaceholder;
