import React, { useState } from 'react';
import { Link } from 'react-router-dom';

interface NavbarProps {
  user: { name: string; email: string } | null;
}

const Navbar: React.FC<NavbarProps> = ({ user }) => {
  const [isOpen, setIsOpen] = useState(false);

  const toggleMenu = () => {
    setIsOpen(!isOpen);
  };

  return (
    <header >
      <nav className="bg-rose-500 w-full p-4">
        <div className="container mx-auto w-full flex justify-between items-center">
          <div className="text-white text-2xl font-bold">MyWebsite</div>

          {/* Hamburger Menu Button */}
          <div className="md:hidden">
            <button onClick={toggleMenu} className="text-white focus:outline-none">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d={isOpen ? 'M6 18L18 6M6 6l12 12' : 'M4 6h16M4 12h16M4 18h16'}></path>
              </svg>
            </button>
          </div>

          {/* Navbar Links */}
          <div className={`flex flex-col  md:flex-row md:space-x-6 mt-4 md:mt-0 ${isOpen ? 'block' : 'hidden'} md:block`}>
            <Link to="/home" className="text-white text-lg hover:bg-rose-600 rounded-lg px-3 py-2">Home</Link>
            {/* <Link to="/quiz" className="text-white text-lg hover:bg-rose-600 rounded-lg px-3 py-2">Quiz</Link> */}
            <Link to="/blog" className="text-white text-lg hover:bg-rose-600 rounded-lg px-3 py-2">Blog</Link>
            <Link to="/contact" className="text-white text-lg hover:bg-rose-600 rounded-lg px-3 py-2">Contact Us</Link>
          </div>
          {user && (
              <div className="text-white text-lg rounded-lg px-3 py-2">
                <span>Welcome, {user.name}</span> | <span>{user.email}</span>
              </div>
            )}
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
