import './Cleric.scss';
import React from 'react';

interface ClericProps {
  disabled?: boolean;
  className?: string;
}

const Cleric: React.FC<ClericProps> = ({ disabled, className }) => {
  const maceArt = `
<span class="mace-head">.----.</span>
<span class="mace-head">/_____\\</span>
<span class="mace-head">|_____|</span>
<span class="mace-head">\\_____/</span>
<span class="mace-head">'----'</span>
<span class="mace-handle">||</span>
<span class="mace-handle">||</span>
<span class="mace-handle">||</span>
<span class="mace-handle">||</span>
<span class="mace-handle">||</span>
<span class="mace-handle">||</span>
<span class="mace-bottom">--</span>
  `;

  return (
    <div
      className={`cleric-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: maceArt }}
    />
  );
};

export default Cleric;