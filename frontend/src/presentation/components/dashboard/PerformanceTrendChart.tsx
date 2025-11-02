import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface PerformanceTrendChartProps {
  data: Array<{
    year: number
    full_time: number
    visiting: number
  }>
}

export const PerformanceTrendChart: React.FC<PerformanceTrendChartProps> = ({ data }) => {
  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          연도별 교원 수 추이
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="full_time" stroke="#1976d2" strokeWidth={2} name="전임교원" />
            <Line type="monotone" dataKey="visiting" stroke="#4caf50" strokeWidth={2} name="초빙교원" />
          </LineChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
