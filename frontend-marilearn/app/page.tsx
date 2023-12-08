"use client"
// components/Login.tsx
import React, { useState } from 'react';
import Image from 'next/image';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoggingIn, setIsLoggingIn] = useState(false);
  const [isResponseOK, setIsResponseOK] = useState(false);

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoggingIn(true);

    try {
      const response = await fetch('https://marilearntstedutech.azurewebsites.net/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `username=${encodeURIComponent(username)}&password=${encodeURIComponent(password)}`,
      });
  
      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        setIsResponseOK(true);
        window.location.href = '/dashboard';
      } else {
        const errorData = await response.json();
        setError(errorData.detail);
        setIsResponseOK(false);
      }
    } catch (error) {
      console.error('Error during authentication', error);
      setError('An unexpected error occurred');
      setIsResponseOK(false);
    } finally {
      setIsLoggingIn(false);
    }
  };
  
  return (
    <div className="flex flex-col items-center mt-10 pt-10 py-40">
      <div className="mb-8">
        <Image src="/logo.png" alt="Logo" width={200} height={200} />
      </div>

      <form onSubmit={handleLogin} className="w-full max-w-md">
        <div className="mb-4 px-5">
          <label htmlFor="username" className="block text-sm font-medium text-gray-600">
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        <div className="mb-4 px-5">
          <label htmlFor="password" className="block text-sm font-medium text-gray-600">
            Password
          </label>
          <input
            type="password"
            id="password"
            name="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>

        {error && (
          <div className="text-red-500 mb-4 px-5">
            <p>{error}</p>
          </div>
        )}

        <div className='px-5'>
          <button
            type="submit"
            className={`bg-blue-500 text-white p-2 rounded-md mb-4 w-full ${isResponseOK ? 'bg-green-500' : ''}`}
            disabled={isLoggingIn} // Disable the button when logging in
          >
            {isLoggingIn ? 'Logging In...' : isResponseOK ? 'Redirecting...' : 'Login'}
          </button>
        </div>

        <div className="text-center">
          <span>Belum punya akun? </span>
          <button type="button" className="text-blue-500" onClick={() => window.location.href = '/signup'}>
            Sign Up
          </button>
        </div>
      </form>
    </div>
  );
};

export default Login;