import './Game.scss';

import React, {
    useRef,
    useEffect
} from 'react';

import {
    Box
} from "@chakra-ui/react";

import {
    MudEvents
} from './Types/MudEvents';

import MapComponent from './Widgets/Map/MapComponent';
import CommandInputComponent from './Widgets/CommandInput/CommandInputComponent';

interface GameProps {
    socket: WebSocket | null;
    username: string;
    title: string;
    setTitle: React.Dispatch<React.SetStateAction<string>>;
    roomDescription: string;
    setRoomDescription: React.Dispatch<React.SetStateAction<string>>;
    npcs: string;
    setNpcs: React.Dispatch<React.SetStateAction<string>>;
    items: string;
    setItems: React.Dispatch<React.SetStateAction<string>>;
    exits: string;
    setExits: React.Dispatch<React.SetStateAction<string>>;
    extraLook: string;
    setExtraLook: React.Dispatch<React.SetStateAction<string>>;
    health: string;
    setHealth: React.Dispatch<React.SetStateAction<string>>;
    inventory: string[];
    setInventory: React.Dispatch<React.SetStateAction<string[]>>;
    command: string;
    setCommand: React.Dispatch<React.SetStateAction<string>>;
    mudEvents: React.ReactNode[];
    setMudEvents: React.Dispatch<React.SetStateAction<React.ReactNode[]>>;
    usersConnected: number;
    setUsersConnected: React.Dispatch<React.SetStateAction<number>>;
    mapImageName: string;
    setMapImageName: React.Dispatch<React.SetStateAction<string>>;
    roomImageName: string;
    setRoomImageName: React.Dispatch<React.SetStateAction<string>>;
    miniMap: string;
    setMinMap: React.Dispatch<React.SetStateAction<string>>;
    isResting: React.ReactNode;
    setIsResting: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    hungry: React.ReactNode;
    setHungry: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    poisoned: React.ReactNode;
    setPoisoned: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    sleepy: React.ReactNode;
    setSleepy: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    thirsty: React.ReactNode;
    setThirsty: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    mood: React.ReactNode;
    setMood: React.Dispatch<React.SetStateAction<React.ReactNode>>;
    importantColor: string;
    importantishColor: string;
    processEvent: (data: any) => void;
    generateWelcomeMessage: (worldName: string, importantColor: string, importantishColor: string) => JSX.Element;
}

import {
    MudStatuses
} from './Types/MudStatuses';

const Game: React.FC<GameProps> = ({
    socket,
    username,
    title,
    setTitle,
    roomDescription,
    setRoomDescription,
    npcs,
    setNpcs,
    items,
    setItems,
    exits,
    setExits,
    extraLook,
    setExtraLook,
    health,
    setHealth,
    inventory,
    setInventory,
    command,
    setCommand,
    mudEvents,
    setMudEvents,
    usersConnected,
    setUsersConnected,
    mapImageName,
    setMapImageName,
    roomImageName,
    setRoomImageName,
    miniMap,
    setMinMap,
    isResting,
    setIsResting,
    statuses,
    setStatuses,
    hungry,
    setHungry,
    thirsty,
    setThirsty,
    mood,
    setMood,
    importantColor,
    importantishColor,
    processEvent,
    generateWelcomeMessage
}) => {
    const scrollMe = useRef<HTMLDivElement>(null);

    // Scrolling effect
    useEffect(() => {
        if (scrollMe.current) {
            setTimeout(() => {
                if (scrollMe.current) {
                    scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
                }
            }, [mudEvents]);
        }
    }, [mudEvents]);

    return (
        <>
            <div className="game-column">
                <div className="game-map">
                    <MapComponent mapImageName={mapImageName} />
                </div>
                <div className="data" ref={scrollMe}>
                    {mudEvents.map((event, index) => {
                        return (
                            <Box key={index}>
                                {React.isValidElement(event) ? (
                                    React.cloneElement(event, {
                                        style: {
                                            ...(event.props as any).style || {},
                                            display: 'inline',
                                        },
                                    })
                                ) : (
                                    event
                                )}
                            </Box>
                        );
                    })}
                </div>
                <CommandInputComponent
                    socket={socket}
                    username={username}
                    command={command}
                    setCommand={setCommand}
                />
            </div>
        </>
    );
};

export default Game;