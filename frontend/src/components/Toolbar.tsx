import React from 'react';

interface User {
    email: string;
}

interface ToolbarProps {
    user: User | null;
    onLogout: () => void;
    onShowAuthForm: () => void;
}

const Toolbar: React.FC<ToolbarProps> = ({ user, onLogout, onShowAuthForm }) => {
    return (
        <div className="toolbar">
            {user ? (
                <>
                    <span>Welcome, {user.email}</span>
                    <button onClick={onLogout}>Logout</button>
                </>
            ) : (
                <button onClick={onShowAuthForm}>Login</button>
            )}
        </div>
    );
};

export default Toolbar;