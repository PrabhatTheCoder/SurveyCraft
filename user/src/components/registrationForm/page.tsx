import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

interface ProxyRegistrationFormProps {
  onRegister: (user: { name: string; email: string }) => void;
}

const ProxyRegistrationForm: React.FC<ProxyRegistrationFormProps> = ({ onRegister }) => {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    const userDetails = { name, email };
    onRegister(userDetails); // Pass user details to parent
    navigate('/home'); // Redirect to home page after registration
  };

  return (
    <div className="max-w-sm mt-40 mx-auto p-6 border border-gray-300 rounded-md text-center bg-white">
      <h2 className="text-2xl mb-4 text-black font-sans">Proxy Registration Form</h2>
      <p className="text-sm mb-6 text-black font-sans">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo
      </p>
      <form onSubmit={handleSubmit}>
        <div className="mb-4 text-left">
          <label htmlFor="name" className="block mb-2 font-sans font-bold text-black">Name</label>
          <input 
            type="text" 
            id="name" 
            value={name} 
            onChange={(e) => setName(e.target.value)} 
            className="w-full p-2 border border-black rounded-md bg-white text-black"
          />
        </div>
        <div className="mb-4 text-left">
          <label htmlFor="phone" className="block mb-2 font-bold text-black font-sans">Phone</label>
          <input 
            type="tel" 
            id="phone" 
            value={phone} 
            onChange={(e) => setPhone(e.target.value)} 
            className="w-full p-2 border border-black rounded-md bg-white text-black"
          />
        </div>
        <div className="mb-4 text-left">
          <label htmlFor="email" className="block mb-2 font-bold text-black font-sans">Email</label>
          <input 
            type="email" 
            id="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            className="w-full p-2 border border-black rounded-md bg-white text-black"
          />
        </div>
        <button type="submit" className="w-full p-2 bg-gray-800 text-white border-2 border-black rounded-md text-lg cursor-pointer hover:bg-gray-600">
          Register
        </button>
      </form>
    </div>
  );
};

export default ProxyRegistrationForm;
