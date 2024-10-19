import { useState, useEffect } from 'react'
import './App.css'
import Toolbar from './components/Toolbar'
import AuthForm from './components/AuthForm'
import SearchBox from './components/SearchBox'
import SearchResults from './components/SearchResults'
import { User, SearchResponse } from './types'
import apiClient from './utils/apiClient'

function App() {
  const [user, setUser] = useState<User | null>(null)
  const [showAuthForm, setShowAuthForm] = useState(false)
  const [searchResults, setSearchResults] = useState<SearchResponse | null>(null)

  useEffect(() => {
    const storedEmail = localStorage.getItem('userEmail');
    const storedToken = sessionStorage.getItem('accessToken');
    if (storedEmail && storedToken) {
      setUser({ email: storedEmail });
    }
  }, [])

  const handleAuth = async (email: string, password: string, mode: 'login' | 'signup') => {
    try {
      const endpoint = mode === 'login' ? '/auth/login' : '/auth/signup';
      const response = await apiClient.post(endpoint, { email, password });
      const data = response.data;
      if (mode === 'login') {
        setUser({ email });
        localStorage.setItem('userEmail', email);
        // Assuming the server sends back an access token
        if (data.access_token) {
          sessionStorage.setItem('accessToken', data.access_token);
        }
      } else {
        alert('Signup successful. Please check your email for verification.');
      }
      setShowAuthForm(false);
    } catch (error) {
      console.error('Authentication failed:', error);
      alert('Authentication failed. Please try again.');
    }
  }

  const handleLogout = async () => {
    try {
      await apiClient.post('/auth/logout');
      setUser(null);
      sessionStorage.removeItem('accessToken');
      localStorage.removeItem('userEmail');
    } catch (error) {
      console.error('Logout failed:', error);
      alert('Logout failed. Please try again.');
    }
  }

  const handleSearch = async (keyword: string) => {
    try {
      const response = await apiClient.get(`/api/reddit/search?keyword=${encodeURIComponent(keyword)}`);
      setSearchResults(response.data);
    } catch (error) {
      console.error('Search failed:', error);
      alert('An error occurred while searching. Please try again.');
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
