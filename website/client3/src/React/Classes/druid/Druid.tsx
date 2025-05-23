import './Druid.scss';
import React from 'react';

interface DruidProps {
  disabled?: boolean;
  className?: string;
}

const Druid: React.FC<DruidProps> = ({ disabled, className }) => {
  const staffArt = `
<span class="staff-bottom">--</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-handle">||</span>
<span class="staff-bottom">--</span>
  `;

  return (
    <div
      className={`druid-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: staffArt }}
    />
  );
};

export default Druid;