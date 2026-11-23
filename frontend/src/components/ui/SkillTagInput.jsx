import React, { useState } from 'react';
import { X, Plus, Sparkles } from 'lucide-react';
import Badge from './Badge';

export const SkillTagInput = ({
  skills = [],
  onChange,
  suggestions = [],
  placeholder = 'Add a skill (e.g. Python, Docker)...',
  label = 'Technical Skills',
  helperText,
  maxSkills = 20,
}) => {
  const [inputValue, setInputValue] = useState('');

  const handleAddSkill = (skillToAdd) => {
    const trimmed = skillToAdd.trim();
    if (!trimmed) return;
    if (skills.length >= maxSkills) return;
    if (!skills.some((s) => s.toLowerCase() === trimmed.toLowerCase())) {
      onChange([...skills, trimmed]);
    }
    setInputValue('');
  };

  const handleRemoveSkill = (skillToRemove) => {
    onChange(skills.filter((s) => s !== skillToRemove));
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      handleAddSkill(inputValue);
    }
  };

  const filteredSuggestions = suggestions
    .filter(
      (s) =>
        !skills.some((existing) => existing.toLowerCase() === s.toLowerCase()) &&
        s.toLowerCase().includes(inputValue.toLowerCase())
    )
    .slice(0, 8);

  return (
    <div className="space-y-2">
      {label && (
        <div className="flex items-center justify-between">
          <label className="block text-xs font-semibold text-slate-700 tracking-wide">
            {label}
          </label>
          <span className="text-[11px] text-slate-400 font-medium">
            {skills.length} / {maxSkills}
          </span>
        </div>
      )}

      {/* Selected skill chips */}
      <div className="flex flex-wrap gap-1.5 min-h-[38px] p-2 bg-slate-50 border border-slate-200 rounded-xl focus-within:border-indigo-600 focus-within:bg-white focus-within:ring-3 focus-within:ring-indigo-600/10 transition-all">
        {skills.map((skill) => (
          <span
            key={skill}
            className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-lg text-xs font-semibold bg-white text-indigo-700 border border-indigo-200/90 shadow-2xs group"
          >
            <span>{skill}</span>
            <button
              type="button"
              onClick={() => handleRemoveSkill(skill)}
              className="text-indigo-400 hover:text-indigo-700 rounded transition-colors"
              aria-label={`Remove ${skill}`}
            >
              <X className="w-3.5 h-3.5" />
            </button>
          </span>
        ))}

        {/* Input box */}
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={skills.length === 0 ? placeholder : 'Add more...'}
          className="flex-1 min-w-[120px] bg-transparent text-xs text-slate-800 placeholder:text-slate-400 outline-none py-1 px-1.5"
        />
      </div>

      {/* Suggestions pill strip */}
      {filteredSuggestions.length > 0 && (
        <div className="pt-1">
          <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-1 flex items-center gap-1">
            <Sparkles className="w-3 h-3 text-indigo-500" />
            Suggested Skills
          </p>
          <div className="flex flex-wrap gap-1.5">
            {filteredSuggestions.map((sug) => (
              <button
                key={sug}
                type="button"
                onClick={() => handleAddSkill(sug)}
                className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-medium bg-slate-100 hover:bg-indigo-50 text-slate-600 hover:text-indigo-700 border border-slate-200/60 hover:border-indigo-200 transition-colors cursor-pointer"
              >
                <Plus className="w-3 h-3" />
                {sug}
              </button>
            ))}
          </div>
        </div>
      )}

      {helperText && <p className="text-[11px] text-slate-500 mt-1">{helperText}</p>}
    </div>
  );
};

export default SkillTagInput;
