import React, { useEffect, useState } from 'react';

const QuizDashboard = () => {
    const [quizzes, setQuizzes] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchQuizzes = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/quizzes/api/quizzes/', {
                    method: 'GET',
                    mode: 'cors',  // Allow CORS
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                
                const data = await response.json();
                setQuizzes(data.quizzes);
            } catch (err) {
                setError('Failed to fetch quizzes');
            } finally {
                setLoading(false);
            }
        };

        fetchQuizzes();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div className="dashboard-container">
            <h1>Quiz Dashboard</h1>
            <ul>
                {quizzes.length > 0 ? (
                    quizzes.map((quiz) => (
                        <li key={quiz.id}>
                            {quiz.title} - Created on {quiz.created_at}
                            <a href={`/edit-quiz/${quiz.id}`}>Edit</a>
                        </li>
                    ))
                ) : (
                    <li>No quizzes found.</li>
                )}
            </ul>
            <a href="/create-quiz">+ Create New Quiz</a>
        </div>
    );
};

export default QuizDashboard;
