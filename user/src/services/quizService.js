export const fetchQuiz = async (quizId) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/api/quiz/${quizId}/`);
        if (!response.ok) {
            throw new Error('Failed to fetch quiz');
        }
        return await response.json();
    } catch (error) {
        console.error(error);
        throw error;
    }
};