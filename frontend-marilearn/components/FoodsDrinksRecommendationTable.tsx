"use client"
// components/FoodsDrinksRecommendationTable.tsx
// components/FoodsDrinksRecommendationTable.tsx
import React, { useState } from 'react';
import axios from 'axios';

interface FoodDrinkData {
  name: string;
  description: string;
  category: string;
  calories: number;
  protein: number;
  fats: number;
  carbs: number;
  sugar: number;
}

const FoodsDrinksRecommendationTable: React.FC = () => {
  const [activity, setActivity] = useState<string>('');
  const [age, setAge] = useState<number | undefined>();
  const [gender, setGender] = useState<string>('');
  const [height, setHeight] = useState<number | undefined>();
  const [max_rec, setMaxRec] = useState<number | undefined>();
  const [weather, setWeather] = useState<string>('');
  const [weight, setWeight] = useState<number | undefined>();
  const [recommendationData, setRecommendationData] = useState<FoodDrinkData[]>([]);

  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:8000/recommendations', {
        activity,
        age,
        gender,
        height,
        max_rec,
        weather,
        weight,
      });
      setRecommendationData(response.data);
    } catch (error) {
      console.error('An error occurred while fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 gap-4">
        <div className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Activity"
            value={activity}
            onChange={(e) => setActivity(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <input
            type="number"
            placeholder="Age"
            value={age || undefined}
            onChange={(e) => setAge(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="text"
            placeholder="Gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <input
            type="number"
            placeholder="Height"
            value={height || undefined}
            onChange={(e) => setHeight(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            placeholder="Max Recommendation"
            value={max_rec || undefined}
            onChange={(e) => setMaxRec(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <input
            type="text"
            placeholder="Weather"
            value={weather}
            onChange={(e) => setWeather(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            placeholder="Weight"
            value={weight || undefined}
            onChange={(e) => setWeight(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <button
            className="bg-blue-500 text-white p-2 rounded-md ml-2"
            onClick={handleSearch}
          >
            Search
          </button>
        </div>
      </div>

      <table className="min-w-full border border-gray-300 mt-4">
        <thead>
          <tr>
            <th className="border border-gray-300 px-4 py-2">Name</th>
            <th className="border border-gray-300 px-4 py-2">Description</th>
            <th className="border border-gray-300 px-4 py-2">Category</th>
            <th className="border border-gray-300 px-4 py-2">Calories</th>
            <th className="border border-gray-300 px-4 py-2">Protein</th>
            <th className="border border-gray-300 px-4 py-2">Fats</th>
            <th className="border border-gray-300 px-4 py-2">Carbs</th>
            <th className="border border-gray-300 px-4 py-2">Sugar</th>
          </tr>
        </thead>
        <tbody>
          {recommendationData.map((foodDrink) => (
            <tr key={foodDrink.name}>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.name}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.description}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.category}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.calories}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.protein}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.fats}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.carbs}</td>
              <td className="border border-gray-300 px-4 py-2">{foodDrink.sugar}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default FoodsDrinksRecommendationTable;