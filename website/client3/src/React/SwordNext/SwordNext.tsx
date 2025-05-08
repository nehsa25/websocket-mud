import './SwordNext.scss';

import React from 'react';

interface SwordNextProps {
    disabled?: boolean;
    className?: string;
}

const SwordNext: React.FC<SwordNextProps> = ({ disabled, className }) => {
    const swordArt = `
<span class="sword-pommel">                  |</span>  <span class="sword-hilt">|</span><span class="sword-shiny">============================\\</span></span>
<span class="sword-pommel">         [===========</span><span class="sword-hilt">|</span><span class="sword-text">NEXT</span>| </span><span class="sword-blade">>>>>>>>>>>>>>>>>>>>>>>><span class="sword-shiny">></span></span>
<span class="sword-pommel">                  |</span>  <span class="sword-hilt">|</span><span class="sword-shiny">============================/</span></span>
    `;

    return (
        <div
                className="sword-next-icon"
                style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8' }}
                dangerouslySetInnerHTML={{ __html: swordArt }}
            />
    );
};

export default SwordNext;