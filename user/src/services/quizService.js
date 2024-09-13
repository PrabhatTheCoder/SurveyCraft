export const fetchQuiz = async (quizId) => {
    if (!quizId) {
        throw new Error('Quiz ID is required');
    }
    const response = await fetch(`/quizzes/api/quizzes/${quizId}/`);
    if (!response.ok) {
        throw new Error('Network response was not ok');
    }
    return response.json();
};
