import React, { useState } from 'react';

interface AuthFormProps {
    onAuth: (email: string, password: string, mode: 'login' | 'signup') => Promise<void>;
    onClose: () => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ onAuth, onClose }) => {
    const [authMode, setAuthMode] = useState<'login' | 'signup'>('login');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        onAuth(email, password, authMode);
    };

    return (
        <div className="auth-form">
            <h2>{authMode === 'login' ? 'Login' : 'Sign Up'}</h2>
            <form onSubmit={handleSubmit}>
                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
                <button type="submit">{authMode === 'login' ? 'Login' : 'Sign Up'}</button>
            </form>
            <button onClick={() => setAuthMode(authMode === 'login' ? 'signup' : 'login')}>
                {authMode === 'login' ? 'Need an account? Sign Up' : 'Already have an account? Login'}
            </button>
            <button onClick={onClose}>Close</button>
        </div>
    );
};

export default AuthForm;