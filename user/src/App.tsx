import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, useLocation } from 'react-router-dom';
import Navbar from './components/Quiz/Navbar';
import HomePage from './components/Quiz/HomePage';
import QuizQuestion from './components/Quiz/page';
import BlogList from './components/Blog/Blog';
import BlogDetail from './components/Blog/BlogDetail';
import ProxyRegistrationForm from './components/registrationForm/page';
import QuizPage from './components/Quiz/Quizpage';
import QuizDashboard from './components/Quiz/QuizDashboard';
const App: React.FC = () => {
  const [user, setUser] = useState<{ name: string; email: string } | null>(null);

  const handleRegister = (userDetails: { name: string; email: string }) => {
    setUser(userDetails);
  };

  return (
    <Router>
      <div>
        <Routes>
          <Route 
            path="/" 
            element={
              <ConditionalNavbar user={user}>
                {user ? <HomePage /> : <ProxyRegistrationForm onRegister={handleRegister} />}
              </ConditionalNavbar>
            } 
          />
          <Route path="/quizzes/:quizId" element={<QuizPage />} />
          <Route path="/home" element={<ConditionalNavbar user={user}><HomePage /></ConditionalNavbar>} />
          <Route path="/blog" element={<ConditionalNavbar user={user}><BlogList /></ConditionalNavbar>} />
          <Route path="/blog/:blogId" element={<ConditionalNavbar user={user}><BlogDetail /></ConditionalNavbar>} />
          <Route path="/quiz" element={<ConditionalNavbar user={user}><QuizQuestion /></ConditionalNavbar>} />
          <Route path="/dashboard" element={<QuizDashboard />} />
        </Routes>
      </div>
    </Router>
  );
};

// Component to conditionally render the Navbar
const ConditionalNavbar: React.FC<{ user: { name: string; email: string } | null, children: React.ReactNode }> = ({ user, children }) => {
  const location = useLocation();
  
  // Check if the current route is the registration route
  const isRegistrationPage = location.pathname === '/';
  
  return (
    <div>
      {!isRegistrationPage && <Navbar user={user} />}
      {children}
    </div>
  );
};

export default App;
