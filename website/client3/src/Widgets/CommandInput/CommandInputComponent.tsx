import React, {
    useState,
    useRef,
    useCallback
} from 'react';
import './CommandInputComponent.scss';
import {
    MudEvents
} from '../../Types/MudEvents';

interface CommandInputProps {
    socket: WebSocket | null;
    username: string;
    command: string;
    setCommand: React.Dispatch<React.SetStateAction<string>>;
}

const CommandInputComponent: React.FC<CommandInputProps> = ({
    socket,
    username,
    command,
    setCommand
}) => {
    const sendcommandarea = useRef<HTMLInputElement>(null);

    const sendCommand = useCallback((cmd: string): void => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const full_cmd = {
                "type": EventUtility.COMMAND,
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

    return (
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
    );
};

export default CommandInputComponent;