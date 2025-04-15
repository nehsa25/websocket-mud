import React from 'react';
import './RoomImageComponent.scss';

interface RoomImageComponentProps {
    roomImageName: string;
}

const RoomImageComponent: React.FC<RoomImageComponentProps> = ({ roomImageName }) => {
    return (
        <div className="image-placeholder">
            {roomImageName && <img src={roomImageName} alt="Room" />}
        </div>
    );
};

export default RoomImageComponent;