import './Warrior.scss';
import React from 'react';

interface WarriorProps {
  disabled?: boolean;
  className?: string;
}

const Warrior: React.FC<WarriorProps> = ({ disabled, className }) => {
  const staffArt = `

<span class="sword-blade">^</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-blade">||</span>
<span class="sword-guard">[===]</span>
<span class="sword-handle">||</span>
<span class="sword-handle">||</span>
<span class="sword-pommel">()</span>
  `;

  return (
    <div
      className={`warrior-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: staffArt }}
    />
  );
};

export default Warrior;