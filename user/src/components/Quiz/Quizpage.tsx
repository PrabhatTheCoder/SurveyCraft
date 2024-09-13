import React from 'react';
import { useParams } from 'react-router-dom';
import QuizDetail from './HomePage'; // Import your QuizDetail component

const QuizPage = () => {
    const { quizId } = useParams();  // Extract quizId from URL

    console.log('Quiz ID:', quizId); // Debugging to ensure the quizId is correctly extracted

    if (!quizId) {
        return <div>Quiz ID is missing</div>;  // If quizId is undefined or missing
    }

    return (
        <div>
            <h1>Quiz Details</h1>
            <QuizDetail quizId={quizId} />
        </div>
    );
};

export default QuizPage;
