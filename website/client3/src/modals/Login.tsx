import './Login.scss';
import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { createListCollection, DataList, List, ListCollection, Portal } from "@chakra-ui/react";
import { Select } from "@chakra-ui/react";
import * as argon2 from 'argon2-wasm';
import { MudEvents } from '../Types/MudEvents';
import { Step, Stepper } from "react-form-stepper";
import SwordNext from '../react/SwordNext';
import { LuTriangleAlert } from 'react-icons/lu';

interface LoginModalProps {
    socket: WebSocket | null;
    showUsernameModal: boolean;
    setShowUsernameModal: (show: boolean) => void;
    showNewUserModal: boolean;
    setShowNewUserModal: (show: boolean) => void;
    username: string;
    setUsername: (username: string) => void;
    pin: string;
    setPin: (pin: string) => void;
    setCurrentRoomTitle: (title: string) => void;
}

interface MudRace {
    id: string;
    name: string;
    description: string;
    abilities: string[];
    playable: boolean;
    directives: string[];
    baseExperienceAdjustment: number;
}

interface MudClass {
    id: string;
    name: string;
    description: string;
    abilities: string[];
    playable: boolean;
    directives: string[];
    baseExperienceAdjustment: number;
}

const apiLocation = import.meta.env.VITE_API_LOCATION ?? 'wss://mud-be.3aynhf1tn4zjy.us-west-2.cs.amazonlightsail.com'

const LoginModal: React.FC<LoginModalProps> = ({
    socket,
    showUsernameModal,
    setShowUsernameModal,
    showNewUserModal,
    setShowNewUserModal,
    username,
    setUsername,
    pin,
    setPin,
    setCurrentRoomTitle
}) => {

    const [races, setRaces] = useState<any[]>([]);
    const [classes, setClasses] = useState<any[]>([]);
    const [activeStep, setActiveStep] = useState(0);
    const [repeatPin, setRepeatPin] = useState<string>("");
    const [firstname, setFirstName] = useState<string>("");
    const [email, setEmail] = useState<string>("");
    const [emailRepeat, setEmailRepeat] = useState<string>("");
    const [modalClass, setModalClass] = useState<string>('modal');
    const [selectedClass, setSelectedClass] = useState<MudClass | null>(null);
    const [selectedRace, setSelectedRace] = useState<MudRace | null>(null);

    let raceCollection = useMemo(() => {
        return createListCollection({
            items: races ?? [],
            itemToString: (race) => race.name,
            itemToValue: (race) => race.name,
        });
    }, [races]);

    let classCollection = useMemo(() => {
        return createListCollection({
            items: classes ?? [],
            itemToString: (player_class) => player_class.name,
            itemToValue: (player_class) => player_class.name,
        });
    }, [races]);

    useEffect(() => {
        const fetchRaces = async () => {
            try {
                const response = await fetch(apiLocation + '/v1/mud/races');
                const data = await response.json();
                setRaces(data);
            } catch (error) {
                console.error('Error fetching races:', error);
            }
        };

        const fetchClasses = async () => {
            try {
                const response = await fetch(apiLocation + '/v1/mud/classes');
                const data = await response.json();
                setClasses(data);
            } catch (error) {
                console.error('Error fetching classes:', error);
            }
        };

        const fetchData = async () => {
            await Promise.all([fetchRaces(), fetchClasses()]);
        };

        fetchData();
    }, []);

    const submitNewPlayer = useCallback(() => {
        console.log("submitNewPlayer: Entered");
    }, []);

    const handleUsernameSubmit = useCallback(() => {
        console.log("handleUsernameSubmit: Entered");
        if (username.trim() !== '') {
            if (socket && socket.readyState === WebSocket.OPEN) {
                (async () => {
                    try {
                        const hash = await argon2.hash({ pass: pin.trim(), salt: uuidv4(), time: 2, mem: 19456, hashLen: 32 });
                        console.log("hash = " + hash);
                        const response = {
                            type: MudEvents.USERNAME_ANSWER,
                            username: username.trim(),
                            pin: hash
                        };
                        socket.send(JSON.stringify(response));
                    } catch (e) {
                        console.error("Error while hashing: " + e);
                    }
                })();

                setShowUsernameModal(false); // Close the modal
                setCurrentRoomTitle(username.trim());
            } else {
                console.log("Websocket not connected");
            }
        }
        console.log("handleUsernameSubmit: Exited");
    }, [socket, username, pin, setShowUsernameModal, setCurrentRoomTitle]);

    const newUser = useCallback(() => {
        console.log("newUser: Entered");
        setActiveStep(1);
        setModalClass('modal');
        setTimeout(() => {
            setShowNewUserModal(true);
            setModalClass('modal active');
        }, 50);
    }, []);

    const handleNewUserSubmit = useCallback(() => {
        console.log("handleNewUserSubmit: Entered");

        // validate username
        if (username.trim() === '') {
            alert("Username cannot be empty");
            return;
        }
        if (username.length < 3 || username.length > 25) {
            alert("Username must be between 3 and 25 characters");
            return;
        }
        if (!/^[a-zA-Z0-9 ]+$/.test(username)) {
            alert("Username can only contain letters, numbers, and spaces");
            return;
        }
        if (username.includes(" ")) {
            alert("Username cannot contain spaces");
            return;
        }

        // validate pin
        if (pin !== repeatPin) {
            alert("Pins do not match");
            return;
        }
        if (pin.length < 4 || pin.length > 25) {
            alert("Pin must be between 4 and 25 characters" + pin.length);
            return;
        }
        if (!/^[a-zA-Z0-9 ]+$/.test(pin)) {
            alert("Pin can only contain letters, numbers, and spaces");
            return;
        }

        // validate email
        if (email !== emailRepeat) {
            alert("Emails do not match");
            return;
        }

        // verify it has a @ and . in the email
        if (!email.includes("@") || !email.includes(".")) {
            alert("Email must be a valid email address");
            return;
        }

        //validate race
        if (player_race === "") {
            alert("Please select a playable race");
            return;
        }

        //validate class
        if (player_class === "") {
            alert("Please select a playable class");
            return;
        }

        // validate firstname
        if (firstname.trim() === '') {
            alert("First name cannot be empty");
            return;
        }

        if (firstname.length < 3 || firstname.length > 25) {
            alert("First name must be between 3 and 25 characters");
            return;
        }

        // if all good, we can send the new user data to the server

        console.log("handleNewUserSubmit: Exited");
    }, [socket, username, pin, repeatPin]);


    useEffect(() => {
        if (showUsernameModal || showNewUserModal) {
            setModalClass('modal active');
        } else {
            setModalClass('modal');
        }
    }, [showUsernameModal, showNewUserModal]);

    return (
        <>
            <Stepper activeStep={activeStep}>
                <Step label="Username" />
                <Step label="Personal Information" />
                <Step label="Race" />
                <Step label="Class" />
                <Step label="Attributes" />
            </Stepper>

            {/* Login Modal */}
            {showUsernameModal && !showNewUserModal && (
                <div className={modalClass}>
                    <div className="modal-content">
                        <div className="form-grid">
                            <div>
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
                            </div>
                            <div>
                                <h2>Enter Pin</h2>
                                <input
                                    type="password"
                                    value={pin}
                                    onChange={(e) => setPin(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            handleUsernameSubmit();
                                        }
                                    }}
                                />
                            </div>
                        </div>
                        <div className="button-grid">
                            <div><button onClick={() => { newUser(); }} className="mud-button">New</button></div>
                            <div><button onClick={() => { handleUsernameSubmit(); }} className="mud-button">To Adventure!</button></div>
                        </div>
                    </div>
                </div>
            )}

            {/* New User Modal - Step 1 */}
            {showNewUserModal && activeStep === 1 && (
                <div className={modalClass}>

                    <div className="modal-content">
                        <div>
                            <h1>Welcome!</h1><br />
                            <h3>Fill out the form below to create a user to enter the world of NehsaMUD!</h3>
                        </div>
                        <div className="form-grid">
                            <div>
                                <h2>Enter Username</h2>
                                <input className="username-input"
                                    type="text"
                                    value={username}
                                    onChange={(e) => setUsername(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            handleNewUserSubmit();
                                        }
                                    }}
                                />

                                <div className='username-requirements'>
                                    <List.Root gap="2" variant="plain" align="start">
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Username must be between 3 and 25 characters
                                        </List.Item>
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Username must contain only letters, numbers, and spaces
                                        </List.Item>
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Must not be in use.
                                        </List.Item>
                                    </List.Root>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <h2>Enter New Pin</h2>
                                    <input
                                        type="password"
                                        className="pin-input"
                                        value={pin}
                                        onChange={(e) => setPin(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleNewUserSubmit();
                                            }
                                        }}
                                    />
                                </div>
                                <div>
                                    <input
                                        type="password"
                                        placeholder="Repeat Pin"
                                        className="pin-input"
                                        value={repeatPin}
                                        onChange={(e) => setRepeatPin(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleNewUserSubmit();
                                            }
                                        }}
                                    />
                                </div>
                                <div className='pin-requirements'>
                                    <List.Root gap="2" variant="plain" align="start">
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Pin must be between 4 and 25 characters
                                        </List.Item>
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Pin must contain only letters, numbers, and spaces
                                        </List.Item>
                                    </List.Root>
                                </div>
                            </div>
                        </div>
                        <div>
                            <h3>Login information for NehsaMUD is stored locally on your device. If this information is lost, your pin will be required to login again.</h3><br />
                            <h3>By creating a user, you agree to the terms and conditions of NehsaMUD.</h3><br />
                            <h3>We will never share your information with anyone.</h3>
                        </div>
                        <div className="button-grid">
                            <div><button onClick={() => setShowNewUserModal(false)} className="mud-button">Cancel</button></div>
                            <div>
                                <button onClick={() => { setActiveStep(2); }} className="mud-button">
                                    <SwordNext />
                                </button>
                            </div>
                        </div>
                    </div>
                </div >
            )}

            {/* New User - Step 2 */}
            {showNewUserModal && activeStep === 2 && (
                <div className={modalClass}>
                    <div className="modal-content">
                        <h2>Step 2: Personal Information</h2>
                        <div className="form-grid">
                            <div>
                                <h2>Enter First Name</h2>
                                <input className="firstname-input"
                                    type="text"
                                    value={firstname}
                                    onChange={(e) => setFirstName(e.target.value)}
                                    onKeyDown={(e) => {
                                        if (e.key === 'Enter') {
                                            handleNewUserSubmit();
                                        }
                                    }}
                                /><br />

                                <div className='firstname-requirements'>
                                    <List.Root gap="2" variant="plain" align="start">
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            This is not visible to other players.
                                        </List.Item>
                                    </List.Root>
                                </div>
                            </div>
                            <div>
                                <div>
                                    <h2>Enter Email</h2>
                                    <input
                                        type="text"
                                        className="email-input"
                                        value={email}
                                        onChange={(e) => setEmail(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleNewUserSubmit();
                                            }
                                        }}
                                    />
                                </div>
                                <div>
                                    <h2>Repeat Email</h2>
                                    <input
                                        type="text"
                                        className="email-input"
                                        value={emailRepeat}
                                        onChange={(e) => setEmailRepeat(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleNewUserSubmit();
                                            }
                                        }}
                                    />
                                </div>
                                <div className='email-requirements'>
                                    <List.Root gap="2" variant="plain" align="start">
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Email is used for pin recovery.
                                        </List.Item>
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            This is not visible to other players.
                                        </List.Item>
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            Must be a valid email address.
                                        </List.Item>
                                    </List.Root>
                                </div>
                            </div>
                        </div>
                        <div className="button-grid">
                            <div><button onClick={() => { setActiveStep(1); }} className="mud-button">Back</button></div>
                            <div>
                                <button onClick={() => { setActiveStep(3); }} className="mud-button">
                                    <SwordNext />
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* New User - Step 3 */}
            {showNewUserModal && activeStep === 3 && (
                <div className={modalClass}>
                    <div className="modal-content">
                        <h2>Step 3: Player Race</h2>
                        <div className="form-grid">
                            <div>
                                <Select.Root collection={raceCollection} onValueChange={(value) => {
                                    const selected = raceCollection.items.find((race) => race.name === value.value[0]);
                                    setSelectedRace(selected);
                                }}>
                                    <Select.HiddenSelect />
                                    <Select.Control>
                                        <Select.Trigger>
                                            <Select.ValueText placeholder="Select Race" />
                                        </Select.Trigger>
                                        <Select.IndicatorGroup>
                                            <Select.Indicator />
                                        </Select.IndicatorGroup>
                                    </Select.Control>
                                    <Portal>
                                        <Select.Positioner>
                                            <Select.Content>
                                                {raceCollection.items.map((mudRace) => (
                                                    <Select.Item item={mudRace} key={mudRace.id}>
                                                        {mudRace.name}
                                                        <Select.ItemIndicator />
                                                    </Select.Item>
                                                ))}
                                            </Select.Content>
                                        </Select.Positioner>
                                    </Portal>
                                </Select.Root>

                                <div className='race-requirements'>
                                    <List.Root gap="2" variant="plain" align="start">
                                        <List.Item>
                                            <List.Indicator asChild color="salmon.500">
                                                <LuTriangleAlert />
                                            </List.Indicator>
                                            You race determines your starting attributes and abilities.
                                        </List.Item>
                                    </List.Root>
                                </div>
                            </div>

                            <div className="race-info">
                                <DataList.Root gap="2" variant="subtle" key={selectedRace?.id}>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Name</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.name}</DataList.ItemValue>
                                    </DataList.Item>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Description</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.description}</DataList.ItemValue>
                                    </DataList.Item>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Abilities</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.abilities}</DataList.ItemValue>
                                    </DataList.Item>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Playable</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.playable ? "Yes":"No"}</DataList.ItemValue>
                                    </DataList.Item>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Experience Adjustment</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.baseExperienceAdjustment}</DataList.ItemValue>
                                    </DataList.Item>
                                    <DataList.Item>
                                        <DataList.ItemLabel>Traits</DataList.ItemLabel>
                                        <DataList.ItemValue>{selectedRace?.directives}</DataList.ItemValue>
                                    </DataList.Item>
                                </DataList.Root>
                                <div>

                                </div>
                            </div>
                        </div>
                        <div className="button-grid">
                            <div><button onClick={() => { setActiveStep(2); }} className="mud-button">Back</button></div>
                            <div>
                                <button onClick={() => { setActiveStep(4); }} className="mud-button">
                                    <SwordNext />
                                </button>
                            </div>
                        </div>
                    </div>
                </div >
            )}

            {/* New User - Step 4 */}
            {
                showNewUserModal && activeStep === 4 && (
                    <div className={modalClass}>
                        <div className="modal-content">
                            <h2>Step 4: Player Class</h2>
                            <div className="form-grid">
                                <div>
                                    <h2>Select class from drop-down:</h2>
                                    <br />
                                    <Select.Root collection={classCollection} onValueChange={(value) => {
                                        const selected = classCollection.items.find((cls) => cls.name === value.value[0]);
                                        setSelectedClass(selected);
                                    }}>
                                        <Select.HiddenSelect />
                                        <Select.Control>
                                            <Select.Trigger>
                                                <Select.ValueText placeholder="Select Class" />
                                            </Select.Trigger>
                                            <Select.IndicatorGroup>
                                                <Select.Indicator />
                                            </Select.IndicatorGroup>
                                        </Select.Control>
                                        <Portal>
                                            <Select.Positioner>
                                                <Select.Content>
                                                    {classCollection.items.map((mudClass) => (
                                                        <Select.Item item={mudClass} key={mudClass.id}>
                                                            {mudClass.name}
                                                            <Select.ItemIndicator />
                                                        </Select.Item>
                                                    ))}
                                                </Select.Content>
                                            </Select.Positioner>
                                        </Portal>
                                    </Select.Root><br />

                                    <div className='class-requirements'>
                                        <List.Root gap="2" variant="plain" align="start">
                                            <List.Item>
                                                <List.Indicator asChild color="salmon.500">
                                                    <LuTriangleAlert />
                                                </List.Indicator>
                                                You class determines the primary function of your character.
                                            </List.Item>
                                        </List.Root>
                                    </div>
                                </div>
                                <div className="class-info-grid">
                                    <div><p>{selectedClass?.description || "Select a class to see its description."}</p></div>
                                    <div><p>{selectedClass?.description || ""}</p></div>
                                    <div><p>{selectedClass?.description || ""}</p></div>
                                </div>
                            </div>
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(3); }} className="mud-button">Back</button></div>
                                <div>
                                    <button onClick={() => { setActiveStep(5); }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }

            {/* New User - Step 5 */}
            {
                showNewUserModal && activeStep === 5 && (
                    <div className={modalClass}>
                        <div className="modal-content">
                            <h2>Step 5: Finalize Attributes</h2>
                            <div className="form-grid">
                                <div>
                                </div>
                            </div>
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(4); }} className="mud-button">Back</button></div>
                                <div>
                                    <button onClick={() => { handleNewUserSubmit(); }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }

            {/* Background Overlay */}
            {(showUsernameModal || showNewUserModal) && <div className="modal-overlay"></div>}
        </>
    );
};

export default LoginModal;