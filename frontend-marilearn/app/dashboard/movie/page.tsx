"use client"
import React, { useEffect, useState } from 'react';
import FoodsDrinksRecommendationTable from '@/components/FoodsDrinksRecommendationTable';

const Movie: React.FC = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const handleLogout = () => {
    localStorage.removeItem('token');
    window.location.href = '/';
  };

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (token) {
      setIsAuthenticated(true);
    } else {
      window.location.href = '/';
    }
  }, []);

  if (!isAuthenticated) {
    return <div>Unauthorized</div>;
  }
  
  return (
    <div className="flex flex-col items-center mt-10 pt-10">
      <h1 className="text-4xl font-bold mb-6 text-blue-600">Foods & Drinks Recommendation</h1>

      <div className="flex space-x-4 pt-4">
        <a href="/dashboard" className="bg-blue-500 text-white py-2 px-4 rounded">Manajemen Edutech</a>
        <a href="/dashboard/recommendation" className="bg-green-500 text-white py-2 px-4 rounded">Recommendation</a>
        <a href="/dashboard/movie" className="bg-yellow-500 text-white py-2 px-4 rounded">Foods & Drinks</a>
      </div>

      <div className="mt-8 w-5/6 pt-4">
        <h2 className="flex text-2xl font-bold mb-4 justify-center items-center text-green-600">Beverage Recommendations</h2>
        <p className='text-justify'>Beverage Recommendation ini merupakan rekomendasi minuman hasil integrasi dengan suatu API yang telah ada pada internet (milik Fikri Naufal) namun saya mengintegrasikannya dengan memastikan student id saya menyimpan umur, tinggi badan, dan berat badan yang dibutuhkan untuk memroses data rekomendasi minuman. </p>
        <li>Masukkan Student ID dengan angka (4, 5, 6, 7, dll)</li>
        <li>Masukkan Gender dengan (Male or Female)</li>
        <li>Masukkan Weather dengan (yes or no)</li>
        <li>Masukkan Activity dengan (sedentary, lightly_active, moderately_active, very_active, extra_active)</li>
        <li>Masukkan Max Recommendation dengan angka (1, 2, 3)</li>
          <FoodsDrinksRecommendationTable />
      </div>
    </div>
  );
};

export default Movie;