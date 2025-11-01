import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface BudgetRatioChartProps {
  data: Array<{
    category: string
    value: string
    percentage: string
  }>
}

const COLORS = ['#1976d2', '#4caf50', '#ff9800', '#f44336', '#9c27b0']

export const BudgetRatioChart: React.FC<BudgetRatioChartProps> = ({ data }) => {
  // string을 number로 변환
  const chartData = data.map(item => ({
    name: item.category,
    value: parseFloat(item.value),
    percentage: parseFloat(item.percentage)
  }))

  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          예산 카테고리별 비율
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={(entry) => `${entry.name}: ${entry.percentage.toFixed(1)}%`}
              outerRadius={80}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip formatter={(value: number) => `${value.toLocaleString()}억원`} />
            <Legend />
          </PieChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
