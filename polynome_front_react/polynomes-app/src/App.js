import React, { useState } from 'react';
import axios from 'axios';

const PolynomialCalculator = () => {
  const [equation, setEquation] = useState('');
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [c, setC] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [quizQuestion, setQuizQuestion] = useState('');
  const [userAnswer, setUserAnswer] = useState('');
  const [quizSolution, setQuizSolution] = useState('');
  const [quizExplanation, setQuizExplanation] = useState('');
  const [showQuizModal, setShowQuizModal] = useState(false);
  const [showSolutionModal, setShowSolutionModal] = useState(false);


  const handleCalculation = async (endpoint) => {
    if (!equation && endpoint !== 'quadratique') {
      setResult('Please enter a polynomial equation.');
      return;
    }
    if (endpoint === 'quadratique' && (!a || !b || !c)) {
      setResult('Please enter values for a, b, and c.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(`http://127.0.0.1:8081/${endpoint}`, {
        equation: endpoint === 'quadratique' ? `${a}x^2 + ${b}x + ${c}` : equation,
        a, b, c,
        variable: 'x',
      });
      if (response.data) {
        setResult(
            typeof response.data === 'string'
                ? response.data
                : Object.entries(response.data)
                    .map(([key, value]) => `${key}: ${value}`)
                    .join('\n')
        );
      } else {
        setResult('No result returned from the server.');
      }
    } catch (error) {
      setResult(
          `Error: ${error.response?.data?.error || 'Failed to calculate.'}`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleRecommendation = async () => {
    if (!equation) {
      setResult('Please enter a polynomial equation for recommendation.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8081/recommend', {
        polynomial: equation,
      });
      if (response.data) {
        setResult(
            `Recommended Method: ${response.data.recommended_method}\nExplanation: ${response.data.explanation}`
        );
      } else {
        setResult('No recommendation returned from the server.');
      }
    } catch (error) {
      setResult(
          `Error: ${error.response?.data?.error || 'Failed to get recommendation.'}`
      );
    } finally {
      setLoading(false);
    }
  };

  const handleShowGraph = async () => {
    if (!equation) {
      alert('Please enter a polynomial equation.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post(
          `http://127.0.0.1:8081/plot`,
          { equation },
          { responseType: 'blob' }
      );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setResult(
          <img
              src={url}
              alt="Polynomial Graph"
              className="w-full rounded-lg shadow-md"
          />
      );
    } catch (error) {
      alert(`Error: ${error.response?.data?.error || 'Failed to fetch graph.'}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setEquation('');
    setA('');
    setB('');
    setC('');
    setResult('');
  };
  const handleGenerateQuiz = async () => {
    if (!equation) {
      setResult('Please enter a polynomial equation to generate a quiz.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://127.0.0.1:8081/quiz', {
        polynomial: equation,
      });
      if (response.data) {
        setQuizQuestion(response.data.question);
        setQuizSolution(response.data.solution);
        setQuizExplanation(response.data.explanation);
        setShowQuizModal(true); // Afficher la fenêtre modale du quiz
      } else {
        setResult('No quiz data returned from the server.');
      }
    } catch (error) {
      setResult(
          `Error: ${error.response?.data?.error || 'Failed to generate quiz.'}`
      );
    } finally {
      setLoading(false);
    }
  };
  const handleShowPredictionGraph = async () => {
    if (!equation) {
      alert('Please enter a polynomial equation.');
      return;
    }
    const numbersOnly = equation.match(/-?\d+/g)?.map(Number);
    if (!numbersOnly || numbersOnly.length === 0) {
      alert('No valid numbers found in the equation.');
      return;
    }
    setLoading(true);
    try {
      const response = await axios.post(
          `http://127.0.0.1:8081/predict-and-plot`,
      { x_values: numbersOnly },
      { responseType: 'blob' }
    );
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setResult(
          <img
              src={url}
              alt="Prediction Graph"
              className="w-full rounded-lg shadow-md"
          />
      );
    } catch (error) {
      alert(`Error:${error.response?.data?.error || 'Failed to fetch prediction graph.'}`);
    } finally {
      setLoading(false);
    }
  };


  return (
      <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-purple-100 to-pink-100 flex items-center justify-center p-4">
        <div className="w-full max-w-2xl bg-white rounded-2xl shadow-2xl overflow-hidden relative">
          <div className="relative p-8">
            <h2 className="text-4xl font-extrabold text-center text-indigo-600 mb-6">
              Polynomial Calculator
            </h2>

            {/* Quadratic Equation Section */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-indigo-600 mb-2">Quadratic Equation</h3>
              <div className="grid grid-cols-3 gap-4 mb-4">
                <input
                    type="number"
                    placeholder="a"
                    className="p-2 border-2 border-indigo-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    value={a}
                    onChange={(e) => setA(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="b"
                    className="p-2 border-2 border-indigo-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    value={b}
                    onChange={(e) => setB(e.target.value)}
                />
                <input
                    type="number"
                    placeholder="c"
                    className="p-2 border-2 border-indigo-300 rounded-lg focus:outline-none focus:border-indigo-500"
                    value={c}
                    onChange={(e) => setC(e.target.value)}
                />
              </div>
              <button
                  onClick={() => handleCalculation('quadratique')}
                  className="w-full px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
              >
                Solve Quadratic
              </button>
            </div>

            {/* General Polynomial Section */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-indigo-600 mb-2">General Polynomial</h3>
              <textarea
                  rows="4"
                  className="w-full p-4 border-2 border-indigo-300 rounded-lg focus:outline-none focus:border-indigo-500"
                  placeholder="Enter polynomial equation (e.g., x^2 - 4)"
                  value={equation}
                  onChange={(e) => setEquation(e.target.value)}
              />
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-4 mt-4">
                {['racines', 'factoriser', 'newton', 'Show Graph'].map((btn) => (
                    <button
                        key={btn}
                        onClick={() => btn === 'Show Graph' ? handleShowGraph() : handleCalculation(btn)}
                        className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600"
                    >
                      {btn}
                    </button>
                ))}
                <button
                    onClick={handleShowPredictionGraph}
                    className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                >
                  Show Prediction Graph
                </button>

                <button
                    onClick={handleReset}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                >
                  Reset
                </button>
              </div>
            </div>
            {/* Quiz Modal */}
            {showQuizModal && (
                <div className="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center">
                  <div className="bg-white p-6 rounded-lg shadow-lg w-1/2">
                    <h3 className="text-xl font-semibold mb-4">Quiz Question</h3>
                    <p className="mb-4">{quizQuestion}</p>
                    <textarea
                        rows="4"
                        className="w-full p-2 border-2 border-indigo-300 rounded-lg focus:outline-none focus:border-indigo-500"
                        placeholder="Enter your answer here..."
                        value={userAnswer}
                        onChange={(e) => setUserAnswer(e.target.value)}
                    />
                    <div className="flex justify-end mt-4">
                      <button
                          onClick={() => setShowQuizModal(false)}
                          className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600 mr-2"
                      >
                        Cancel
                      </button>
                      <button
                          onClick={() => {
                            setShowQuizModal(false);
                            setShowSolutionModal(true);
                          }}
                          className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600"
                      >
                        Submit Answer
                      </button>
                    </div>
                  </div>
                </div>
            )}

            {/* Solution Modal */}
            {showSolutionModal && (
                <div className="fixed inset-0 bg-gray-800 bg-opacity-75 flex items-center justify-center">
                  <div className="bg-white p-6 rounded-lg shadow-lg w-1/2">
                    <h3 className="text-xl font-semibold mb-4">Solution</h3>
                    <p className="mb-4"><strong>Correct Solution:</strong> {quizSolution}</p>
                    <p className="mb-4"><strong>Explanation:</strong> {quizExplanation}</p>
                    <div className="flex justify-end mt-4">
                      <button
                          onClick={() => setShowSolutionModal(false)}
                          className="px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600"
                      >
                        Close
                      </button>
                    </div>
                  </div>
                </div>
            )}

            {/* Quiz Section */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-yellow-600 mb-2">Generate Quiz</h3>
              <button
                  onClick={handleGenerateQuiz}
                  className="w-full px-4 py-2 bg-yellow-500 text-white rounded-lg hover:bg-yellow-600 mt-4"
              >
                Generate Quiz
              </button>
            </div>


            {/* Recommendation Section */}
            <div className="mb-6">
              <h3 className="text-xl font-semibold text-indigo-600 mb-2">Recommend Method</h3>
              <button
                  onClick={handleRecommendation}
                  className="w-full px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 mt-4"
              >
                Recommend Method
              </button>
            </div>

            {/* Result Section */}
            <div className="border-2 border-indigo-200 p-6 bg-white rounded-lg min-h-[150px]">
              {loading ? (
                  <div className="text-center">
                    <span className="animate-spin inline-block w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full"></span>
                  </div>
              ) : (
                  <pre className="text-sm text-indigo-800 whitespace-pre-wrap">{result}</pre>
              )}
            </div>
          </div>
        </div>
      </div>
  );
};

export default PolynomialCalculator;