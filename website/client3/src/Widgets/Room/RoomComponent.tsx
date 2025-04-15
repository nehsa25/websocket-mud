import './RoomComponent.scss';

import React, {
    useCallback,
    useEffect,
    useState
} from 'react';
import {
    Box,
    Text
} from "@chakra-ui/react";
import {
    useColorModeValue
} from "../../components/ui/color-mode";

interface RoomProps {
    data: any;
}

const Room: React.FC<RoomProps> = ({
    data
}) => {
    console.log("Room: Entered");
    console.log("Room: data prop:", data);

    // Use Chakra UI's useColorModeValue hook
    const importantColor = useColorModeValue("red.600", "red.400");
    const importantishColor = useColorModeValue("blue.600", "blue.400");

    const [roomDescription, setRoomDescription] = useState<string>("");
    const [roomNpcs, setRoomNpcs] = useState<string>("");
    const [roomItems, setRoomItems] = useState<string>("");
    const [roomExits, setRoomExits] = useState<string>("");

    console.log("Room: State variables initialized:", {
        roomDescription,
        roomNpcs,
        roomItems,
        roomExits
    });

    const colorizeMessage = useCallback((message: string): JSX.Element => {
        console.log("colorizeMessage: Entered");
        const colors = ["red", "green", "blue", "white", "yellow", "cyan", "magenta", "black", "gray", "grey",
            "orange", "teal", "maroon", "olive", "navy", "lime", "aqua", "silver", "crimson", "purple", "brown", "pink"];

        let parts: React.ReactNode[] = [message];
        let newParts: React.ReactNode[] = [];

        colors.forEach(color => {
            parts.forEach((part, index) => {
                if (typeof part === 'string') {
                    const regex = new RegExp(`(\\s${color}\\s|\\s${color}(?=\\S*['-])([a-zA-Z'-]+))`, 'gi');
                    const split = (part as string).split(regex);
                    for (let i = 0; i < split.length; i++) {
                        if (i % 2 === 1) {
                            newParts.push(<span key={`${index}-${i}`} className={`color-${color}`}>{split[i]}</span>);
                        } else {
                            newParts.push(split[i]);
                        }
                    }
                } else {
                    newParts.push(part);
                }
            });
            parts = newParts;
            newParts = [];
        });
        console.log("colorizeMessage: Exited");
        return <>{parts}</>;
    }, []);

    // Function to add a dashed border around the string
    const addBorder = useCallback((message: string): JSX.Element => {
        console.log("addBorder: Entered");
        let roomTitle = message;
        roomTitle = roomTitle.replace(/---\\d*/g, ' ');
        let desc = "";
        const descriptionLength = roomTitle.length;
        if (descriptionLength < 160) {
            for (let i = 0; i < descriptionLength + 4; i++) {
                desc += '-';
            }
        } else {
            desc += "---------------------------------------------------------------------------------------------------------------------------------------------------------------";
        }
        console.log("addBorder: Exited");
        return (
            <>
                <hr className="hr-border" />
                <span className="room-title">
                    {desc}
                    <br />| {roomTitle} |<br />
                    {desc}
                </span>
            </>
        );
    }, []);

    // Function to add a bar under the string
    const addBar = useCallback((message: string): JSX.Element => {
        console.log("addBar: Entered");
        console.log("addBar: Exited");
        return (
            <>
                {message}
                <hr className="hr-border" />
            </>
        );
    }, []);

    useEffect(() => {
        console.log("Room: useEffect - data prop changed");
        if (data) {
            console.log("Room: useEffect - data is truthy");
            setRoomDescription(data.description || "");
            setRoomNpcs(data.npcs || '');
            setRoomItems(data.items || '');
            setRoomExits(data.exits || '');

            console.log("Room: useEffect - State variables updated:", {
                roomDescription: data.description || "",
                roomNpcs: data.npcs || '',
                roomItems: data.items || '',
                roomExits: data.exits || ''
            });
        } else {
            console.log("Room: useEffect - data is falsy");
        }
    }, [data]);

    const roomName = useCallback(() => {
        if (data && data.name) {
            return data.name.replace(/---\d+$/, '');
        }
        return '';
    }, [data]);

    console.log("Room: Rendering component");
    return (
        <Box>
            {data && (
                <>
                    <div className="room">
                        <div className="room-title">
                            {roomName()}
                        </div>

                        <div className="room-description-message">
                            {colorizeMessage(addBar(data.description))}
                        </div>

                        {data.players && (
                            <>
                                <div className="room-people-container">
                                    <span className="room-section-title">People: </span>
                                    <span className="room-section-value">{data.players}</span>
                                </div>
                            </>
                        )}


                        {data.npcs && (
                            <>
                                <div className="room-npcs-container">
                                    <span className="room-section-title">NPCs: </span>
                                    <span className="room-section-value">{data.npcs}</span>
                                </div>
                            </>
                        )}

                        {data.items && (
                            <>
                                <div className="room-items-container">
                                    <span className="room-section-title">Items: </span>
                                    <span className="room-section-value">{data.items}</span>
                                </div>
                            </>
                        )}


                        {data.exits && (
                            <>
                                <div className="room-exits-container">
                                    <span className="room-section-title">Exits: </span>
                                    <span className="room-section-value">{data.exits}</span>
                                </div>
                            </>
                        )}

                    </div>
                </>
            )
            }
        </Box >
    );
};

export default Room;