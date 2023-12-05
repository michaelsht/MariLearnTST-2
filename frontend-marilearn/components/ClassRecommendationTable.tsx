"use client"
import React, { useState, useEffect } from 'react';

interface ClassRecommendationData {
  class_id: number;
  class_name: string;
  class_description: string;
  class_instructor: number;
}

const ClassRecommendationTable: React.FC = () => {
  const [studentId, setStudentId] = useState<number | undefined>();
  const [recommendationData, setRecommendationData] = useState<ClassRecommendationData[]>([]);

  const handleSearch = async () => {
    try {
      const response = await fetch(`http://marilearnedu.gjeyefeubba0fndn.eastus.azurecontainer.io/classes/recommendations/${studentId}`, {
        method: 'GET',
      });
      const data = await response.json();
      setRecommendationData(data.result);
      console.log("DATA ", recommendationData)
      if (response.ok) {
        setRecommendationData(data.result);
      } else {
        console.error(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('An error occurred while fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="flex text-2xl font-bold mb-4 justify-center items-center text-green-600">Class Recommendation Table</h1>
      <li>Masukkan ID Student untuk mencari class yang sesuai dengan minat student tersebut</li>
      <li>Tekan tombol search untuk melakukan pencarian</li>
      <li>Tunggu sebentar</li>
      <li>Daftar class yang direkomendasikan akan ditampilkan pada tabel</li>
      <div className="mb-4 flex justify-end items-center">
        <label htmlFor="studentId" className="mr-2">
          Student ID:
        </label>
        <input
          type="number"
          id="studentId"
          value={studentId || ''}
          onChange={(e) => setStudentId(parseInt(e.target.value, 10) || undefined)}
          className="p-2 border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black"
        />
        <button className="bg-blue-500 text-white p-2 rounded-md ml-2" onClick={handleSearch}>
          Search
        </button>
      </div>

      <table className="min-w-full border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 px-4 py-2">Class ID</th>
            <th className="border border-gray-300 px-4 py-2">Class Name</th>
            <th className="border border-gray-300 px-4 py-2">Class Description</th>
            <th className="border border-gray-300 px-4 py-2">Class Instructor</th>
          </tr>
        </thead>
        <tbody>
          {recommendationData.map((classData) => (
            <tr key={classData.class_id}>
              <td className="border border-gray-300 px-4 py-2">{classData.class_id}</td>
              <td className="border border-gray-300 px-4 py-2">{classData.class_name}</td>
              <td className="border border-gray-300 px-4 py-2">{classData.class_description}</td>
              <td className="border border-gray-300 px-4 py-2">{classData.class_instructor}</td>
            </tr>
          ))}
        </tbody>
      </table>

    </div>
  );
};

export default ClassRecommendationTable;