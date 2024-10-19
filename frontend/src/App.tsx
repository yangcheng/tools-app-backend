import { useState, useEffect } from 'react'
import './App.css'
import Toolbar from './components/Toolbar'
import AuthForm from './components/AuthForm'
import SearchBox from './components/SearchBox'
import SearchResults from './components/SearchResults'
import { User, SearchResponse } from './types'

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [showAuthForm, setShowAuthForm] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null)

  useEffect(() => {
    const storedUser = localStorage.getItem('user')
    if (storedUser) {
      setUser(JSON.parse(storedUser))
    }
  }, [])

  const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/signup'
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      })
      if (response.ok) {
        const data = await response.json()
        if (mode === 'login') {
          setUser({ email })
          localStorage.setItem('user', JSON.stringify({ email }))
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
  }

  const handleSearch = async (keyword: string) => {
    try {
      const response = await fetch(`http://localhost:8000/api/reddit/search?keyword=${encodeURIComponent(keyword)}`)
      if (!response.ok) {
        throw new Error('Search failed')
      }
      const data: SearchResponse = await response.json()
      setSearchResults(data)
    } catch (error) {
      alert('An error occurred while searching. Please try again.')
    }
  }

  return (
    <div className="app-container">
      <Toolbar
        user={user}
        onLogout={handleLogout}
        onShowAuthForm={() => setShowAuthForm(true)}
      />

      <div className="main-content">
        {showAuthForm && !user && (
          <AuthForm onAuth={handleAuth} onClose={() => setShowAuthForm(false)} />
        )}

        {user && <SearchBox onSearch={handleSearch} />}

        {searchResults && (
          <SearchResults searchResults={searchResults} />
        )}
      </div>
    </div>
  )
}

export default App
