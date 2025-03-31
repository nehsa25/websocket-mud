import React, { useState, useRef, useEffect } from 'react';
import './App.css';
import { MudEvents } from './Types/MudEvents.ts';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar, faSmile, faTint } from '@fortawesome/free-solid-svg-icons';
import { MudStatuses, MudStatusIcons } from './Types/MudStatuses.ts';
import ReactDOMServer from 'react-dom/server';

function App() {
    // State variables for dynamic data
    const [title, setCurrentRoomTitle] = useState<string>("Coggle");
    const [roomDescription, setCurrentRoomDescription] = useState<string>("");
    const [npcs, setCurrentRoomNpcs] = useState<string>("");
    const [items, setCurrentRoomItems] = useState<string>("");
    const [exits, setCurrentRoomExits] = useState<string>("");
    const [extraLook, setExtraLook] = useState<string>("");
    const [health, setHealth] = useState<string>("");
    const [inventory, setInventory] = useState<string[]>([]);
    const [command, setCommand] = useState<string>("");
    const [mudEvents, setMudEvents] = useState<string[]>([]);
    const [usersConnected, setUsersConnected] = useState<number>(0);
    const [mapImageName, setMapImageName] = useState<string>("");
    const [roomImageName, setRoomImageName] = useState<string>("");
    const [miniMap, setMiniMap] = useState<string>("");
    const [isResting, setIsResting] = useState<boolean>(false);
    const [statuses, setStatuses] = useState<MudStatuses[]>([]);
    const [hungry, setHungry] = useState<JSX.Element>(<FontAwesomeIcon icon={faSmile} />);
    const [thirsty, setThirsty] = useState<JSX.Element>(<FontAwesomeIcon icon={faTint} />);
    const [mood, setMood] = useState<JSX.Element>(<FontAwesomeIcon icon={faSmile} />);
    const [worldName, setWorldName] = useState<string>("NehsaMUD");

    // Modal state
    const [showUsernameModal, setShowUsernameModal] = useState<boolean>(false);
    const [username, setUsername] = useState<string>('');

    // WebSocket state
    const [socket, setSocket] = useState<WebSocket | null>(null);

    // Refs for scrolling and input
    const scrollMe = useRef<HTMLDivElement>(null);
    const sendcommandarea = useRef<HTMLInputElement>(null);

    // WebSocket connection setup
    useEffect(() => {
        const ws = new WebSocket('ws://localhost:60049');

        ws.onopen = () => {
            console.log('Connected to WebSocket server');
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                processEvent(data);
            } catch (error) {
                console.error('Error parsing JSON:', error);
                console.log('Raw message:', event.data);
            }
        };

        ws.onclose = () => {
            console.log('Disconnected from WebSocket server');
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
        };

        setSocket(ws);

        return () => {
            ws.close();
        };
    }, []);

    // Function to handle command input
    const sendKeyCommand = (event: React.KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter') {
            sendCommand(command);
        }
    };

    // Effect to scroll to the bottom of the chat log
    useEffect(() => {
        if (scrollMe.current) {
            scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
        }
    }, [mudEvents]);

    // Function to generate the welcome message HTML
    const generateWelcomeMessage = (worldName: string): string => {
        const starTeal = <FontAwesomeIcon icon={faStar} className="color-teal" />;
        const starPurple = <FontAwesomeIcon icon={faStar} className="color-purple" />;
        const starRed = <FontAwesomeIcon icon={faStar} className="color-red" />;
        const starYellow = <FontAwesomeIcon icon={faStar} className="color-yellow" />;
        let welcome = "";
        welcome += " Welcome to the NehsaMud and the world of ";
        welcome += convertReactElementToString(
            <>
                {starTeal}
                {starPurple}
                {starRed}
                {starYellow}
            </>
        );
        welcome += `<span class="important">${worldName}</span>`;
        welcome += convertReactElementToString(
            <>
                {starYellow}
                {starRed}
                {starPurple}
                {starTeal}
            </>
        );
        welcome += `<br/><br/>`;
        welcome += ` My son, Ethan, and I are working on this project. It's not just a game but a platform for continuous learning and exploration. We use Python, React, TypeScript, Golang, C#, and various other libaries, tools, and AI within Illisurom, all aiming to create an engaging game and educational experience.`;
        welcome += ` <br/><br/>Why a MUD?`;
        welcome += ` <br/>It's a tribute to one of the most underappreciated types of game ever created: <span class="importantish">text-based multi-user dungeon (&quot;MUDs&quot;)</span>. MUDs were not just challenging and fast-paced, but also highly social and encouraging. In fact, I met my wife playing a MUD.`;
        welcome += ` <br/><br/>Some of the features (all in various states of completion):`;
        welcome += ` <ul class="condensed">`;
        welcome += ` <li>Client is built using React and TypeScript.</li>`;
        welcome += ` <li>All the images are created via AI. More information on that in the aimage">AI Image Generation</a></li>`;
        welcome += ` <li>All NPC and monster dialog is AI provided via Gemini">Google Gemini</a>.</li>`;
        welcome += ` <li>All maps are dynamically created based on the world and where the user is (using Dot and Pydot</a>).</li>`;
        welcome += ` <li>Various NPCs can interact with the real world, including scaping webpages, the weather, or other data, and return it in-game.</li>`;
        welcome += ` </ul>`;
        welcome += ` <br/><br/>Lastly, NehsaMUD is a side project.  We want to recreate an old game using modern technologies.  `;
        welcome += ` Please understand that NehsaMUD is a side project. It's perpetually mostly broken...<br/>`;
        welcome += ` <br/><h4 class="important">We hope you like it!</h4>`;

        return welcome;
    };

    // Function to colorize the message
    const colorizeMessage = (message: string): string => {
        const colors = ["red", "green", "blue", "white", "yellow", "cyan", "magenta", "black", "gray", "grey",
            "orange", "teal", "maroon", "olive", "navy", "lime", "aqua", "silver", "crimson", "purple", "brown", "pink"];

        let coloredMessage = message;
        colors.forEach(replaceValue => {
            const findExpression = new RegExp(`\\s(${replaceValue})\\s|\\s(${replaceValue}(?=\\S*['-])([a-zA-Z'-]+))`, 'gi');
            coloredMessage = coloredMessage.replace(findExpression, (match) => {
                return `<span class="color-${replaceValue}">${match}</span>`;
            });
        });
        return coloredMessage;
    };

    // Function to add a dashed border around the string
    const addBorder = (message: string): string => {
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
        return `<hr class="hr-border" /><span class="room-title">${desc}<br/>| ${roomTitle} |<br/>${desc}</span>`;
    };

    // Function to add a bar under the string
    const addBar = (message: string): string => {
        return `${message}<hr class="hr-border" />`;
    };

    const pushGenericEvent = (message: string): void => {
        setMudEvents(prevEvents => [...prevEvents, message]);
        // Scroll to bottom after adding a new event
        if (scrollMe.current) {
            scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
        }
    }

    const convertReactElementToString = (reactContent: React.JSX.Element): string => {
        return ReactDOMServer.renderToString(reactContent);
    };

    // Combined effect for scrolling, triggers whenever mudEvents changes
    useEffect(() => {
        if (scrollMe.current) {
            // Use setTimeout to ensure scroll happens after render commit
            setTimeout(() => {
                if (scrollMe.current) {
                    scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
                }
            }, 0);
        }
    }, [mudEvents]);


    const pushRoomEvent = (data: any): void => {
        let roommessage = "";

        if (data.name != "") {
            roommessage += "<br><span class=\"room-message\">" + addBorder(data.name) + "</span>";
        }

        // check if there's a room descrption
        if (data.description != "") {
            let description = colorizeMessage(addBar(data.description));
            roommessage += "<br><span class=\"room-description-message\">" + description + "</span>";
        }

        // check for people
        if (data.players != "") {
            roommessage += "<br><span class=\"people1-message\">People: </span><span class=\"people2-message\">" + data.players + "</span>";
        }

        // check for monsters
        if (data.npcs != "") {
            roommessage += "<br><span class=\"npcs1-message\">" + data.npcs + "</span>";
        }

        // check for items
        if (data.items != "") {
            roommessage += "<br><span class=\"items1-message\">You see: </span><span class=\"items2-message\">" + data.items + "</span>";
        }

        // check for available exits
        if (data.exits != "") {
            roommessage += "<br><span class=\"exits1-message\">Exits: </span><span class=\"exits2-message\">" + data.exits + "</span>";
        }

        setMudEvents(prevEvents => [...prevEvents, roommessage]);
    }

    const sendCommand = (cmd: string): void => {
        if (socket && socket.readyState === WebSocket.OPEN) {
            const full_cmd = {
                "type": MudEvents.COMMAND,
                "cmd": cmd,
                "extra": {
                    "name": username.trim() || "Coggles",
                }
            };
            console.log("Sending: ");
            console.log(full_cmd);
            socket.send(JSON.stringify(full_cmd));
            setCommand(""); // Clear the input after sending
        } else {
            console.log("Websocket not connected");
        }
    };

    // Function to process incoming events and update state
    const processEvent = (data: any): void => {
        switch (data.type) {
            case MudEvents.WELCOME:
                pushGenericEvent(data.message);
                break;
            case MudEvents.BOOK:
                pushGenericEvent(`<span class="book-message">${data.book?.title} by ${data.book?.author}</span>`);
                break;
            case MudEvents.USERNAME_REQUEST:
                setWorldName(data.world_name || "NehsaMUD");
                setShowUsernameModal(true);
                const welcomeMessageHtml = generateWelcomeMessage(data.world_name || "NehsaMUD");
                pushGenericEvent(welcomeMessageHtml);
                break;
            case MudEvents.DUPLICATE_NAME:
                pushGenericEvent(`<span class="error-message">That username is already taken.</span>`);
                break;
            case MudEvents.INVALID_NAME:
                pushGenericEvent(`<span class="error-message">Invalid username. Please use only letters and numbers. Name must be at least 3 characters long.</span>`);
                break;
            case MudEvents.EVENT:
                pushGenericEvent(`<span class="event-message">${data.message}</span>`);
                break;
            case MudEvents.INFO:
                pushGenericEvent(`<span class="info-message">${data.message}</span>`);
                break;
            case MudEvents.ANNOUCEMENT:
                pushGenericEvent(`<span class="announcement-message">${data.message}</span>`);
                break;
            case MudEvents.TIME:
                pushGenericEvent(`<span class="time-message">${data.time}</span>`);
                break;
            case MudEvents.CHANGE_NAME:
                setCurrentRoomTitle(data.name);
                pushGenericEvent(`<span class="info-message">Your name has been changed to ${data.name}.</span>`);
                break;
            case MudEvents.COMMAND:
                pushGenericEvent(`<span class="command-message">${data.message}</span>`);
                break;
            case MudEvents.YOU_ATTACK:
                pushGenericEvent(`<span class="attack-message">${data.message}</span>`);
                break;
            case MudEvents.INVENTORY:
                setInventory(data.inventory?.items?.map((item: any) => item.name) || []);
                break;
            case MudEvents.ERROR:
                pushGenericEvent(`<span class="error-message">${data.message}</span>`);
                break;
            case MudEvents.ATTACK:
                pushGenericEvent(`<span class="attack-message">${data.message}</span>`);
                break;
            case MudEvents.HEALTH:
                setHealth(`${data.statuses?.current_hp}/${data.statuses?.max_hp}`);
                setIsResting(data.is_resting || false);
                if (Array.isArray(data.statuses)) {
                    setStatuses(data.statuses);
                } else {
                    setStatuses([]);
                }
                break;
            case MudEvents.HELP:
                // Handle help
                let helpMessage = "";
                if (Array.isArray(data.help_commands)) {
                    helpMessage += "<span class=\"help-message\">Available commands:</span><ul>";
                    data.help_commands.forEach((commandHelp: any) => {
                        helpMessage += `<li><span class="help-command">${commandHelp.command}</span> - <span class="help-description">${commandHelp.description}</span>`;
                        if (commandHelp.examples && commandHelp.examples.length > 0) {
                            helpMessage += "<ul>Examples:";
                            commandHelp.examples.forEach((example: string) => {
                                helpMessage += `<li>${example}</li>`;
                            });
                            helpMessage += "</ul>";
                        }
                        helpMessage += "</li>";
                    });
                    helpMessage += "</ul>";
                } else {
                    helpMessage = `<span class="help-message">${data.message}</span>`;
                }
                pushGenericEvent(helpMessage);
                break;
            case MudEvents.REST:
                setIsResting(data.is_resting || false);
                pushGenericEvent(`<span class="rest-message">You are now resting.</span>`);
                break;
            case MudEvents.ROOM_IMAGE:
                setRoomImageName(data.room_image_name);
                break;
            case MudEvents.ROOM:
                setCurrentRoomTitle(data.name || "NehsaMud");
                setCurrentRoomDescription(data.description || "");
                setCurrentRoomNpcs(data.npcs || '');
                setCurrentRoomItems(data.items || '');
                setCurrentRoomExits(data.exits || '');
                pushRoomEvent(data);
                break;
            case MudEvents.HUNGER:
                setHungry(data.hunger || <FontAwesomeIcon icon={faSmile} />);
                break;
            case MudEvents.THIRST:
                setThirsty(data.thirst || <FontAwesomeIcon icon={faTint} />);
                break;
            case MudEvents.MOOD_CHANGED:
                setMood(data.mood || <FontAwesomeIcon icon={faSmile} />);
                break;
            case MudEvents.CLIENT_LIST:
                pushGenericEvent(`<span class="client-list-message">Users connected: ${data.players}</span>`);
                break;
            default:
                console.error("unsupported event: " + data.type);
                break;
        }
    };

    // Function to handle username submission
    const handleUsernameSubmit = () => {
        if (username.trim() !== '') {
            if (socket && socket.readyState === WebSocket.OPEN) {
                const response = { type: MudEvents.USERNAME_ANSWER, username: username.trim() };
                socket.send(JSON.stringify(response));
                setCurrentRoomTitle(username.trim()); // Update the title state
                setShowUsernameModal(false); // Close the modal
            } else {
                console.log("Websocket not connected");
            }
        }
    };

    return (
        <div className="game-container">
            <div className="top-bar">
                <div className="title">{title}</div>
                <div className="health">HEALTH {health}</div>
            </div>

            <div className="main-grid">
                <div className="column1">
                    <div className="data" ref={scrollMe}>
                        {mudEvents.map((event, index) => (
                            <div key={index} dangerouslySetInnerHTML={{ __html: event }}></div>
                        ))}
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
                <div className="rightSideBar">
                    <div className="side-panel">
                        <div className="scrollable-content">
                            <div>
                                <div className="status">
                                    <div>HUNGRY {hungry}</div>
                                    <div>THIRSTY {thirsty}</div>
                                    <div>
                                        STATUSES
                                        {Array.isArray(statuses) && statuses.map((status, index) => (
                                            <>{MudStatusIcons[status]}</>
                                        ))}
                                    </div>
                                    <div>MOOD {mood}</div>
                                </div>
                                <div className="inventory">
                                    INVENTORY
                                    <ul>
                                        {inventory.map((item, index) => (
                                            <li key={index}>{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div className="image-placeholder">
                            {roomImageName && <img src={"../mud-images/rooms/" + roomImageName} alt="Room" />}
                        </div>
                    </div>
                </div>
            </div>

            {/* Basic Modal */}
            {showUsernameModal && (
                <div className="modal">
                    <div className="modal-content">
                        <h2>Enter Username</h2>
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            onKeyDown={(e) => {
                                if (e.key === 'Enter') {
                                    handleUsernameSubmit();
                                }
                            }}
                        />
                        <button onClick={handleUsernameSubmit}>Submit</button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default App;