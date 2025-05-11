import './Warlock.scss';
import React from 'react';

interface WarlockProps {
  disabled?: boolean;
  className?: string;
}

const Warlock: React.FC<WarlockProps> = ({ disabled, className }) => {
  const staffArt = `

<span class="sword-blade">^</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-guard">[===]</span>
<span class="sword-handle">||</span>
<span class="sword-pommel">()</span>
  `;

  return (
    <div
      className={`warlock-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: staffArt }}
    />
  );
};

export default Warlock;