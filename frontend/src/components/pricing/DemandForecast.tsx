import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

// Sample forecast data
const sampleData = [
  { month: 'Jan', actual: 120, forecast: 125, lower: 110, upper: 140 },
  { month: 'Feb', actual: 135, forecast: 140, lower: 125, upper: 155 },
  { month: 'Mar', actual: 145, forecast: 150, lower: 135, upper: 165 },
  { month: 'Apr', actual: 160, forecast: 165, lower: 150, upper: 180 },
  { month: 'May', actual: null, forecast: 175, lower: 160, upper: 190 },
  { month: 'Jun', actual: null, forecast: 180, lower: 165, upper: 195 },
]

const DemandForecast = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Demand Forecast</h1>
        <p className="mt-2 text-gray-600">
          AI-powered demand forecasting and market predictions
        </p>
      </div>

      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">6-Month Forecast</h2>
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={sampleData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line
              type="monotone"
              dataKey="actual"
              stroke="#3B82F6"
              strokeWidth={2}
              name="Actual"
              dot={{ fill: '#3B82F6' }}
            />
            <Line
              type="monotone"
              dataKey="forecast"
              stroke="#10B981"
              strokeWidth={2}
              strokeDasharray="5 5"
              name="Forecast"
              dot={{ fill: '#10B981' }}
            />
            <Line
              type="monotone"
              dataKey="upper"
              stroke="#D1D5DB"
              strokeWidth={1}
              name="Upper Bound"
              dot={false}
            />
            <Line
              type="monotone"
              dataKey="lower"
              stroke="#D1D5DB"
              strokeWidth={1}
              name="Lower Bound"
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Predicted Growth</h3>
          <p className="mt-2 text-3xl font-semibold text-green-600">+15.5%</p>
          <p className="mt-1 text-sm text-gray-500">Next 6 months</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Confidence Level</h3>
          <p className="mt-2 text-3xl font-semibold text-blue-600">85%</p>
          <p className="mt-1 text-sm text-gray-500">Model accuracy</p>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-sm font-medium text-gray-600">Peak Month</h3>
          <p className="mt-2 text-3xl font-semibold text-purple-600">June</p>
          <p className="mt-1 text-sm text-gray-500">Highest demand</p>
        </div>
      </div>
    </div>
  )
}

export default DemandForecast
