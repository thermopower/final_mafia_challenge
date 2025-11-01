import React from 'react'
import { Card, CardContent, Typography, Box } from '@mui/material'
import TrendingUpIcon from '@mui/icons-material/TrendingUp'
import TrendingDownIcon from '@mui/icons-material/TrendingDown'
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat'

interface KPICardProps {
  title: string
  value: string
  unit: string
  changeRate: string
  trend: 'up' | 'down' | 'neutral'
}

export const KPICard: React.FC<KPICardProps> = ({
  title,
  value,
  unit,
  changeRate,
  trend
}) => {
  const getTrendIcon = () => {
    switch (trend) {
      case 'up':
        return <TrendingUpIcon sx={{ color: '#4caf50', fontSize: 32 }} />
      case 'down':
        return <TrendingDownIcon sx={{ color: '#f44336', fontSize: 32 }} />
      case 'neutral':
        return <TrendingFlatIcon sx={{ color: '#9e9e9e', fontSize: 32 }} />
    }
  }

  const getTrendColor = () => {
    switch (trend) {
      case 'up':
        return '#4caf50'
      case 'down':
        return '#f44336'
      case 'neutral':
        return '#9e9e9e'
    }
  }

  return (
    <Card elevation={3} sx={{ height: '100%' }}>
      <CardContent>
        <Typography variant="subtitle2" color="text.secondary" gutterBottom>
          {title}
        </Typography>

        <Box display="flex" alignItems="center" justifyContent="space-between" mt={2}>
          <Box>
            <Typography variant="h4" component="div" fontWeight="bold">
              {value}
              <Typography variant="h6" component="span" color="text.secondary" ml={1}>
                {unit}
              </Typography>
            </Typography>
            <Typography
              variant="body2"
              sx={{ color: getTrendColor(), mt: 1 }}
            >
              전년 대비 {changeRate}%
            </Typography>
          </Box>

          <Box>
            {getTrendIcon()}
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}
