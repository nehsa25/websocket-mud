import React, { useRef, useEffect } from 'react';
import './HealthBarComponent.scss';

interface HealthBarComponentProps {
    health: string;
}

const HealthBarComponent: React.FC<HealthBarComponentProps> = ({ health }) => {
    const healthDivRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        function updateHealthBar(element: HTMLDivElement | null, health: string) {
            if (!element) return;
            console.log("Health string:", health);
            const [current, max] = health.split('/').map(Number);
            console.log("Current HP:", current, "Max HP:", max);
            const percentage = (current / max) * 100;
            console.log("Health percentage:", percentage);

            let barColor = 'red';
            if (percentage >= 80) {
                barColor = 'green';
            } else if (percentage >= 40) {
                barColor = 'yellow';
            }
            console.log("Bar color:", barColor);

            element.style.setProperty('--health-width', `${percentage}%`);
            element.style.setProperty('--health-color', barColor);
        }

        if (healthDivRef.current) {
            updateHealthBar(healthDivRef.current, health);
        }
    }, [health]);

    return (
        <div className="health" ref={healthDivRef}>
            <span className="health-text">HEALTH {health}</span>
        </div>
    );
};

export default HealthBarComponent;