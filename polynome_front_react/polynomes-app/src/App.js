import React, { useState } from 'react';
import axios from 'axios';

const PolynomialCalculator = () => {
  const [equation, setEquation] = useState('');
  const [a, setA] = useState('');
  const [b, setB] = useState('');
  const [c, setC] = useState('');
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

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
                    onClick={handleReset}
                    className="px-4 py-2 bg-red-500 text-white rounded-lg hover:bg-red-600"
                >
                  Reset
                </button>
              </div>
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
