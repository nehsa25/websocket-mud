import React from 'react';
import {
    MudStatuses,
    MudStatusIcons
} from './Types/MudStatuses';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBed, faBoltLightning, faDrumstickBite, faFaceSmileBeam, faFaceTired, faSkullCrossbones, faTint } from '@fortawesome/free-solid-svg-icons';

interface SidePanelProps {
    title: string;
    health: string;
    hungry: React.ReactNode;
    thirsty: React.ReactNode;
    poisoned: React.ReactNode;
    sleepy: React.ReactNode;
    resting: React.ReactNode;
    mood: React.ReactNode;
    inventory: string[];
    roomImageName: string;
}

const SidePanel: React.FC<SidePanelProps> = ({
    title,
    health,
    hungry,
    thirsty,
    poisoned,
    sleepy,
    resting,
    mood,
    inventory,
    roomImageName
}) => {
    return (
        <div className="rightSideBar">
            <div className="side-panel">
                <div className="scrollable-content">
                    <div className="side-panel-grid">
                        <div>
                            <div className="title"> {title} </div>
                            <div className="health"> HEALTH {health}</div>
                        </div>
                        <div className="status">
                            <div> <FontAwesomeIcon icon={faDrumstickBite} /> </div><div>{hungry}</div>
                            <div> <FontAwesomeIcon icon={faTint} /> </div><div>{thirsty}</div>
                            <div> <FontAwesomeIcon icon={faSkullCrossbones} /> </div><div>{poisoned}</div>
                            <div> <FontAwesomeIcon icon={faBoltLightning} /> </div><div>{sleepy}</div>
                            <div> <FontAwesomeIcon icon={faBed} /> </div><div>{resting}</div>
                            <div> <FontAwesomeIcon icon={faFaceSmileBeam} /> </div><div>{mood}</div>
                        </div>
                        <div className="inventory">
                            INVENTORY
                            <ul> {
                                inventory.map((item, index) => (
                                    <li key={index} > {item} </li>))
                            }
                            </ul>
                        </div>
                    </div>
                </div>
                <div className="image-placeholder"> {
                    roomImageName && < img src={
                        `../mud-images/rooms/${roomImageName}`
                    }
                        alt="Room" />
                }
                </div>
            </div>
        </div>
    );
};

export default SidePanel;