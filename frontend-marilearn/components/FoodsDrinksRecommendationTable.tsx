"use client"
import React, { useState } from 'react';

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
  const [studentId, setStudentId] = useState<number | undefined>();
  const [activity, setActivity] = useState<string>('');
  const [gender, setGender] = useState<string>('');
  const [max_rec, setMaxRec] = useState<number | undefined>();
  const [weather, setWeather] = useState<string>('');
  const [recommendationData, setRecommendationData] = useState<FoodDrinkData[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    setIsLoading(true);
    try {
      let age, weight, height;

      // Set values based on student_id
      if (studentId !== undefined) {
        if (studentId <= 10) {
          age = 20;
          weight = 60;
          height = 165;
        } else if (studentId > 10) {
          age = 25;
          weight = 65;
          height = 170;
        }
      }

      const response = await fetch('https://marilearntstedu.azurewebsites.net/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          activity,
          age,
          gender,
          height,
          max_rec,
          weather,
          weight,
        }),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      setRecommendationData(data);
      setIsLoading(false);
    } catch (error) {
      console.error('An error occurred while fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <div className="grid grid-cols-1 gap-4">
        <div className="grid grid-cols-2 gap-4">
          <input
            type="number"
            placeholder="Student ID"
            value={studentId || undefined}
            onChange={(e) => setStudentId(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <input
            list="activityOptions"
            placeholder="Activity"
            value={activity}
            onChange={(e) => setActivity(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />

          <datalist id="activityOptions">
            <option value="sedentary" />
            <option value="lightly_active" />
            <option value="moderately_active" />
            <option value="very_active" />
            <option value="extra_active" />
          </datalist>
        </div>
        <div className="grid grid-cols-2 gap-4">
          <input
            list="genderOptions"
            placeholder="Gender"
            value={gender}
            onChange={(e) => setGender(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <datalist id="genderOptions">
            <option value="Male" />
            <option value="Female" />
          </datalist>
          <input
            type="number"
            placeholder="Max Recommendation"
            value={max_rec || undefined}
            onChange={(e) => setMaxRec(parseInt(e.target.value, 10) || undefined)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <input
            list="weatherOptions"
            placeholder="Weather"
            value={weather}
            onChange={(e) => setWeather(e.target.value)}
            className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
          />
          <datalist id="weatherOptions">
            <option value="yes" />
            <option value="no" />
          </datalist>
          <button
            className="bg-blue-500 text-white p-2 rounded-md ml-2"
            onClick={handleSearch}
          >
          {isLoading ? 'Searching...' : 'Search'}
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
          {recommendationData && recommendationData.map((foodDrink) => (
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