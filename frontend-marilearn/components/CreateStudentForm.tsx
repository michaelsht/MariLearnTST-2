// components/CreateStudentForm.tsx
import React, { useState } from 'react';

const CreateStudentForm: React.FC = () => {
  // State to store student data
  const [studentData, setStudentData] = useState({
    username: '',
    fullname: '',
    email: '',
    interest: '',
  });

  // State to store error message
  const [error, setError] = useState<string | null>(null);

  // Function to handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setStudentData((prevData) => ({ ...prevData, [name]: value }));
  };

  // Function to add a new student
  const handleAddStudent = async () => {
    try {
      // Mendapatkan token akses dari local storage
      const accessToken = localStorage.getItem('access_token');

      const response = await fetch('https://marilearnedu.gjeyefeubba0fndn.eastus.azurecontainer.io/students/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({
          parameter: {
            username: studentData.username,
            fullname: studentData.fullname,
            email: studentData.email,
            interest: studentData.interest,
          },
        }),
      });

      const responseData = await response.json();

      if (response.ok) {
        console.log('Student created successfully:', responseData);
        // Reset data after adding
        setStudentData({
          username: '',
          fullname: '',
          email: '',
          interest: '',
        });
        setError(null); // Reset error state
      } else {
        console.error('Error creating student:', responseData);
        // Handle error response
        setError(responseData.detail[0].msg);
      }
    } catch (error) {
      console.error('An unexpected error occurred during student creation:', error);
      // Handle unexpected errors
      setError('An unexpected error occurred');
    }
  };

  return (
    <div className="flex w-full justify-center items-center">
      <div className="bg-gray-700 p-6 rounded-2xl w-3/5 justify-center items-center">
        <h2 className="text-xl font-bold mb-4 text-gray-100 text-center">Create Student</h2>

        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-bold text-gray-300">
            Username
          </label>
          <input
            type="text"
            id="username"
            name="username"
            value={studentData.username}
            onChange={handleInputChange}
            placeholder='Enter Username'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="fullname" className="block text-sm font-bold text-gray-300">
            Full Name
          </label>
          <input
            type="text"
            id="fullname"
            name="fullname"
            value={studentData.fullname}
            onChange={handleInputChange}
            placeholder='Enter Full Name'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="email" className="block text-sm font-bold text-gray-300">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={studentData.email}
            onChange={handleInputChange}
            placeholder='Enter Email'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="interest" className="block text-sm font-bold text-gray-300">
            Student Interest
          </label>
          <input
            type="text"
            id="interest"
            name="interest"
            value={studentData.interest}
            onChange={handleInputChange}
            placeholder='Enter Interest'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        {error && (
          <div className="text-red-500 mb-4 px-5">
            <p>{error}</p>
          </div>
        )}

        <button
          type="button"
          onClick={handleAddStudent}
          className="bg-blue-500 text-white p-2 rounded-md w-full"
        >
          Add Student
        </button>
      </div>
    </div>
  );
};

export default CreateStudentForm;