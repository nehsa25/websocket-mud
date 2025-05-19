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
    const [roomName, setRoomName] = useState<string>("");
    const [roomDescription, setRoomDescription] = useState<string>("");
    const [roomCharacters, setRoomCharacters] = useState<string>("");
    const [roomNpcs, setRoomNpcs] = useState<string>("");
    const [roomItems, setRoomItems] = useState<string>("");
    const [roomExits, setRoomExits] = useState<string>("");

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
        if (data) {
            console.log("Room Data", data);
            setRoomName(data.name || '');
            setRoomDescription(data.description || '');
            setRoomCharacters(data.characters || '');
            setRoomNpcs(data.npcs || '');
            setRoomItems(data.items || '');
            setRoomExits(data.exits || '');
        }
    }, [data]);

    return (
        <Box>
            {data && (
                <>
                    <div className="room">
                        <div className="room-title">
                            {roomName}
                        </div>

                        {roomDescription && (
                            <div className="room-description-message">
                                {colorizeMessage(addBar(roomDescription))}
                            </div>
                        )}

                        {roomCharacters && (
                            <div className="room-people-container">
                                <span className="room-section-title">People: </span>
                                <span className="room-section-value">{roomCharacters}</span>
                            </div>
                        )}


                        {roomNpcs && (
                            <div className="room-npcs-container">
                                <span className="room-section-title">NPCs: </span>
                                <span className="room-section-value">{roomNpcs}</span>
                            </div>
                        )}

                        {roomItems && (
                            <div className="room-items-container">
                                <span className="room-section-title">Items: </span>
                                <span className="room-section-value">{roomItems}</span>
                            </div>
                        )}


                        {roomExits && (
                            <div className="room-exits-container">
                                <span className="room-section-title">Exits: </span>
                                <span className="room-section-value">{roomExits}</span>
                            </div>
                        )}

                    </div>
                </>
            )
            }
        </Box >
    );
};

export default Room;