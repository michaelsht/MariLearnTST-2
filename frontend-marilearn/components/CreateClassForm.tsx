"use client"
import React, { useState } from 'react';

const CreateClassForm: React.FC = () => {
  // State untuk menyimpan data class
  const [classData, setClassData] = useState({
    class_name: '',
    class_description: '',
    class_instructor: '',
  });

  // Fungsi untuk menangani perubahan pada input
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setClassData((prevData) => ({ ...prevData, [name]: value }));
  };

  // Fungsi untuk menambahkan class
  const handleAddClass = () => {
    // Lakukan sesuatu dengan data class (misalnya, kirim ke server)
    console.log('Menambahkan class:', classData);
    // Reset data setelah menambahkan
    setClassData({
      class_name: '',
      class_description: '',
      class_instructor: '',
    });
  };

  return (
    <div className="flex w-full justify-center items-center">
      <div className="bg-gray-700 p-6 rounded-2xl w-3/5 justify-center items-center">
        <h2 className="text-xl font-bold mb-4 text-gray-100 text-center">Create Class</h2>

        <div className="mb-4">
          <label htmlFor="class_name" className="block text-sm font-bold text-gray-300">
            Name
          </label>
          <input
            type="text"
            id="class_name"
            name="class_name"
            value={classData.class_name}
            onChange={handleInputChange}
            placeholder='Enter Class Name'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="class_description" className="block text-sm font-bold text-gray-300">
            Description
          </label>
          <input
            type="text"
            id="class_description"
            name="class_description"
            value={classData.class_description}
            onChange={handleInputChange}
            placeholder='Enter Class Description'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <div className="mb-4">
          <label htmlFor="class_instructor" className="block text-sm font-bold text-gray-300">
            Instructor
          </label>
          <input
            type="text"
            id="class_instructor"
            name="class_instructor"
            value={classData.class_instructor}
            onChange={handleInputChange}
            placeholder='Enter Class Instructor'
            className="mt-1 p-2 w-full border rounded-md focus:outline-none focus:ring focus:border-blue-300 text-black border-1 border-black"
          />
        </div>

        <button
          type="button"
          onClick={handleAddClass}
          className="bg-blue-500 text-white p-2 rounded-md w-full"
        >
          Add Class
        </button>
      </div>
    </div>
  );
};

export default CreateClassForm;
