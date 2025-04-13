import React, { useRef, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faBed, faBoltLightning, faDrumstickBite, faFaceSmileBeam, faSkullCrossbones, faTint } from '@fortawesome/free-solid-svg-icons';
import './SidePanel.scss';

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
    const healthDivRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function updateHealthBar(element: HTMLDivElement | null, health: string) {
            if (!element) return;
            console.log("Health string:", health); // Log the health string
            const [current, max] = health.split('/').map(Number);
            console.log("Current HP:", current, "Max HP:", max); // Log current and max HP
            const percentage = (current / max) * 100;
            console.log("Health percentage:", percentage); // Log the calculated percentage

            let barColor = 'red';
            if (percentage >= 80) {
                barColor = 'green';
            } else if (percentage >= 40) {
                barColor = 'yellow';
            }
            console.log("Bar color:", barColor); // Log the determined bar color

            element.style.setProperty('--health-width', `${percentage}%`);
            element.style.setProperty('--health-color', barColor);
        }

        if (healthDivRef.current) {
            updateHealthBar(healthDivRef.current, health);
        }
    }, [health]);

    return (
        <div className="rightSideBar">
            <div className="side-panel">
                <div className="scrollable-content">
                    <div className="side-panel-grid">
                        <div>
                            <div className="title"> {title} </div>
                            <div className="health" ref={healthDivRef}>
                                <span className="health-text">HEALTH {health}</span>
                            </div>
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
                    roomImageName && < img src={roomImageName} alt="Room" />
                }
                </div>
            </div>
        </div>
    );
};

export default SidePanel;