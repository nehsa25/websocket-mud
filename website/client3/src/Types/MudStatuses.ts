import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSkull, faBed, faOm, faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import React from 'react';

export enum MudStatuses {
    POISONED = "POISONED",
    RESTING = "RESTING",
    MEDITATING = "MEDITATING",
    DAZZLED = "DAZZLED"
}

export type StatusIcons = {
    [key in MudStatuses]: any;
};

export const MudStatusIcons: StatusIcons = {
    [MudStatuses.POISONED]: React.createElement(FontAwesomeIcon, { icon: faSkull }),
    [MudStatuses.RESTING]: React.createElement(FontAwesomeIcon, { icon: faBed }),
    [MudStatuses.MEDITATING]: React.createElement(FontAwesomeIcon, { icon: faOm }),
    [MudStatuses.DAZZLED]: React.createElement(FontAwesomeIcon, { icon: faEyeSlash })
};