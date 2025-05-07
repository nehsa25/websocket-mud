import './Login.scss';
import React, { useState, useCallback, useEffect } from 'react';
import { v4 as uuidv4 } from 'uuid';
import { List } from "@chakra-ui/react";
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

    const [activeStep, setActiveStep] = useState(0);
    const [repeatPin, setRepeatPin] = useState<string>("0000");
    const [modalClass, setModalClass] = useState<string>('modal');
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

        // go to step 2
        setActiveStep(1);
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
                <Step label="Login" />
                <Step label="Character" />
                <Step label="Confirm" />
            </Stepper>


            {/* Login Modal */}
            {showUsernameModal && (
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

            {/* New User Modal */}
            {showNewUserModal && (
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
                                            handleUsernameSubmit();
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
                                    <input className="pin-input"
                                        value={pin}
                                        onChange={(e) => setPin(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleUsernameSubmit();
                                            }
                                        }}
                                    />
                                </div>
                                <div>
                                    <h2>Repeat Pin</h2>
                                    <input className="pin-input"
                                        value={repeatPin}
                                        onChange={(e) => setRepeatPin(e.target.value)}
                                        onKeyDown={(e) => {
                                            if (e.key === 'Enter') {
                                                handleUsernameSubmit();
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
                                <button onClick={() => { handleNewUserSubmit(); }} className="mud-button">
                                    <SwordNext />
                                </button>
                            </div>
                        </div>
                    </div>
                </div >
            )}
        </>
    );
};

export default LoginModal;