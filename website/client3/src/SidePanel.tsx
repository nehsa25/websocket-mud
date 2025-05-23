import React from 'react';
import './SidePanel.scss';
import InventoryComponent from './Widgets/Inventory/InventoryComponent';
import StatusComponent from './Widgets/Status/StatusComponent';
import HealthBarComponent from './Widgets/HealthBar/HealthBarComponent';
import RoomImageComponent from './Widgets/RoomImage/RoomImageComponent';

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
                    <div className="sidepanel-grid">
                        <div className="username"> {title} </div>
                        <div className="healthbar-component">
                            <HealthBarComponent health={health} />
                        </div>
                        <div className="roomimage-component">
                            <RoomImageComponent roomImageName={roomImageName} />
                        </div>
                        <div className="status-component">
                            <StatusComponent hungry={hungry}
                                thirsty={thirsty}
                                poisoned={poisoned}
                                sleepy={sleepy}
                                resting={resting}
                                mood={mood}
                            />
                        </div>
                        <div className="inventory-component">
                            <InventoryComponent inventory={inventory} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SidePanel;