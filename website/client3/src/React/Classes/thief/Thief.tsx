import './Thief.scss';
import React from 'react';

interface ThiefProps {
  disabled?: boolean;
  className?: string;
}

const Thief: React.FC<ThiefProps> = ({ disabled, className }) => {
  const staffArt = `

<span class="padlock-handle"></span>
<span class="padlock-handle">||||||||</span>
<span class="padlock-handle">||    ||</span>
<span class="padlock-handle">||    ||</span>
<span class="padlock-handle">||    ||</span>
<span class="padlock-base">||||||||||||</span>
<span class="padlock-base">|||||<span class="padlock-hole">  </span>|||||</span>
<span class="padlock-base">||||||||||||</span>
<span class="padlock-bottom">==========</span>
  `;

  return (
    <div
      className={`thief-icon ${className || ''} ${disabled ? 'disabled' : ''}`}
      style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8', textAlign: 'center' }}
      dangerouslySetInnerHTML={{ __html: staffArt }}
    />
  );
};

export default Thief;