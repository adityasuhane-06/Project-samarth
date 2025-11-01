import { useState, useEffect } from 'react'
import Header from './components/Header'
import ServerStats from './components/ServerStats'
import SampleQuestions from './components/SampleQuestions'
import QueryForm from './components/QueryForm'
import ResultDisplay from './components/ResultDisplay'
import ErrorMessage from './components/ErrorMessage'
import LoadingSpinner from './components/LoadingSpinner'
import { healthCheck, submitQuery } from './services/api'
import { SAMPLE_QUESTIONS } from './utils/constants'

function App() {
  const [question, setQuestion] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [serverHealth, setServerHealth] = useState(null)

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

  return (
    <div className="min-h-screen py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        <Header />
        
        {serverHealth && <ServerStats health={serverHealth} />}

        <div className="bg-white rounded-2xl shadow-2xl p-8 space-y-6 fade-in">
          <SampleQuestions 
            questions={SAMPLE_QUESTIONS} 
            onSelectQuestion={loadSampleQuestion} 
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
  )
}

export default App
