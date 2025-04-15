import React, { useState, useEffect } from 'react';
import './MapComponent.scss';

interface MapComponentProps {
    mapImageName: string;
}

const MapComponent: React.FC<MapComponentProps> = ({ mapImageName }) => {
    const [isClicked, setIsClicked] = useState(false);
    const [svgContent, setSvgContent] = useState<string | null>(null);

    const handleClick = () => {
        setIsClicked(!isClicked);
    };

    const getMapImageNameWithoutMini = (name: string) => {
        return name.replace("_mini", "");
    };

    const mapImageSource = isClicked ? getMapImageNameWithoutMini(mapImageName) : mapImageName;

    return (
        <div 
            className={`map-container ${isClicked ? 'map-container-hover' : 'map-container-mini'}`} 
            onClick={handleClick}>
            {<img src={mapImageSource} alt="Mini Map" className="map-svg" />}
        </div>
    );
};

export default MapComponent;