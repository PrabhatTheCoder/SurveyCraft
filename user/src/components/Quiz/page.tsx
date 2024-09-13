import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import quizData from '../../../quizData.json';

const QuizQuestion = () => {
  const [selectedOptions, setSelectedOptions] = useState<(number | number[] | null)[]>(Array(quizData.length).fill(null));
  const [timeLeft, setTimeLeft] = useState(120); // 2 minutes = 120 seconds
  const [showResults, setShowResults] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    if (timeLeft === 0) {
      setShowResults(true);
    }

    const timerId = setInterval(() => {
      setTimeLeft((prevTime) => prevTime - 1);
    }, 1000);

    return () => clearInterval(timerId);
  }, [timeLeft]);

  const handleOptionSelect = (questionIndex: number, optionIndex: number) => {
    const newSelectedOptions = [...selectedOptions];

    if (Array.isArray(quizData[questionIndex].correctAnswerIndex)) {
      // Multiple-answer question
      if (!Array.isArray(newSelectedOptions[questionIndex])) {
        newSelectedOptions[questionIndex] = [];
      }

      const currentSelection = newSelectedOptions[questionIndex] as number[];
      if (currentSelection.includes(optionIndex)) {
        newSelectedOptions[questionIndex] = currentSelection.filter((index) => index !== optionIndex);
      } else {
        newSelectedOptions[questionIndex] = [...currentSelection, optionIndex];
      }
    } else {
      // Single-answer question
      newSelectedOptions[questionIndex] = optionIndex;
    }

    setSelectedOptions(newSelectedOptions);
  };

  const handleSubmitQuiz = () => {
    setShowResults(true);
  };

  const handleRetakeQuiz = () => {
    setSelectedOptions(Array(quizData.length).fill(null));
    setShowResults(false);
    setTimeLeft(120);
  };

  const handleGoHome = () => {
    navigate('/'); // Redirect to Home Page
  };

  const correctAnswersCount = selectedOptions.reduce((count, answer, index) => {
    const correctAnswer = quizData[index].correctAnswerIndex;

    if (Array.isArray(correctAnswer) && Array.isArray(answer)) {
      return answer.sort().join() === correctAnswer.sort().join() ? count + 1 : count;
    }

    return answer === correctAnswer ? count + 1 : count;
  }, 0);

  if (showResults) {
    return (
      <div className="bg-gray-100 flex min-h-screen">
        <div className="container mx-auto p-8">
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-4xl font-bold">Quiz Results</h2>
            <p className="mt-4 text-lg">You got {correctAnswersCount} out of {quizData.length} questions correct.</p>
            
            <div className="mt-8 items-center">
              {quizData.map((question, index) => (
                <div key={index} className="mb-4">
                  <h3 className="font-bold">{question.question}</h3>
                  <p>Your answer: {Array.isArray(selectedOptions[index]) ? (selectedOptions[index] as number[]).map(i => question.options[i]).join(', ') : question.options[selectedOptions[index] as number]}</p>
                  
                  {Array.isArray(selectedOptions[index]) && Array.isArray(quizData[index].correctAnswerIndex) && selectedOptions[index]?.sort().join() !== (quizData[index].correctAnswerIndex as number[]).sort().join() && (
                    <p className="text-red-500">Correct answer: {(quizData[index].correctAnswerIndex as number[]).map(i => question.options[i]).join(', ')}</p>
                  )}
                  {!Array.isArray(selectedOptions[index]) && selectedOptions[index] !== quizData[index].correctAnswerIndex && (
                    <p className="text-red-500">Correct answer: {question.options[quizData[index].correctAnswerIndex as number]}</p>
                  )}
                </div>
              ))}
            </div>

            <div className="mt-8 flex space-x-4">
              <button
                className="bg-rose-500 hover:bg-black duration-150 text-white font-bold py-2 px-4 rounded"
                onClick={handleRetakeQuiz}
              >
                Retake Quiz
              </button>
              <button
                className="bg-blue-500 hover:bg-blue-700 duration-150 text-white font-bold py-2 px-4 rounded"
                onClick={handleGoHome}
              >
                Go to Home
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-gray-100 flex min-h-screen">
      <div className="container mx-auto p-8">
        <div className="bg-white rounded-lg shadow-md p-8">
          <div className="flex justify-between items-center">
            <h2 className="text-2xl font-bold">Quiz</h2>
            <div className="text-white p-3 bg-black font-bold text-2xl rounded-lg">
              {Math.floor(timeLeft / 60)}:{('0' + (timeLeft % 60)).slice(-2)}
            </div>
          </div>

          <form className="mt-8 space-y-8">
            {quizData.map((question, index) => (
              <div key={index}>
                <h1 className="text-3xl text-left font-bold mt-4">{index + 1}. {question.question}</h1>
                <div className="mt-4">
                  {question.options.map((option, optionIndex) => (
                    <div
                      key={optionIndex}
                      className={`flex items-center bg-gray-200 rounded-md p-4 mb-2 w-full text-left hover:bg-rose-300 duration-200 cursor-pointer ${
                        Array.isArray(selectedOptions[index])
                          ? (selectedOptions[index] as number[]).includes(optionIndex)
                            ? 'bg-rose-500 border border-black text-white'
                            : ''
                          : selectedOptions[index] === optionIndex
                          ? 'bg-rose-500 border border-black text-white'
                          : ''
                      }`}
                      onClick={() => handleOptionSelect(index, optionIndex)}
                    >
                      <span className="mr-4">
                        {Array.isArray(quizData[index].correctAnswerIndex) ? (
                          <input
                            type="checkbox"
                            checked={Array.isArray(selectedOptions[index]) && (selectedOptions[index] as number[]).includes(optionIndex)}
                            readOnly
                            className="form-checkbox h-5 w-5 text-rose-600"
                          />
                        ) : (
                          <span className={`h-5 w-5 inline-block rounded-full border-2 ${selectedOptions[index] === optionIndex ? 'bg-rose-200 border-white-600' : 'border-gray-400'}`}></span>
                        )}
                      </span>
                      {option}
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </form>

          <button
            className="mt-8 bg-rose-500 hover:bg-black duration-150 text-white font-bold py-2 px-4 rounded"
            onClick={handleSubmitQuiz}
          >
            Submit Quiz
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizQuestion;
