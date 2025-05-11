import './Login.scss';
import React, { useState, useCallback, useEffect, useMemo } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { createListCollection, DataList, List, Text, Portal } from "@chakra-ui/react";
import { Select } from "@chakra-ui/react";
import * as argon2 from 'argon2-wasm';
import { MudEvents } from '../Types/MudEvents';
import { Step, Stepper } from "react-form-stepper";
import SwordNext from '../React/SwordNext/SwordNext';
import { LuTriangleAlert } from 'react-icons/lu';
import Bard from '../React/Classes/bard/Bard';
import Barbarian from '../React/Classes/barbarian/Barbarian';
import Cleric from '../React/Classes/cleric/Cleric';
import Druid from '../React/Classes/druid/Druid';
import Wizard from '../React/Classes/mage/Mage';
import Mage from '../React/Classes/mage/Mage';
import Thief from '../React/Classes/thief/Thief';
import Warrior from '../React/Classes/warrior/Warrior';
import Warlock from '../React/Classes/warlock/Warlock';
import Human from '../React/Races/human/Human';

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
    strength: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
    constitution: number;
    dexterity: number;
    luck: number;
}

interface MudClass {
    id: string;
    name: string;
    description: string;
    abilities: string[];
    playable: boolean;
    directives: string[];
    baseExperienceAdjustment: number;
    strength: number;
    intelligence: number;
    wisdom: number;
    charisma: number;
    constitution: number;
    dexterity: number;
    luck: number;
}

interface BodyType {
    id: string;
    name: string;
    description: string;
}

interface EyeColorType {
    id: string;
    name: string;
}

interface EyeBrowType {
    id: string;
    name: string;
}

interface HairColorType {
    id: string;
    name: string;
}

interface HairStyleType {
    id: string;
    name: string;
}

interface FacialHairStyleType {
    id: string;
    name: string;
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
    const [strength, setStrength] = useState<number>(0);
    const [intelligence, setIntelligence] = useState<number>(0);
    const [wisdom, setWisdom] = useState<number>(0);
    const [charisma, setCharisma] = useState<number>(0);
    const [constitution, setConstitution] = useState<number>(0);
    const [dexterity, setDexterity] = useState<number>(0);
    const [luck, setLuck] = useState<number>(0);
    const [attributesRemaining, setAttributesRemaining] = useState<number>(5);

    // body types
    const [selectedBodyType, setSelectedBodyType] = useState<BodyType>();
    let bodyTypeCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'thin', name: 'Thin', description: "+1 dex, -1 strength" },
                { id: 'average', name: 'Average', description: "No modifiers" },
                { id: 'large', name: 'Large', description: "+1 strength, -1 dex" },
                { id: 'enormous', name: 'Enormous', description: "+1 strength, +1 const" },
            ],
            itemToString: (selectedBodyType) => selectedBodyType.name,
            itemToValue: (selectedBodyType) => selectedBodyType.name,
        });
    }, [selectedBodyType]);

    // eye color types
    const [selectedEyeColor, setSelectedEyeColor] = useState<EyeColorType>();
    let eyeColorCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'brown', name: 'Brown' },
                { id: 'blue', name: 'Blue' },
                { id: 'green', name: 'Green' },
                { id: 'gray', name: 'Gray' },
                { id: 'black', name: 'Black' },
                { id: 'red', name: 'Red' },
                { id: 'yellow', name: 'Yellow' },
                { id: 'purple', name: 'Purple' },
                { id: 'pink', name: 'Pink' },
                { id: 'orange', name: 'Orange' },
                { id: 'white', name: 'White' },
                { id: 'gold', name: 'Gold' },
                { id: 'silver', name: 'Silver' },
                { id: 'amber', name: 'Amber' },
                { id: 'hazel', name: 'Hazel' },
                { id: 'violet', name: 'Violet' }
            ],
            itemToString: (eyeColor) => eyeColor.name,
            itemToValue: (eyeColor) => eyeColor.name,
        });
    }, [selectedEyeColor]);

    // eye brow types
    const [selectedEyeBrow, setSelectedEyeBrow] = useState<EyeBrowType>();
    let eyeBrowCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'thin', name: 'thin' },
                { id: 'bushy', name: 'bushy' },
                { id: 'obtuse', name: 'obtuse' },
            ],
            itemToString: (eyebrow) => eyebrow.name,
            itemToValue: (eyebrow) => eyebrow.name,
        });
    }, [selectedEyeBrow]);

    // hair color types
    const [selectedHairColor, setSelectedHairColor] = useState<HairColorType>();
    let hairColorCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'brown', name: 'Brown' },
                { id: 'blue', name: 'Blue' },
                { id: 'green', name: 'Green' },
                { id: 'gray', name: 'Gray' },
                { id: 'black', name: 'Black' },
                { id: 'red', name: 'Red' },
                { id: 'yellow', name: 'Yellow' },
                { id: 'purple', name: 'Purple' },
                { id: 'pink', name: 'Pink' },
                { id: 'orange', name: 'Orange' },
                { id: 'white', name: 'White' },
                { id: 'gold', name: 'Gold' },
                { id: 'silver', name: 'Silver' },
                { id: 'amber', name: 'Amber' },
                { id: 'hazel', name: 'Hazel' },
                { id: 'violet', name: 'Violet' }
            ],
            itemToString: (selectedHairColor) => selectedHairColor.name,
            itemToValue: (selectedHairColor) => selectedHairColor.name,
        });
    }, [selectedHairColor]);

    // hair style types
    const [selectedHairStyle, setSelectedHairStyle] = useState<HairStyleType>();
    let hairStyleCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'bald', name: 'Bald' },
                { id: 'short', name: 'Short Hair' },
                { id: 'longhair', name: 'Long Hair' },
                { id: 'mohawk', name: 'Mohawk' },
            ],
            itemToString: (selectedHairStyle) => selectedHairStyle.name,
            itemToValue: (selectedHairStyle) => selectedHairStyle.name,
        });
    }, [selectedHairStyle]);

    // facial hair style types
    const [selectedFacialHairStyle, setSelectedFacialHairStyle] = useState<FacialHairStyleType>();
    let facialHairStyleCollection = useMemo(() => {
        return createListCollection({
            items: [
                { id: 'none', name: 'None' },
                { id: 'mustache', name: 'Mustache' },
                { id: 'beard', name: 'Beard' },
                { id: 'goatee', name: 'Goatee' },
                { id: 'sideburns', name: 'Sideburns' },
            ],
            itemToString: (selectedHairStyle) => selectedHairStyle.name,
            itemToValue: (selectedHairStyle) => selectedHairStyle.name,
        });
    }, [selectedFacialHairStyle]);


    let raceCollection = useMemo(() => {
        return createListCollection({
            items: races?.filter(c => c.playable) ?? [],
            itemToString: (race) => race.name,
            itemToValue: (race) => race.name,
        });
    }, [races]);

    let classCollection = useMemo(() => {
        return createListCollection({
            items: classes?.filter(c => c.playable) ?? [],
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
                setSelectedRace(data[0]);
            } catch (error) {
                console.error('Error fetching races:', error);
            }
        };

        const fetchClasses = async () => {
            try {
                const response = await fetch(apiLocation + '/v1/mud/classes');
                const data = await response.json();
                setClasses(data);
                setSelectedClass(data[0]);
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

    const baseAttributes = useMemo(() => ({
        strength: 0,
        intelligence: 0,
        wisdom: 0,
        charisma: 0,
        constitution: 0,
        dexterity: 0,
        luck: 0,
    }), []);

    const updateAttributes = useCallback((race: MudRace | null, playerClass: MudClass | null) => {
        let newStrength = baseAttributes.strength;
        let newIntelligence = baseAttributes.intelligence;
        let newWisdom = baseAttributes.wisdom;
        let newCharisma = baseAttributes.charisma;
        let newConstitution = baseAttributes.constitution;
        let newDexterity = baseAttributes.dexterity;
        let newLuck = baseAttributes.luck;

        if (race) {
            newStrength += race.strength ?? 0;
            newIntelligence += race.intelligence ?? 0;
            newWisdom += race.wisdom ?? 0;
            newCharisma += race.charisma ?? 0;
            newConstitution += race.constitution ?? 0;
            newDexterity += race.dexterity ?? 0;
            newLuck += race.luck ?? 0;
        }

        if (playerClass) {
            newStrength += playerClass.strength ?? 0;
            newIntelligence += playerClass.intelligence ?? 0;
            newWisdom += playerClass.wisdom ?? 0;
            newCharisma += playerClass.charisma ?? 0;
            newConstitution += playerClass.constitution ?? 0;
            newDexterity += playerClass.dexterity ?? 0;
            newLuck += playerClass.luck ?? 0;
        }

        setStrength(newStrength);
        setIntelligence(newIntelligence);
        setWisdom(newWisdom);
        setCharisma(newCharisma);
        setConstitution(newConstitution);
        setDexterity(newDexterity);
        setLuck(newLuck);
    }, [baseAttributes, setStrength, setIntelligence, setWisdom, setCharisma, setConstitution, setDexterity, setLuck]);


    useEffect(() => {
        updateAttributes(selectedRace, selectedClass);
    }, [selectedRace, selectedClass, updateAttributes]);

    useEffect(() => {
        if (showUsernameModal || showNewUserModal) {
            setModalClass('modal active');
        } else {
            setModalClass('modal');
        }
    }, [showUsernameModal, showNewUserModal]);

    useEffect(() => {
        console.log("Attributes Remaining changed:", attributesRemaining);
    }, [attributesRemaining]);

    const decreaseStrength = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setStrength((prev) => Math.max(prev - 1, 0));
    }
        , []);

    const increaseStrength = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setStrength((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setStrength, attributesRemaining]);

    const decreaseIntelligence = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setIntelligence((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseIntelligence = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setIntelligence((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setIntelligence, attributesRemaining]);

    const decreaseWisdom = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setWisdom((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseWisdom = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setWisdom((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setWisdom, attributesRemaining]);

    const decreaseCharisma = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setCharisma((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseCharisma = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setCharisma((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setCharisma, attributesRemaining]);

    const decreaseConstitution = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setConstitution((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseConstitution = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setConstitution((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setConstitution, attributesRemaining]);

    const decreaseDexterity = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setDexterity((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseDexterity = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setDexterity((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setDexterity, attributesRemaining]);

    const decreaseLuck = useCallback(() => {
        setAttributesRemaining((prev) => prev + 1);
        setLuck((prev) => Math.max(prev - 1, 0));
    }, []);

    const increaseLuck = useCallback(() => {
        if (attributesRemaining > 0) {
            setAttributesRemaining((prev) => prev - 1);
            setLuck((prev) => Math.min(prev + 1, 100));
        } else {
            alert("You have no more points to spend!");
        }
    }, [setAttributesRemaining, setLuck, attributesRemaining]);

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
            {
                showUsernameModal && !showNewUserModal && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
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
            {
                showNewUserModal && activeStep === 1 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 1 of 7: Username and Pin</h2><br />
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
            {
                showNewUserModal && activeStep === 2 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 2 of 7: Personal Information</h2><br />
                            </div>
                            <Text>The information on this page is not used in the game.<br />Your email address is optional but beware it is required to perform pin resets for account recovery.</Text>
                            <div className="form-grid">
                                <div className="form-grid-rows-condensed">
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
                                        />
                                    </div>
                                    <div>
                                        <h2>Enter Email (Optional)</h2>
                                        <input
                                            type="text"
                                            className="email-input"
                                            value={email}
                                            onChange={(e) => setEmail(e.target.value)}
                                        /><br /><br />
                                        <h2>Repeat Email</h2>
                                        <input
                                            type="text"
                                            className="email-input"
                                            value={emailRepeat}
                                            onChange={(e) => setEmailRepeat(e.target.value)}
                                        />
                                    </div>
                                </div>
                                <div>
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
                                    <button onClick={() => {
                                        if (!firstname) {
                                            alert("Please provide a first name. Email address is optional (but is only used if you need a pin reset)."); return;
                                        } setActiveStep(3);
                                    }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

            {/* New User - Step 3 - Race */}
            {
                showNewUserModal && activeStep === 3 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 3 of 7:  Player Race</h2><br />
                            </div>
                            <div className="form-grid">
                                <div>
                                    <Select.Root
                                        collection={raceCollection}
                                        value={[selectedRace?.name]}
                                        onValueChange={(value) => {
                                            const selected = raceCollection.items.find((race) => race.name === value.value[0]);
                                            setSelectedRace(selected);
                                        }}
                                    >
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
                                            <DataList.ItemValue>{selectedRace?.playable ? "Yes" : "No"}</DataList.ItemValue>
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
                                </div>
                            </div>
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
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(2); }} className="mud-button">Back</button></div>
                                <div>
                                    <button onClick={() => { setActiveStep(4); }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

            {/* New User - Step 4 */}
            {
                showNewUserModal && activeStep === 4 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 4 of 7: Player Class</h2><br />
                            </div>
                            <div className="form-grid">
                                <div>
                                    <Select.Root
                                        collection={classCollection}
                                        value={[selectedClass?.name]}
                                        onValueChange={(value) => {
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
                                    </Select.Root>
                                </div>
                                <div className="class-info">
                                    <div>{selectedClass?.name}
                                        {selectedClass?.name === "barbarian" && (<Barbarian />)}
                                        {selectedClass?.name === "bard" && (<Bard />)}
                                        {selectedClass?.name === "wizard" && (<Wizard />)}
                                        {selectedClass?.name === "cleric" && (<Cleric />)}
                                        {selectedClass?.name === "druid" && (<Druid />)}
                                        {selectedClass?.name === "mage" && (<Mage />)}
                                        {selectedClass?.name === "thief" && (<Thief />)}
                                        {selectedClass?.name === "warrior" && (<Warrior />)}
                                        {selectedClass?.name === "warlock" && (<Warlock />)}
                                    </div>
                                    <DataList.Root gap="2" variant="subtle" key={selectedClass?.id}>
                                        <DataList.Item>
                                            <DataList.ItemLabel>Description</DataList.ItemLabel>
                                            <DataList.ItemValue>{selectedClass?.description}</DataList.ItemValue>
                                        </DataList.Item>
                                        <DataList.Item>
                                            <DataList.ItemLabel>Abilities</DataList.ItemLabel>
                                            <DataList.ItemValue>{selectedClass?.abilities}</DataList.ItemValue>
                                        </DataList.Item>
                                        <DataList.Item>
                                            <DataList.ItemLabel>Playable</DataList.ItemLabel>
                                            <DataList.ItemValue>{selectedClass?.playable ? "Yes" : "No"}</DataList.ItemValue>
                                        </DataList.Item>
                                        <DataList.Item>
                                            <DataList.ItemLabel>Experience Adjustment</DataList.ItemLabel>
                                            <DataList.ItemValue>{selectedClass?.baseExperienceAdjustment}</DataList.ItemValue>
                                        </DataList.Item>
                                        <DataList.Item>
                                            <DataList.ItemLabel>Traits</DataList.ItemLabel>
                                            <DataList.ItemValue>{selectedClass?.directives}</DataList.ItemValue>
                                        </DataList.Item>
                                    </DataList.Root>
                                </div>
                            </div>
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
                )}

            {/* New User - Step 5 Description */}
            {
                showNewUserModal && activeStep === 5 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 5 of 7: Character Description</h2>
                            </div>
                            <div className="form-grid">
                                <div className="form-grid-rows-condensed">
                                    <div>
                                        <Select.Root size="xs" collection={bodyTypeCollection} onValueChange={(value) => {
                                            const selected = bodyTypeCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedBodyType(selected);
                                        }}
                                        >
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Body Type" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {bodyTypeCollection.items.map((bodyType) => (
                                                            <Select.Item item={bodyType} key={bodyType.id}>
                                                                {bodyType.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                    <div>
                                        <Select.Root size="xs" collection={eyeColorCollection} onValueChange={(value) => {
                                            const selected = eyeColorCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedEyeColor(selected);
                                        }}>
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Eye Color" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {eyeColorCollection.items.map((eyeColor) => (
                                                            <Select.Item item={eyeColor} key={eyeColor.id}>
                                                                {eyeColor.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                    <div>
                                        <Select.Root size="xs" collection={eyeBrowCollection} onValueChange={(value) => {
                                            const selected = eyeBrowCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedEyeBrow(selected);
                                        }}>
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Eye Brow" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {eyeBrowCollection.items.map((eyebrow) => (
                                                            <Select.Item item={eyebrow} key={eyebrow.id}>
                                                                {eyebrow.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                    <div>
                                        <Select.Root size="xs" collection={facialHairStyleCollection} onValueChange={(value) => {
                                            const selected = facialHairStyleCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedFacialHairStyle(selected);
                                        }}>
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Facial Hair" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {facialHairStyleCollection.items.map((facialHair) => (
                                                            <Select.Item item={facialHair} key={facialHair.id}>
                                                                {facialHair.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                    <div>
                                        <Select.Root size="xs" collection={hairColorCollection} onValueChange={(value) => {
                                            const selected = hairColorCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedHairColor(selected);
                                        }}>
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Hair Color" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {hairColorCollection.items.map((hairColor) => (
                                                            <Select.Item item={hairColor} key={hairColor.id}>
                                                                {hairColor.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                    <div>
                                        <Select.Root size="xs" collection={hairStyleCollection} onValueChange={(value) => {
                                            const selected = hairStyleCollection.items.find((bt) => bt.name === value.value[0]);
                                            setSelectedHairStyle(selected);
                                        }}>
                                            <Select.Control>
                                                <Select.Trigger>
                                                    <Select.ValueText placeholder="Select Hair Style" />
                                                </Select.Trigger>
                                                <Select.IndicatorGroup>
                                                    <Select.Indicator />
                                                </Select.IndicatorGroup>
                                            </Select.Control>
                                            <Portal>
                                                <Select.Positioner>
                                                    <Select.Content>
                                                        {hairStyleCollection.items.map((hairStyle) => (
                                                            <Select.Item item={hairStyle} key={hairStyle.id}>
                                                                {hairStyle.name}
                                                                <Select.ItemIndicator />
                                                            </Select.Item>
                                                        ))}
                                                    </Select.Content>
                                                </Select.Positioner>
                                            </Portal>
                                        </Select.Root>
                                    </div>
                                </div>
                                <div>
                                    {
                                        selectedRace?.name == "human" && (
                                            <Human
                                                eyecolor={selectedEyeColor?.id}
                                                haircolor={selectedHairColor?.id}
                                                hairstyle={selectedHairStyle?.id}
                                                body_type={selectedBodyType?.id}
                                                facial_hair={selectedFacialHairStyle?.id}
                                            />
                                        )}

                                </div>
                            </div>
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(4); }} className="mud-button">Back</button></div>
                                <div>
                                    <button onClick={() => { setActiveStep(6); }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div >
                )
            }

            {/* New User - Step 6 - Attributes */}
            {
                showNewUserModal && activeStep === 6 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 6 of 7: Finalize Attributes</h2><br />
                            </div>
                            <div className="form-grid">
                                <div className="form-grid-rows-condensed">
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Strength</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseStrength(); }} className="mud-button">-</button>
                                                <input
                                                    className="strength-input"
                                                    type="text"
                                                    value={strength}
                                                    onChange={(e) => setStrength(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseStrength() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Intelligence</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseIntelligence(); }} className="mud-button">-</button>
                                                <input className="intelligence-input"
                                                    type="text"
                                                    value={intelligence}
                                                    onChange={(e) => setIntelligence(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseIntelligence() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Wisdom</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseWisdom(); }} className="mud-button">-</button>
                                                <input className="wisdom-input"
                                                    type="text"
                                                    value={wisdom}
                                                    onChange={(e) => setWisdom(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseWisdom() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Dexterity</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseDexterity(); }} className="mud-button">-</button>
                                                <input className="dexterity-input"
                                                    type="text"
                                                    value={dexterity}
                                                    onChange={(e) => setDexterity(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseDexterity() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Constitution</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseConstitution(); }} className="mud-button">-</button>
                                                <input className="constitution-input"
                                                    type="text"
                                                    value={constitution}
                                                    onChange={(e) => setConstitution(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseConstitution() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Charisma</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseCharisma(); }} className="mud-button">-</button>
                                                <input className="charisma-input"
                                                    type="text"
                                                    value={charisma}
                                                    onChange={(e) => setCharisma(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseCharisma() }} className="mud-button">+</button>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="attributes-info-grid">
                                        <div>
                                            <h2>Luck</h2>
                                        </div>
                                        <div>
                                            <div className="attribute-input-group">
                                                <button onClick={() => { decreaseLuck(); }} className="mud-button">-</button>
                                                <input className="luck-input"
                                                    type="text"
                                                    value={luck}
                                                    onChange={(e) => setLuck(Number(e.target.value))}
                                                />
                                                <button onClick={() => { increaseLuck() }} className="mud-button">+</button>
                                            </div>

                                        </div>
                                    </div>
                                </div>
                                <div className="attributes-panel">
                                    <div>Attributes<br /><br />

                                        <Text>While your race and class are the primary indicators of your characters attributes, some adjustments can be made here.</Text>

                                        Attributes Remainining: {attributesRemaining}</div>
                                    <div>Help
                                        <DataList.Root className="attribute-details" gap="2" variant="bold">
                                            <DataList.Item>
                                                <DataList.ItemLabel>Strength</DataList.ItemLabel>
                                                <DataList.ItemValue>How hard can you hit things?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Intelligence</DataList.ItemLabel>
                                                <DataList.ItemValue>How smart are you?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Wisdom</DataList.ItemLabel>
                                                <DataList.ItemValue>How wise are you?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Dexterity</DataList.ItemLabel>
                                                <DataList.ItemValue>How quick are you?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Constitution</DataList.ItemLabel>
                                                <DataList.ItemValue>How tough are you?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Charisma</DataList.ItemLabel>
                                                <DataList.ItemValue>Do people give you free stuff?</DataList.ItemValue>
                                            </DataList.Item>
                                            <DataList.Item>
                                                <DataList.ItemLabel>Luck</DataList.ItemLabel>
                                                <DataList.ItemValue>How lucky are you?</DataList.ItemValue>
                                            </DataList.Item>
                                        </DataList.Root>
                                    </div>
                                </div>
                            </div>
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(5); }} className="mud-button">Back</button></div>
                                <div>
                                    <button onClick={() => { setActiveStep(7); }} className="mud-button">
                                        <SwordNext />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }

            {/* New User - Step 7 - Summary */}
            {
                showNewUserModal && activeStep === 7 && (
                    <div className={modalClass}>
                        <div className="modal-content-grid">
                            <div>
                                <h2>Step 7 of 7: Summary</h2><br />
                            </div>
                            <div>
                                <div className="form-quad-grid">
                                    <div>
                                        Player
                                        <div className="form-grid-condensed">
                                            <div>Username</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Pin</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Name</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Email</div><div>value</div>
                                        </div>
                                    </div>
                                    <div>
                                        Description
                                        <div className="form-grid-condensed">
                                            <div>Hair Style</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Hair Color</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Eye Color</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Eye Brows</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Body Type</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Sex</div><div>value</div>
                                        </div>
                                    </div>
                                    <div>
                                        Attributes
                                        <div className="form-grid-condensed">
                                            <div>Race</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Class</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Strength</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Dexerity</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Intelligence</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Wisdom</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Luck</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Charisma</div><div>value</div>
                                        </div>
                                    </div>
                                    <div>
                                        Traits
                                        <div className="form-grid-condensed">
                                            <div>Race</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Class</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Strength</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Dexerity</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Intelligence</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Wisdom</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Luck</div><div>value</div>
                                        </div>
                                        <div className="form-grid-condensed">
                                            <div>Charisma</div><div>value</div>
                                        </div>
                                    </div>
                                </div>
                                <div>
                                    <Human
                                        eyecolor={selectedEyeColor?.id}
                                        haircolor={selectedHairColor?.id}
                                        hairstyle={selectedHairStyle?.id}
                                        body_type={selectedBodyType?.id}
                                        facial_hair={selectedFacialHairStyle?.id}
                                    />
                                </div>
                            </div>
                            <div className="button-grid">
                                <div><button onClick={() => { setActiveStep(6); }} className="mud-button">Back</button></div>
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