import { useState, useEffect } from 'react'
import './App.css'

interface User {
  email: string;
}

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [showAuthForm, setShowAuthForm] = useState(false)
  const [authMode, setAuthMode] = useState<'login' | 'signup'>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')

  useEffect(() => {
    // Check if user is already logged in (e.g., by checking localStorage or cookies)
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const endpoint = authMode === 'login' ? '/auth/login' : '/auth/signup'
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })
      if (response.ok) {
        const data = await response.json()
        if (authMode === 'login') {
          setUser({ email })
          localStorage.setItem('user', JSON.stringify({ email }))
          // You might want to store the tokens securely here
        } else {
          alert('Signup successful. Please check your email for verification.')
        }
        setShowAuthForm(false)
      } else {
        throw new Error('Authentication failed')
      }
    } catch (error) {
      alert('Authentication failed. Please try again.')
    }
  }

  const handleLogout = () => {
    setUser(null)
    localStorage.removeItem('user')
    // You should also invalidate the tokens on the server-side
  }

  return (
    <div className="app-container">
      <div className="toolbar">
        {user ? (
          <>
            <span>Welcome, {user.email}</span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <button onClick={() => setShowAuthForm(true)}>Login</button>
        )}
      </div>

      <div className="main-content">
        {showAuthForm && !user && (
          <div className="auth-form">
            <h2>{authMode === 'login' ? 'Login' : 'Sign Up'}</h2>
            <form onSubmit={handleAuth}>
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
          </div>
        )}

        {user && (
          <div className="search-box">
            <input type="text" placeholder="Search..." />
            <button>Search</button>
          </div>
        )}
      </div>
    </div>
  )
}

export default App
