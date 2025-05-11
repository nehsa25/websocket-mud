import './Human.scss';

import React from 'react';

interface HumanProps {
    disabled?: boolean;
    className?: string;
    eyecolor?: string;
    haircolor?: string;
    hairstyle?: string;
    body_type?: string;
    facial_hair?: string;
}

const human: React.FC<HumanProps> = ({
    disabled,
    className,
    eyecolor,
    haircolor,
    hairstyle,
    body_type,
    eyebrows,
    facial_hair,
}) => {
    let hair = '';
    let eyes = 'O';
    let mouth = `\\    ----    /\n`;
    mouth += `  \\         /  \n`;
    mouth += `\\--------/`;    
    let bodyType = '';
    let longhair = '';

    // some colors do not have named value so we need to provide a hex value
    if (eyecolor == "hazel") {
        eyecolor = "#8F7753;";
    } else if (eyecolor == "black") {
        eyecolor = "#111;";
    }

    // --- Hair Styles ---
    const hairStyling = `color: ${haircolor || 'inherit'};`;
    if (hairstyle === 'none') {
        hair = `<span style="${hairStyling}">  _.--""--._\n .\'          \'.</span>`;
        longhair = '';
    } else if (hairstyle === 'bald') {
        hair = `<span style="${hairStyling}">  _.--""--._\n .\'          \'.</span>`;
        longhair = '';
    } else if (hairstyle === 'short') {
        hair = `<span style="${hairStyling}">  _.--""--._\n`;        
        hair += `///___\\\\\\'\\</span>`;
        longhair = '';
    } else if (hairstyle === 'longhair') {
        hair = `<span style="${hairStyling}">   _.--""--._\n`;
        hair += ` /.________.\'\\\n`;
        hair += ` | ___________ |</span>`;
        longhair = `<span style="${hairStyling}">\\\\\\</span>`;
    } else if (hairstyle === 'mohawk') {
        hair = `<span style="${hairStyling}">   ||/</span>\n`;
        hair += `<span style="${hairStyling}">    |/| </span>\n`;
        hair += `<span style="${hairStyling}">   ||/</span>\n`;
        hair += `<span style="${hairStyling}">   _.--""--._\n /.________.\'\\</span>\n`;
        longhair = '';
    } else {
        hair = `<span style="${hairStyling}">   _.--""--._\n .\'          \'.</span>`;
        longhair = '';
    }

    // --- Eye Color ---
    const eyeStyling = `color: ${eyecolor || 'inherit'};`;
    eyes = `<span style="${eyeStyling}">${eyes}</span>`;

    // --- Facial Hair ---
    const facialHairStyle = `color: ${haircolor || 'inherit'};`;
    if (facial_hair === '') {
        mouth = `\\              /\n`;
        mouth += `\\    ----    /\n`;
        mouth += `  \\          /  \n`;
        mouth += `\\--------/`;
    } else if (facial_hair === 'beard') {
        mouth = `<span style="${facialHairStyle}">\\\\\\ ------- ///</span>\n`;
        mouth += `<span style="${facialHairStyle}">\\\\</span>  ---- <span style="${facialHairStyle}">//</span>\n`;
        mouth += `<span style="${facialHairStyle}">   \\-----//  </span>\n`;
    } else if (facial_hair === 'mustache') {
        mouth = `\\<span style="${facialHairStyle}">    -------    </span>/\n`;
        mouth += `\\     '---'     /`;
    } else if (facial_hair === 'goatee') {
        mouth = `\\<span style="${facialHairStyle}">    \\\\\\////    </span>/\n`;
        mouth += `\\   <span style="${facialHairStyle}">\\</span>'---'<span style="${facialHairStyle}">/</span>   /\n`;
        mouth += `\\    <span style="${facialHairStyle}">----</span>    /\n`;
        mouth += `  \\         /  \n`;
        mouth += `\\--------/`;
    } else if (facial_hair === 'sideburns') {
        mouth = `<span style="${facialHairStyle}">\\</span>              <span style="${facialHairStyle}">/</span>\n`;
        mouth += `<span style="${facialHairStyle}">\\</span>    ----    <span style="${facialHairStyle}">/</span>\n`;
        mouth += `  \\         /  \n`;
        mouth += `\\--------/`;
    } 

    // --- eye brows ---
    if (body_type === 'none') {
        bodyType = '----\n'
        bodyType += '--|  |--\n'
        bodyType += '  |  |  \n'
        bodyType += '  |  |  \n'
        bodyType += '----'
    } else if (body_type === 'thin') {
        bodyType = '----\n'
        bodyType += '--|  |--\n'
        bodyType += '  |  |  \n'
        bodyType += '  |  |  \n'
        bodyType += '----'
    } else if (body_type === 'average') {
        bodyType = '------\n'
        bodyType += '--|    |--\n'
        bodyType += '  |    |  \n'
        bodyType += '  |    |  \n'
        bodyType += '------'
    } else if (body_type === 'large') {
        bodyType = '------\n'
        bodyType += '--|      |--\n'
        bodyType += '  |      |  \n'
        bodyType += '  |      |  \n'
        bodyType += '------'
    } else {
        bodyType = '--------\n'
        bodyType += '--|        |--\n'
        bodyType += '  |        |  \n'
        bodyType += '  |        |  \n'
        bodyType += '-------'
    }

    // --- Body Type ---
    if (body_type === 'none') {
        bodyType = '----\n'
        bodyType += '--|  |--\n'
        bodyType += '  |  |  \n'
        bodyType += '  |  |  \n'
        bodyType += '----'
    } else if (body_type === 'thin') {
        bodyType = '----\n'
        bodyType += '--|  |--\n'
        bodyType += '  |  |  \n'
        bodyType += '  |  |  \n'
        bodyType += '----'
    } else if (body_type === 'average') {
        bodyType = '------\n'
        bodyType += '--|    |--\n'
        bodyType += '  |    |  \n'
        bodyType += '  |    |  \n'
        bodyType += '------'
    } else if (body_type === 'large') {
        bodyType = '------\n'
        bodyType += '--|      |--\n'
        bodyType += '  |      |  \n'
        bodyType += '  |      |  \n'
        bodyType += '------'
    } else {
        bodyType = '--------\n'
        bodyType += '--|        |--\n'
        bodyType += '  |        |  \n'
        bodyType += '  |        |  \n'
        bodyType += '-------'
    }

    const humanFaceArt = `
<span class="face">
${hair}
/  <span class="eyebrows">^^</span>     <span class="eyebrows">^^</span>  \\
/    ${eyes}      ${eyes}   \\
|               |
|       <span class="nose">^</span>       |
${mouth}
 ${longhair}|${longhair}
${bodyType}
  \\   /
  // \\\\
  |   |
</span>
  `;

    return (
        <div
            className="lute-icon"
            style={{ fontFamily: 'monospace', margin: 0, lineHeight: '0.8' }}
            dangerouslySetInnerHTML={{ __html: humanFaceArt }}
        />
    );
};

export default human;