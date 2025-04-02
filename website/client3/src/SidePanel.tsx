import React from 'react';
import {
    MudStatuses,
    MudStatusIcons
} from './Types/MudStatuses';

interface SidePanelProps {
    title: string;
    health: string;
    hungry: React.ReactNode;
    thirsty: React.ReactNode;
    statuses: MudStatuses[];
    mood: React.ReactNode;
    inventory: string[];
    roomImageName: string;
}

const SidePanel: React.FC<SidePanelProps> = ({
    title,
    health,
    hungry,
    thirsty,
    statuses,
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
                            <div> HUNGRY {hungry}</div>
                            <div> THIRSTY {thirsty} </div>
                            <div> STATUSES {
                                Array.isArray(statuses) && statuses.map((status, index) => (<
                                    React.Fragment key={
                                        index
                                    } > {
                                        MudStatusIcons[status]
                                    } </React.Fragment>
                                ))
                            }
                            </div>
                            <div>MOOD {mood}</div>
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