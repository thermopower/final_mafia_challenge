import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface PaperDistributionChartProps {
  data: Array<{
    category: string
    count: number
  }>
}

export const PaperDistributionChart: React.FC<PaperDistributionChartProps> = ({ data }) => {
  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          논문 카테고리별 분포
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="category" />
            <YAxis />
            <Tooltip formatter={(value: number) => `${value}편`} />
            <Legend />
            <Bar dataKey="count" fill="#4caf50" name="논문 수" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
