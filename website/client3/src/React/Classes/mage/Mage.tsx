import './Mage.scss';
import React from 'react';

interface MageProps {
  disabled?: boolean;
  className?: string;
}

const Mage: React.FC<MageProps> = ({ disabled, className }) => {
  const staffArt = `

<span class="staff-head">(<span class="staff-glow">*</span>)</span>
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
<span class="staff-bottom">--</span>
  `;

  return (
    <div
      className={`mage-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: staffArt }}
    />
  );
};

export default Mage;