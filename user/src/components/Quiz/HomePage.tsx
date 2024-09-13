import React, { useEffect, useState } from 'react';
import { fetchQuiz } from '../../services/quizService';

const QuizDetail = ({ quizId }) => {
    const [quiz, setQuiz] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        console.log('Quiz ID:', quizId); // Debug line

        const getQuiz = async () => {
            if (!quizId) {
                setError('BRUHHHH!!!');
                setLoading(false);
                return;
            }

            try {
                const data = await fetchQuiz(quizId);
                setQuiz(data);
            } catch (err) {
                setError('Failed to fetch quiz');
            } finally {
                setLoading(false);
            }
        };

        getQuiz();
    }, [quizId]);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    if (!quiz) return <div>No quiz found</div>;

    return (
        <div>
            <h1>{quiz.title}</h1>
            <p>{quiz.description}</p>
            <div>
                {quiz.questions.map((question) => (
                    <div key={question.id}>
                        <h3>{question.title}</h3>
                        {question.question_type === 'radio' && (
                            <div>
                                {question.choices.map((choice) => (
                                    <div key={choice.id}>
                                        <input
                                            type="radio"
                                            id={`choice_${choice.id}`}
                                            name={`question_${question.id}`}
                                            value={choice.id}
                                        />
                                        <label htmlFor={`choice_${choice.id}`}>{choice.text}</label>
                                    </div>
                                ))}
                            </div>
                        )}
                        {question.question_type === 'checkbox' && (
                            <div>
                                {question.choices.map((choice) => (
                                    <div key={choice.id}>
                                        <input
                                            type="checkbox"
                                            id={`choice_${choice.id}`}
                                            name={`question_${question.id}[]`}
                                            value={choice.id}
                                        />
                                        <label htmlFor={`choice_${choice.id}`}>{choice.text}</label>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default QuizDetail;
