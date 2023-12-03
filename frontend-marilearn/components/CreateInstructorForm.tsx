"use client"
import React, { useState } from 'react';

const CreateInstructorForm: React.FC = () => {
  // State to store instructor data
  const [instructorData, setInstructorData] = useState({
    instructor_name: '',
    instructor_bio: '',
    instructor_specialty: '',
  });

  // Function to handle input changes
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setInstructorData((prevData) => ({ ...prevData, [name]: value }));
  };

  // Function to add a new instructor
  const handleAddInstructor = () => {
    // Do something with the instructor data (e.g., send to the server)
    console.log('Adding instructor:', instructorData);
    // Reset data after adding
    setInstructorData({
      instructor_name: '',
      instructor_bio: '',
      instructor_specialty: '',
    });
  };

  return (
    <div className="flex w-full justify-center items-center">
      <div className="bg-gray-700 p-6 rounded-2xl w-3/5 justify-center items-center">
        <h2 className="text-xl font-bold mb-4 text-gray-100 text-center">Create Instructor</h2>

        <div className="mb-4">
          <label htmlFor="instructor_name" className="block text-sm font-bold text-gray-300">
            Name
          </label>
          <input
            type="text"
            id="instructor_name"
            name="instructor_name"
            value={instructorData.instructor_name}
            onChange={handleInputChange}
            placeholder='Enter Instructor Name'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="instructor_bio" className="block text-sm font-bold text-gray-300">
            Bio
          </label>
          <input
            type="text"
            id="instructor_bio"
            name="instructor_bio"
            value={instructorData.instructor_bio}
            onChange={handleInputChange}
            placeholder='Enter Instructor Bio'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="instructor_specialty" className="block text-sm font-bold text-gray-300">
            Specialty
          </label>
          <input
            type="text"
            id="instructor_specialty"
            name="instructor_specialty"
            value={instructorData.instructor_specialty}
            onChange={handleInputChange}
            placeholder='Enter Instructor Specialty'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <button
          type="button"
          onClick={handleAddInstructor}
          className="bg-blue-500 text-white p-2 rounded-md w-full"
        >
          Add Instructor
        </button>
      </div>
    </div>
  );
};

export default CreateInstructorForm;