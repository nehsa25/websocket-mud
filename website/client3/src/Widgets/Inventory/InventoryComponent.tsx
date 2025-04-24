import React from 'react';
import './InventoryComponent.scss';
import { ItemIcons, ItemType } from '../../Types/ItemTypes';

interface InventoryProps {
    items: {
        name: string;
        item_type: ItemType;
    }[];
}

const InventoryComponent: React.FC<InventoryProps> = ({ items }) => {
    return (
        <div className="inventory-container">
            <div className="inventory-title">Inventory</div>
            <div className="inventory-list">
                {items.map((item, index) => {
                    const itemTypeString = ItemType[item.item_type];
                    const icon = (ItemIcons as any)[itemTypeString] as string || '';
                    return (
                        <div key={index} className="inventory-item">
                            <span className="icon">{icon}</span>
                            {item.name}
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default InventoryComponent;