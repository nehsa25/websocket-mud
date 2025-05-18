import { LuCircleCheck } from "react-icons/lu"
import {
    useColorModeValue,
} from "./components/ui/color-mode";

import {
    Heading,
    Text,
    Box,
    List,
    Flex
} from "@chakra-ui/react";

import React, { useState, useRef, useEffect, useCallback } from 'react';
import './App.scss';
import { MudEvents } from './Types/MudEvents';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faStar, faSmile, faTint, faFrown } from '@fortawesome/free-solid-svg-icons';
import Game from './Game';
import SidePanel from './SidePanel';
import { appState } from './store';
import { useSnapshot } from 'valtio';
import { getUsername } from './Utils/utils';
import Room from './Widgets/Room/RoomComponent';
import Splash from './splash';
import LoginModal from './modals/Login';
import { LuExternalLink } from "react-icons/lu"

function App() {
    console.log("App: Entered");
    const snap = useSnapshot(appState);

    // State variables for dynamic data
    const [title, setCurrentRoomTitle] = useState<string>("");
    const [roomDescription, setCurrentRoomDescription] = useState<string>("");
    const [npcs, setCurrentRoomNpcs] = useState<string>("");
    const [items, setCurrentRoomItems] = useState<string>("");
    const [exits, setCurrentRoomExits] = useState<string>("");
    const [extraLook, setExtraLook] = useState<string>("");
    const [health, setHealth] = useState<string>("");
    const [inventory, setInventory] = useState<string[]>([]);
    const [command, setCommand] = useState<string>("");
    const [mudEvents, setMudEvents] = useState<React.ReactNode[]>([]);
    const [usersConnected, setUsersConnected] = useState<number>(0);
    const [mapImageName, setMapImageName] = useState<string>("");
    const [roomImageName, setRoomImageName] = useState<string>("");
    const [miniMap, setMiniMap] = useState<string>("");
    const [resting, setResting] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [hungry, setHungry] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [thirsty, setThirsty] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [poisoned, setPoisoned] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [sleepy, setSleepy] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [mood, setMood] = useState<React.ReactNode>(<FontAwesomeIcon icon={faSmile} />);
    const [worldName, setWorldName] = useState<string>("NehsaMUD");

    // Modal state
    const [showNewUserModal, setShowNewUserModal] = useState<boolean>(false);
    const [showUsernameModal, setShowUsernameModal] = useState<boolean>(false);
    const [username, setUsername] = useState<string>(getUsername());
    const [pin, setPin] = useState<string>("0000");

    // WebSocket state
    const [socket, setSocket] = useState<WebSocket | null>(null);

    // Refs for scrolling and input
    const [isFirstMessageReceived, setIsFirstMessageReceived] = useState<boolean>(false);
    const scrollMe = useRef<HTMLDivElement>(null);
    const sendcommandarea = useRef<HTMLInputElement>(null);

    // Use Chakra UI's useColorModeValue hook
    const importantColor = useColorModeValue("red.600", "red.400");
    const importantishColor = useColorModeValue("blue.600", "blue.400");

    // ensure we only attempt to initalize the websocket once
    let wsInstance: WebSocket | null = null;

    // Scroll to bottom after adding a new event
    const pushGenericEvent = useCallback((message: React.ReactNode): void => {
        console.log("pushGenericEvent: Entered");

        const styledMessage = (
            <Text as="span" className="latest-message">
                {message}
            </Text>
        );
        setMudEvents(prevEvents => [...prevEvents, styledMessage]);
        if (scrollMe.current) {
            scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
        }
        console.log("pushGenericEvent: Exited");
    }, [setMudEvents]);

    // Function to generate the welcome message HTML
    const generateWelcomeMessage = useCallback((
        worldName: string,
        importantColor: string,
        importantishColor: string
    ): JSX.Element => {
        console.log("generateWelcomeMessage: Entered");
        const starTeal = <FontAwesomeIcon icon={faStar} color="teal" />;
        const starPurple = <FontAwesomeIcon icon={faStar} color="purple" />;
        const starRed = <FontAwesomeIcon icon={faStar} color="red" />;
        const starYellow = <FontAwesomeIcon icon={faStar} color="yellow" />;

        const result = (
            <Box>
                <Text as="span">
                    Welcome to the NehsaMud and the world of{" "}
                    <Flex display="inline-flex">
                        {starTeal} {starPurple} {starRed} {starYellow}
                    </Flex>
                    <Text as="span" fontWeight="bold" color={importantColor}>
                        {worldName}
                    </Text>
                    <Flex display="inline-flex">
                        {starYellow} {starRed} {starPurple} {starTeal}
                    </Flex>
                </Text>

                <Heading size="md" mt={4}>
                    My son, Ethan, and I are making a MUD!
                </Heading>
                <Text as="span">
                    The intent is for NehsaMUD to not just a game but a platform for continuous learning and
                    exploration. We use Python, React, TypeScript, Golang, C#, and various
                    other libraries, tools, and AI within Illisurom, all aiming to create an
                    engaging world.
                </Text>

                <Heading size="md" mt={4}>
                    Why a MUD?
                </Heading>
                <Text as="span">
                    It's a tribute to one of the most underappreciated types of game ever
                    created:{" "}
                    <Box as="a" target="_blank" href="https://en.wikipedia.org/wiki/Multi-user_dungeon" fontWeight="semibold" color={importantishColor}>
                        text-based multi-user_dungeon ("MUDs")
                    </Box>
                    . MUDs were not just challenging and fast-paced, but also highly social
                    and encouraging. I met my wife playing a MUD.
                </Text>

                <Heading size="md" mt={4}>
                    Some of the features (all in various states of completion):
                </Heading>
                <List.Root gap="2" variant="plain" align="center">
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        Client is built using React, Vite, Chakra-UI, and TypeScript.
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        Backend is Python3, AsyncIO, Go, MariaDB, and C#
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        All the images are created via AI. More information on that in the <span style={{ paddingLeft: '5px' }}>
                            <Text as="a" target="_blank" href="https://www.nehsa.net/aiimage" color="blue.500">
                                AI Image Generation
                            </Text>
                        </span>
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        All NPC and monster dialog is AI provided via <span style={{ paddingLeft: '5px' }}>
                            <Text as="a" target="_blank" href="https://www.nehsa.net/gemini" color="blue.500">
                                Google Gemini
                            </Text></span>
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        All maps are dynamically created based on the world and where the user
                        is (using Dot and Pydot).
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        Various NPCs can interact with the real world, including scraping
                        webpages, the weather, or other data, and return it in-game.
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        Events between the websocket server and world state are handled asyncio message queues.
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        LocalStorage and JWT tokens are used for session management.
                    </List.Item>
                    <List.Item>
                        <List.Indicator asChild color="green.500">
                            <LuCircleCheck />
                        </List.Indicator>
                        Pins are stored securely using Argon2id hashing.
                    </List.Item>
                </List.Root>

                <Heading size="md" mt={4}>
                    Lastly, NehsaMUD is a side project.
                </Heading>

                <Text as="span">
                    We want to recreate an old game using modern technologies. Please
                    understand that NehsaMUD is a side project. It's perpetually mostly
                    broken...
                </Text>

                <Heading size="lg" mt={4} color={importantColor}>
                    We hope you like it!
                </Heading>
            </Box>
        );
        console.log("generateWelcomeMessage: Exited");
        return result;
    }, [importantColor, importantishColor]);

    // Function to process incoming events and update state
    const processEvent = useCallback((data: any): void => {
        console.log("processEvent: Enter for event: " + data.type);
        const ws = data[1];
        data = data[0];

        switch (data.type) {
            case MudEvents.WELCOME:
                pushGenericEvent(data.message);
                setCurrentRoomTitle(data?.name?.trim());
                localStorage.setItem("nehsamud", JSON.stringify(data));
                break;
            case MudEvents.BOOK:
                pushGenericEvent(<span className="book-message">{data.book?.title} by {data.book?.author}</span>);
                break;
            case MudEvents.USERNAME_REQUEST:
                setWorldName(data.world_name || "NehsaMUD");
                const welcomeMessage = generateWelcomeMessage(worldName, importantColor, importantishColor);
                pushGenericEvent(welcomeMessage);

                // check local storage for nehsamud object
                const nehsamud = localStorage.getItem("nehsamud");
                if (nehsamud) {
                    console.log("Found nehsamud in local storage: " + nehsamud);
                    try {
                        const parsedNehsamud = JSON.parse(nehsamud);
                        if (parsedNehsamud.name) {
                            setUsername(parsedNehsamud.name);
                            if (parsedNehsamud.token == null) {
                                // prompt for pin
                                setShowUsernameModal(true);
                            }

                            const response = {
                                type: MudEvents.USERNAME_ANSWER,
                                username: parsedNehsamud.name,
                                token: parsedNehsamud.token,
                                pin: parsedNehsamud.pin,
                            };

                            if (ws && ws.readyState === WebSocket.OPEN) {
                                console.log("Sending username to server: " + parsedNehsamud.name);
                                ws.send(JSON.stringify(response));
                            } else {
                                console.log("WebSocket not connected, cannot send username.");
                            }

                            setCurrentRoomTitle(parsedNehsamud.username);
                        } else {
                            throw new Error("Username not found in stored data");
                        }
                    } catch (error) {
                        console.error('Error parsing stored user data:', error);
                        //  Handle the error (e.g., clear the local storage, prompt for login)
                        localStorage.removeItem('nehsaUser');
                        setShowUsernameModal(true);
                        break;
                    }
                } else {
                    setShowUsernameModal(true);
                }
                break;
            case MudEvents.DUPLICATE_NAME:
                pushGenericEvent(<span className="error-message">That username is already taken.</span>);
                break;
            case MudEvents.INVALID_NAME:
                pushGenericEvent(<span className="error-message">Invalid username. Please use only letters and numbers. Name must be at least 3 characters long.</span>);
                break;
            case MudEvents.EVENT:
                pushGenericEvent(<span className="event-message">{data.message}</span>);
                break;
            case MudEvents.INFO:
                pushGenericEvent(<span className="info-message">{data.message}</span>);
                break;
            case MudEvents.ANNOUNCEMENT:
                pushGenericEvent(<span className="announcement-message">{data.message}</span>);
                break;
            case MudEvents.TIME:
                pushGenericEvent(<span className="time-message">{data.time}</span>);
                break;
            case MudEvents.CHANGE_NAME:
                setCurrentRoomTitle(data.name);
                pushGenericEvent(<span className="info-message">Your name has been changed to {data.name}.</span>);
                break;
            case MudEvents.COMMAND:
                pushGenericEvent(<span className="command-message">{data.message}</span>);
                break;
            case MudEvents.YOU_ATTACK:
                pushGenericEvent(<span className="attack-message">{data.message}</span>);
                break;
            case MudEvents.INVENTORY:
                setInventory(data.inventory?.items?.map((item: any) => item.name) || []);
                break;
            case MudEvents.ERROR:
                pushGenericEvent(<span className="error-message">{data.message}</span>);
                break;
            case MudEvents.ATTACK:
                pushGenericEvent(<span className="attack-message">{data.message}</span>);
                break;
            case MudEvents.HEALTH:
                console.log("health: " + data.current_hp + "/" + data.max_hp);
                setHealth(`${data.current_hp}/${data.max_hp}`);

                setResting(data.statuses.is_resting == false ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);

                setThirsty(data.statuses.is_thirsty == false ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);

                setHungry(data.statuses.is_hungry == false ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);

                setMood(data.statuses.mood.value ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);

                setPoisoned(data.statuses.is_poisoned == false ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);

                setSleepy(data.statuses.is_sleepy == false ?
                    <FontAwesomeIcon icon={faSmile} /> : <FontAwesomeIcon icon={faFrown} />);
                break;
            case MudEvents.HELP:
                // Handle help
                let helpMessage = "";
                if (Array.isArray(data.help_commands)) {
                    helpMessage += "<ul>";
                    data.help_commands.forEach((commandHelp: any) => {
                        helpMessage += `<li><span class="help-command">${commandHelp.command}</span> - <span className="help-description">${commandHelp.description}</span>`;
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
                    helpMessage = `<span className="help-message">{data.message}</span>`;
                }
                pushGenericEvent(helpMessage);
                break;
            case MudEvents.REST:
                setResting(data.is_resting || false);
                pushGenericEvent(<span className="rest-message">You are now resting.</span>);
                break;
            case MudEvents.ROOM_IMAGE:
                setRoomImageName(data.room_image_name);
                break;
            case MudEvents.ROOM:
                console.log("Room: " + data.room);
                pushGenericEvent(<Room data={data} />);
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
                pushGenericEvent(<span className="client-list-message">Users connected: {data.players}</span>);
                break;
            case MudEvents.MAP_EVENT:
                setMapImageName(data.map_image_name_mini);
                break;
            default:
                console.error("unsupported event: " + data.type);
                break;
        }
        console.log("processEvent: Exited");
    }, [
        generateWelcomeMessage,
        pushGenericEvent,
        setCurrentRoomDescription,
        setCurrentRoomExits,
        setCurrentRoomItems,
        setCurrentRoomNpcs,
        setHealth,
        setHungry,
        setInventory,
        setResting,
        setMood,
        setRoomImageName,
        setPoisoned,
        setSleepy,
        setThirsty,
        worldName,
        importantColor,
        importantishColor
    ]);

    const newUser = useCallback(() => {
        console.log("newUser: Entered");
        setShowNewUserModal(true);
    }, []);

    // WebSocket connection setup
    useEffect(() => {
        console.log("WebSocket useEffect: Entered");

        if (wsInstance) {
            console.log("WebSocket already initialized, skipping.");
            return;
        }

        const ws = new WebSocket(import.meta.env.VITE_WSS_LOCATION ?? 'wss://mud-be.3aynhf1tn4zjy.us-west-2.cs.amazonlightsail.com');
        wsInstance = ws;
        ws.onopen = () => {
            console.log('Connected to WebSocket server');
        };

        ws.onmessage = (event) => {
            try {
                setIsFirstMessageReceived(true);
                const data = JSON.parse(event.data);
                console.log('Received data:', data);
                processEvent([data, ws]);
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
            console.log('Closing WebSocket connection on unmount');
            if (ws.readyState === WebSocket.OPEN) {
                try {
                    ws.close();
                } catch (error) {
                    console.error('Error closing WebSocket:', error);
                }
            }
        };
    }, []);
    console.log("WebSocket useEffect: Exited");

    // Combined effect for scrolling, triggers whenever mudEvents changes
    useEffect(() => {
        console.log("Scrolling useEffect: Entered");
        if (scrollMe.current) {
            // Use setTimeout to ensure scroll happens after render commit
            setTimeout(() => {
                if (scrollMe.current) {
                    scrollMe.current.scrollTop = scrollMe.current.scrollHeight;
                }
            }, 0);
        }
        console.log("Scrolling useEffect: Exited");
    }, [mudEvents]);

    // State to manage whether the side panel is collapsed
    const [isSidePanelCollapsed, setIsSidePanelCollapsed] = useState(false);

    // Function to toggle the side panel collapse state
    const toggleSidePanel = () => {
        setIsSidePanelCollapsed(!isSidePanelCollapsed);
    };

    if (!isFirstMessageReceived) {
        return <Splash />;
    }

    console.log("App: Rendering");
    const result = (
        <div className="game-container">
            <div className="main-grid" style={{ gridTemplateColumns: isSidePanelCollapsed ? '1fr auto' : '3fr 1fr' }}>
                <div className="game-component">
                    <Game
                        socket={socket}
                        username={username}
                        title={title}
                        setTitle={setCurrentRoomTitle}
                        roomDescription={roomDescription}
                        setRoomDescription={setCurrentRoomDescription}
                        npcs={npcs} setNpcs={setCurrentRoomNpcs}
                        items={items}
                        setItems={setCurrentRoomItems}
                        exits={exits}
                        extraLook={extraLook}
                        setExtraLook={setExtraLook}
                        health={health}
                        setHealth={setHealth}
                        inventory={inventory}
                        setInventory={setInventory}
                        command={command}
                        setCommand={setCommand}
                        mudEvents={mudEvents}
                        setMudEvents={setMudEvents}
                        usersConnected={usersConnected}
                        setUsersConnected={setUsersConnected}
                        mapImageName={mapImageName}
                        setMapImageName={setMapImageName}
                        roomImageName={roomImageName}
                        setRoomImageName={setRoomImageName}
                        miniMap={miniMap}
                        setMinMap={setMiniMap}
                        isResting={resting}
                        setIsResting={setResting}
                        hungry={hungry}
                        setHungry={setHungry}
                        thirsty={thirsty}
                        setThirsty={setThirsty}
                        mood={mood}
                        setMood={setMood}
                        importantColor={importantColor}
                        importantishColor={importantishColor}
                        generateWelcomeMessage={generateWelcomeMessage}
                        isSidePanelCollapsed={isSidePanelCollapsed}
                    />
                </div>
                <div className="sidepanel-component">
                    <SidePanel
                        title={title}
                        health={health}
                        hungry={hungry}
                        thirsty={thirsty}
                        poisoned={poisoned}
                        sleepy={sleepy}
                        resting={resting}
                        mood={mood}
                        inventory={inventory}
                        roomImageName={roomImageName}
                        isCollapsed={isSidePanelCollapsed} // Pass the collapse state
                        toggleCollapse={toggleSidePanel} // Pass the toggle function
                    />
                </div>
            </div>

            <LoginModal
    socket={socket}
    showUsernameModal={showUsernameModal}
    setShowUsernameModal={setShowUsernameModal}
    showNewUserModal={showNewUserModal}
    setShowNewUserModal={setShowNewUserModal}
    username={username}
    setUsername={setUsername}
    pin={pin}
    setPin={setPin}
    setCurrentRoomTitle={setCurrentRoomTitle}
   />
        </div>
    );
    console.log("App: Exited");
    return result;
}

export default App;