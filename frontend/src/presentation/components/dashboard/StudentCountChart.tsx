import React from 'react'
import { Card, CardContent, Typography } from '@mui/material'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

interface StudentCountChartProps {
  data: Array<{
    department: string
    count: number
  }>
}

export const StudentCountChart: React.FC<StudentCountChartProps> = ({ data }) => {
  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          학과별 학생 수
        </Typography>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={data}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="department" />
            <YAxis />
            <Tooltip formatter={(value: number) => `${value}명`} />
            <Legend />
            <Bar dataKey="count" fill="#9c27b0" name="학생 수" />
          </BarChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  )
}
