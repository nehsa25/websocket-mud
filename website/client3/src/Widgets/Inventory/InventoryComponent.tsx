import React from 'react';
import './InventoryComponent.scss';

interface InventoryComponentProps {
    inventory: string[];
}

const InventoryComponent: React.FC<InventoryComponentProps> = ({ inventory }) => {
    return (
        <div className="inventory-container">
            <div className="inventory-title"> INVENTORY </div>
            <div className="inventory-list">
                {inventory.map((item, index) => (
                    <div key={index} className="inventory-item">
                        {item}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default InventoryComponent;