"use client"
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface InstructorRecommendationData {
  instructor_id: number;
  instructor_name: string;
  instructor_bio: string;
  instructor_specialty: string;
}

const InstructorRecommendationTable: React.FC = () => {
  const [studentId, setStudentId] = useState<number | undefined>();
  const [recommendationData, setRecommendationData] = useState<InstructorRecommendationData[]>([]);

  const handleSearch = async () => {
    try {
      const response = await axios.get(`http://marilearnedu.gjeyefeubba0fndn.eastus.azurecontainer.io/instructors/recommendations/${studentId}`);
      setRecommendationData(response.data.result);
    } catch (error) {
      console.error('An error occurred while fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="flex text-2xl font-bold mb-4 justify-center items-center text-yellow-500">Instructor Recommendation Table</h1>
      <li>Masukkan ID Student untuk mencari instructor yang sesuai dengan minat student tersebut serta keahlian instructor</li>
      <li>Tekan tombol search untuk melakukan pencarian</li>
      <li>Tunggu sebentar</li>
      <li>Daftar instructor yang direkomendasikan akan ditampilkan pada tabel</li>

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
            <th className="border border-gray-300 px-4 py-2">Instructor ID</th>
            <th className="border border-gray-300 px-4 py-2">Instructor Name</th>
            <th className="border border-gray-300 px-4 py-2">Instructor Bio</th>
            <th className="border border-gray-300 px-4 py-2">Instructor Specialty</th>
          </tr>
        </thead>
        <tbody>
          {recommendationData.map((instructorRecommendation) => (
            <tr key={instructorRecommendation.instructor_id}>
              <td className="border border-gray-300 px-4 py-2">{instructorRecommendation.instructor_id}</td>
              <td className="border border-gray-300 px-4 py-2">{instructorRecommendation.instructor_name}</td>
              <td className="border border-gray-300 px-4 py-2">{instructorRecommendation.instructor_bio}</td>
              <td className="border border-gray-300 px-4 py-2">{instructorRecommendation.instructor_specialty}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default InstructorRecommendationTable;