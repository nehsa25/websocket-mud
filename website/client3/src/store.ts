// store.ts
import { proxy } from 'valtio';
import { MudStatuses } from './Types/MudStatuses';
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSmile, faTint } from '@fortawesome/free-solid-svg-icons';

interface AppState {
    title: string;
    roomDescription: string;
    npcs: string;
    items: string;
    exits: string;
    extraLook: string;
    health: string;
    inventory: string[];
    command: string;
    mudEvents: React.ReactNode[];
    usersConnected: number;
    mapImageName: string;
    roomImageName: string;
    miniMap: string;
    isResting: boolean;
    statuses: MudStatuses[];
    hungry: React.ReactNode;
    thirsty: React.ReactNode;
    mood: React.ReactNode;
    worldName: string;
    showUsernameModal: boolean;
    username: string;
    socket: WebSocket | null;
}

enum Mood {
    NORMAL = "NORMAL",
    HAPPY = "HAPPY",
    SAD = "SAD",
    ANGRY = "ANGRY",
}

export const appState = proxy<AppState>({
    title: "",
    roomDescription: "",
    npcs: "",
    items: "",
    exits: "",
    extraLook: "",
    health: "",
    inventory: [],
    command: "",
    mudEvents: [],
    usersConnected: 0,
    mapImageName: "",
    roomImageName: "",
    miniMap: "",
    isResting: false,
    statuses: [],
    hungry: false,
    thirsty: false,
    mood: Mood.NORMAL,
    worldName: "NehsaMUD",
    showUsernameModal: false,
    username: '',
    socket: null,
});