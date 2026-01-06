import { useState, useEffect } from 'react'
import Header from './components/Header'
import ServerStats from './components/ServerStats'
import SampleQuestions from './components/SampleQuestions'
import QueryForm from './components/QueryForm'
import ResultDisplay from './components/ResultDisplay'
import ErrorMessage from './components/ErrorMessage'
import LoadingSpinner from './components/LoadingSpinner'
import NeuralBackground from './components/NeuralBackground'
import LandingPage from './components/LandingPage'
import { healthCheck, submitQuery } from './services/api'
import { SAMPLE_QUESTIONS } from './utils/constants'
import { useTheme } from './context/ThemeContext'

function App() {
  const [showLanding, setShowLanding] = useState(true)
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [serverHealth, setServerHealth] = useState(null)
  const { isDark } = useTheme()

  useEffect(() => {
    checkServerHealth()
  }, [])

  const checkServerHealth = async () => {
    try {
      const data = await healthCheck()
      setServerHealth(data)
    } catch (err) {
      console.error('Server health check failed:', err)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!question.trim()) {
      setError('Please enter a question')
      return
    }

    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await submitQuery(question)
      setResult(data)
    } catch (err) {
      setError(err.message || 'An error occurred while processing your query')
    } finally {
      setLoading(false)
    }
  }

  const loadSampleQuestion = (sampleQ) => {
    setQuestion(sampleQ)
    setError(null)
    setResult(null)
  }

  const hasQuery = question.trim().length > 0

  return (
    <div className="min-h-screen relative overflow-hidden">
      <NeuralBackground hasQuery={hasQuery && !showLanding} />
      
      {showLanding ? (
        <LandingPage onEnter={() => setShowLanding(false)} />
      ) : (
        <div className="py-8 px-4 sm:px-6 lg:px-8 relative fade-in" style={{ zIndex: 10 }}>
          <div className="max-w-7xl mx-auto relative">
            <Header hasQuery={hasQuery} />
            
            {serverHealth && <ServerStats health={serverHealth} hasQuery={hasQuery} />}

            <div className={`${isDark ? `glass-dark border-2 ${hasQuery ? 'border-yellow-600/70' : 'border-silver-500/50'}` : 'glass-light'} rounded-2xl p-8 space-y-6 fade-in transition-all duration-500`}>
              <SampleQuestions 
                questions={SAMPLE_QUESTIONS} 
                onSelectQuestion={loadSampleQuestion}
                hasQuery={hasQuery}
              />

              <QueryForm
                question={question}
                setQuestion={setQuestion}
                onSubmit={handleSubmit}
                loading={loading}
              />

              {loading && <LoadingSpinner />}

              {error && <ErrorMessage message={error} />}

              {result && <ResultDisplay result={result} />}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
