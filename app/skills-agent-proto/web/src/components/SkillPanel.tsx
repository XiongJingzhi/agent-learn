import { memo } from "react";

import type { SkillSummary } from "../state/chatReducer";

type SkillPanelProps = {
  skills: SkillSummary[];
  activeSkillName?: string;
  loading: boolean;
  error?: string;
};

export const SkillPanel = memo(function SkillPanel({
  skills,
  activeSkillName,
  loading,
  error,
}: SkillPanelProps) {
  return (
    <aside className="skills-panel">
      <header className="skills-panel__header">
        <p className="eyebrow">Capabilities</p>
        <h2>Discovered Skills</h2>
      </header>

      {loading && <p className="skills-panel__hint">Scanning skills...</p>}
      {error && <p className="skills-panel__error">{error}</p>}

      {!loading && !error && skills.length === 0 && (
        <p className="skills-panel__hint">No skills found.</p>
      )}

      <ul className="skills-list">
        {skills.map((skill) => {
          const active = skill.name === activeSkillName;
          const description = skill.description || "No description provided.";
          return (
            <li
              key={skill.name}
              className={active ? "skill-card skill-card--active" : "skill-card"}
            >
              <div className="skill-card__title-row">
                <h3>{skill.name}</h3>
                {active && <span className="skill-card__badge">In Use</span>}
              </div>
              <p className="skill-card__description" title={description}>
                {description}
              </p>
              <code className="skill-card__path" title={skill.path}>
                {skill.path}
              </code>
            </li>
          );
        })}
      </ul>
    </aside>
  );
});
