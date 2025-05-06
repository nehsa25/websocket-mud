import React from 'react';

interface SplashProps {
    isConnecting: boolean;
}

const Splash: React.FC<SplashProps> = ({ isConnecting }) => {
    const splashStyle: React.CSSProperties = {
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100%',
        height: '100%',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        fontSize: '2em',
        color: 'white',
        zIndex: 1000,
    };

    return (
        isConnecting && (
            <div style={splashStyle}>
                Connecting to WebSocket Server...
            </div>
        )
    );
};

export default Splash;