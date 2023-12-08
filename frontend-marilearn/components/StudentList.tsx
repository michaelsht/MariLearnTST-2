"use client";
import React, { useState, useEffect } from 'react';
import axios from 'axios';

interface StudentData {
  student_id: number;
  username: string;
  fullname: string;
  email: string;
  interest: string;
}

const StudentList: React.FC = () => {
  const [studentData, setStudentData] = useState<StudentData[]>([]);

  useEffect(() => {
    // Fetch initial data when the component mounts
    fetchStudentData();
  }, []);

  const fetchStudentData = async () => {
    try {
      const response = await axios.get('https://marilearntstedu.azurewebsites.net/students/');
      setStudentData(response.data.result);
    } catch (error) {
      console.error('An error occurred while fetching data:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="flex text-2xl font-bold mb-4 justify-center items-center text-yellow-500">Student List</h1>

      <table className="min-w-full border border-gray-300">
        <thead>
          <tr>
            <th className="border border-gray-300 px-4 py-2">Student ID</th>
            <th className="border border-gray-300 px-4 py-2">Username</th>
            <th className="border border-gray-300 px-4 py-2">Full Name</th>
            <th className="border border-gray-300 px-4 py-2">Email</th>
            <th className="border border-gray-300 px-4 py-2">Interest</th>
          </tr>
        </thead>
        <tbody>
          {studentData.map((student) => (
            <tr key={student.student_id}>
              <td className="border border-gray-300 px-4 py-2">{student.student_id}</td>
              <td className="border border-gray-300 px-4 py-2">{student.username}</td>
              <td className="border border-gray-300 px-4 py-2">{student.fullname}</td>
              <td className="border border-gray-300 px-4 py-2">{student.email}</td>
              <td className="border border-gray-300 px-4 py-2">{student.interest}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default StudentList;