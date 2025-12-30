import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface Scenario {
  id: string
  name: string
  costMultiplier: number
  revenueMultiplier: number
  riskLevel: 'low' | 'medium' | 'high'
}

const ScenarioAnalysis = () => {
  const [baseValue, setBaseValue] = useState<number>(1000000)
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>(['optimistic'])

  const scenarios: Scenario[] = [
    { id: 'pessimistic', name: 'Pessimistic', costMultiplier: 1.3, revenueMultiplier: 0.8, riskLevel: 'high' },
    { id: 'realistic', name: 'Realistic', costMultiplier: 1.1, revenueMultiplier: 1.0, riskLevel: 'medium' },
    { id: 'optimistic', name: 'Optimistic', costMultiplier: 0.95, revenueMultiplier: 1.2, riskLevel: 'low' },
  ]

  const calculateScenario = (scenario: Scenario) => {
    const revenue = baseValue * scenario.revenueMultiplier
    const cost = baseValue * 0.75 * scenario.costMultiplier
    const profit = revenue - cost
    const margin = (profit / revenue) * 100

    return {
      scenario: scenario.name,
      revenue: revenue / 1000000,
      cost: cost / 1000000,
      profit: profit / 1000000,
      margin: margin,
    }
  }

  const chartData = scenarios
    .filter(s => selectedScenarios.includes(s.id))
    .map(calculateScenario)

  const toggleScenario = (id: string) => {
    setSelectedScenarios(prev =>
      prev.includes(id)
        ? prev.filter(s => s !== id)
        : [...prev, id]
    )
  }

  const getRiskColor = (level: 'low' | 'medium' | 'high') => {
    switch (level) {
      case 'low': return 'bg-green-100 text-green-800'
      case 'medium': return 'bg-yellow-100 text-yellow-800'
      case 'high': return 'bg-red-100 text-red-800'
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Scenario Analysis</h1>
        <p className="mt-2 text-gray-600">
          Model different project scenarios and financial outcomes
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <div className="mb-6">
          <label htmlFor="baseValue" className="block text-sm font-medium text-gray-700 mb-2">
            Base Project Value ($)
          </label>
          <input
            type="number"
            id="baseValue"
            value={baseValue}
            onChange={(e) => setBaseValue(Number(e.target.value))}
            className="block w-full max-w-xs px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            step="10000"
          />
        </div>

        <div className="mb-6">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Select Scenarios</h3>
          <div className="flex flex-wrap gap-3">
            {scenarios.map((scenario) => (
              <button
                key={scenario.id}
                onClick={() => toggleScenario(scenario.id)}
                className={`px-4 py-2 rounded-lg border-2 transition-colors ${
                  selectedScenarios.includes(scenario.id)
                    ? 'border-blue-500 bg-blue-50 text-blue-700'
                    : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                }`}
              >
                <div className="flex items-center space-x-2">
                  <span className="font-medium">{scenario.name}</span>
                  <span className={`px-2 py-0.5 rounded-full text-xs ${getRiskColor(scenario.riskLevel)}`}>
                    {scenario.riskLevel}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {chartData.length > 0 ? (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="scenario" />
              <YAxis label={{ value: 'Amount ($M)', angle: -90, position: 'insideLeft' }} />
              <Tooltip
                formatter={(value: number) => [`$${value.toFixed(2)}M`, '']}
              />
              <Legend />
              <Bar dataKey="revenue" fill="#3B82F6" name="Revenue" />
              <Bar dataKey="cost" fill="#EF4444" name="Cost" />
              <Bar dataKey="profit" fill="#10B981" name="Profit" />
            </BarChart>
          </ResponsiveContainer>
        ) : (
          <div className="text-center py-12 text-gray-500">
            Select at least one scenario to view analysis
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {scenarios.filter(s => selectedScenarios.includes(s.id)).map((scenario) => {
          const result = calculateScenario(scenario)
          return (
            <div key={scenario.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-gray-900">{scenario.name}</h3>
                <span className={`px-2.5 py-0.5 rounded-full text-xs font-medium ${getRiskColor(scenario.riskLevel)}`}>
                  {scenario.riskLevel} risk
                </span>
              </div>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Revenue:</span>
                  <span className="text-sm font-medium">${result.revenue.toFixed(2)}M</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Cost:</span>
                  <span className="text-sm font-medium">${result.cost.toFixed(2)}M</span>
                </div>
                <div className="flex justify-between border-t pt-2">
                  <span className="text-sm font-semibold text-gray-900">Profit:</span>
                  <span className="text-sm font-semibold text-green-600">${result.profit.toFixed(2)}M</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm text-gray-600">Margin:</span>
                  <span className="text-sm font-medium">{result.margin.toFixed(1)}%</span>
                </div>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default ScenarioAnalysis
