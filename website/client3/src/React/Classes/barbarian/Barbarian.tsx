import './Barbarian.scss';
import React from 'react';

interface BarbarianProps {
  disabled?: boolean;
  className?: string;
}

const Barbarian: React.FC<BarbarianProps> = ({ disabled, className }) => {
  const axeArt = `
<span class="axe-head">^</span>
<span class="axe-head">      |<span class="axe-head">______</span></span>
<span class="axe-handle">       |<span class="axe-head">------></span></span>
<span class="axe-handle">       |<span class="axe-head">------></span></span>
<span class="axe-handle">       |<span class="axe-head">------></span></span>
<span class="axe-handle">       |<span class="axe-head">------></span></span>
<span class="axe-handle">  ||</span>
<span class="axe-handle">  ||</span>
<span class="axe-handle">  ||</span>
<span class="axe-handle">  ||</span>
<span class="axe-handle">  ||</span>
<span class="axe-bottom">  --</span>
  `;

  return (
    <div
      className={`barbarian-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: axeArt }}
    />
  );
};

export default Barbarian;