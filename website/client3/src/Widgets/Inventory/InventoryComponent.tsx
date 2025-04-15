import React from 'react';
import './InventoryComponent.scss';

interface InventoryComponentProps {
    inventory: string[];
}

const InventoryComponent: React.FC<InventoryComponentProps> = ({ inventory }) => {
    return (
        <div className="inventory-container">
            <div className="inventory-title"> INVENTORY </div>
            <ul className="inventory-list">{
                inventory.map((item, index) => (
                    <li key={index} > {item} </li>))
            }
            </ul>
        </div>
    );
};

export default InventoryComponent;