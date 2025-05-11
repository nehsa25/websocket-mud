import './Bard.scss';

import React from 'react';

interface BardProps {
    disabled?: boolean;
    className?: string;
}

const Bard: React.FC<BardProps> = ({ disabled, className }) => {
    const luteArt = `
<span class="lute-top">     __<span class="lute-strings">===</span>__</span>
<span class="lute-neck">       |<span class="lute-strings">--</span>|</span>
<span class="lute-neck">       |<span class="lute-strings">--</span>|</span>
<span class="lute-neck">       |<span class="lute-strings">--</span>|</span>
<span class="lute-neck">       |<span class="lute-strings">--</span>|</span>
<span class="lute-body">     / ~~~ \\</span>
<span class="lute-body">   /  ~~~~~~ \\</span>
<span class="lute-body">  /  ~~<span class="lute-hole">{  }</span>~~ \\</span>
<span class="lute-body"> |  ~~~<span class="lute-hole">{  }</span>~~~|</span>
<span class="lute-body">  \\__________/</span>
`;

    return (
        <div
                className="lute-icon"
                style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8' }}
                dangerouslySetInnerHTML={{ __html: luteArt }}
            />
    );
};

export default Bard;