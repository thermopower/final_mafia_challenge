import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface PerformanceTrendChartProps {
  data: Array<{
    month: string
    value: string
  }>
}

export const PerformanceTrendChart: React.FC<PerformanceTrendChartProps> = ({ data }) => {
  // string을 number로 변환
  const chartData = data.map(item => ({
    month: item.month,
    value: parseFloat(item.value)
  }))

  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          실적 월별 추세
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip formatter={(value: number) => `${value.toLocaleString()}억원`} />
            <Legend />
            <Line type="monotone" dataKey="value" stroke="#1976d2" strokeWidth={2} name="실적 금액" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
