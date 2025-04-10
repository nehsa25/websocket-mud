import React, {
    useRef,
    useEffect,
    useCallback
} from 'react';

import {
    Box
} from "@chakra-ui/react";

import {
    MudEvents
} from './Types/MudEvents';

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
    const sendcommandarea = useRef<HTMLInputElement>(null);

    // Scrolling effect
    useEffect(() => {
        if (scrollMe.current) {
            setTimeout(() => {
                if (scrollMe.current) {
                    scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
                }
            }, 0);
        }
    }, [mudEvents]);

    const sendCommand = useCallback((cmd: string): void => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const full_cmd = {
                "type": MudEvents.COMMAND,
                "cmd": cmd,
                "extra": {
                    "name": username.trim() || "",
                }
            };
            console.log("Sending: ");
            console.log(full_cmd);
            socket.send(JSON.stringify(full_cmd));
            setCommand(""); // Clear the input after sending
        } else {
            console.log("Websocket not connected");
        }
    }, [socket, username, setCommand]);

    const sendKeyCommand = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            sendCommand(command);
        }
    };

    const handleDataClick = () => {
        if (sendcommandarea.current) {
            sendcommandarea.current.focus();
        }
    };

    return (
        <>
            <div className="column1">
                <div className="map-container">
                    <img
                        src={mapImageName}
                        className="map"
                    />
                </div>
                <div className="data" ref={scrollMe} onClick={handleDataClick}>
                    {mudEvents.map((event, index) => {
                        return (
                            <Box key={index}>
                                {React.isValidElement(event) ? (
                                    React.cloneElement(event, {
                                        style: {
                                            ...(event.props as any).style || {},
                                            display: 'inline', // Or 'block' depending on your layout needs
                                        },
                                    })
                                ) : (
                                    event
                                )}
                            </Box>
                        );
                    })}
                </div>
                <div className="command-input">
                    <input
                        ref={sendcommandarea}
                        type="text"
                        value={command}
                        onChange={(e) => setCommand(e.target.value)}
                        onKeyDown={sendKeyCommand}
                        placeholder="Type a command here and press <ENTER>. (e.g. type 'say Hi'<ENTER> to say hello)"
                        className="input-field"
                    />
                </div>
            </div>
        </>
    );
};

export default Game;