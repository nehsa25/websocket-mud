import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBed, faBoltLightning, faDrumstickBite, faFaceSmileBeam, faSkullCrossbones, faTint } from '@fortawesome/free-solid-svg-icons';
import './StatusComponent.scss';

interface StatusComponentProps {
    hungry: React.ReactNode;
    thirsty: React.ReactNode;
    poisoned: React.ReactNode;
    sleepy: React.ReactNode;
    resting: React.ReactNode;
    mood: React.ReactNode;
}

const StatusComponent: React.FC<StatusComponentProps> = ({ hungry, thirsty, poisoned, sleepy, resting, mood }) => {

    const getStatusClass = (status: React.ReactNode): string => {
        if (status) {
            return "status-good";
        } else if (status === false) {
            return "status-bad";
        } else {
            return "status-neutral";
        }
    };

    return (
        <div className="status">
            <div className={getStatusClass(hungry)}>{<FontAwesomeIcon icon={faDrumstickBite} />}</div>
            <div className={getStatusClass(thirsty)}>{<FontAwesomeIcon icon={faTint} />}</div>
            <div className={getStatusClass(poisoned)}>{<FontAwesomeIcon icon={faSkullCrossbones} />}</div>
            <div className={getStatusClass(sleepy)}>{<FontAwesomeIcon icon={faBoltLightning} />}</div>
            <div className={getStatusClass(resting)}>{<FontAwesomeIcon icon={faBed} />}</div>
            <div className={getStatusClass(mood)}>{<FontAwesomeIcon icon={faFaceSmileBeam} />}</div>
        </div>
    );
};

export default StatusComponent;