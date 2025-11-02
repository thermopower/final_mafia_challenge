import React, { useState } from 'react'
import {
  Box,
  Grid,
  Typography,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Paper
} from '@mui/material'
import { useDashboard } from '@/application/hooks/useDashboard'
import { Loading } from '@/presentation/components/common/Loading'
import { ErrorMessage } from '@/presentation/components/common/ErrorMessage'
import { KPICard } from '@/presentation/components/dashboard/KPICard'
import { PerformanceTrendChart } from '@/presentation/components/dashboard/PerformanceTrendChart'
import { PaperDistributionChart } from '@/presentation/components/dashboard/PaperDistributionChart'
import { BudgetRatioChart } from '@/presentation/components/dashboard/BudgetRatioChart'
import { StudentCountChart } from '@/presentation/components/dashboard/StudentCountChart'

export const DashboardPage: React.FC = () => {
  const currentYear = new Date().getFullYear()
  const [year, setYear] = useState<number>(currentYear)
  const [department, setDepartment] = useState<string>('all')

  const { data, isLoading, error, refetch } = useDashboard({ year, department })

  const handleYearChange = (event: SelectChangeEvent<number>) => {
    setYear(Number(event.target.value))
  }

  const handleDepartmentChange = (event: SelectChangeEvent<string>) => {
    setDepartment(event.target.value)
  }

  if (isLoading) {
    return <Loading message="대시보드 데이터를 불러오는 중..." />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={refetch} />
  }

  if (!data) {
    return <ErrorMessage message="데이터를 불러올 수 없습니다" onRetry={refetch} />
  }

  console.log('[DashboardPage] 받은 데이터:', data)

  // 연도 목록 생성 (현재 연도부터 5년 전까지)
  const years = Array.from({ length: 6 }, (_, i) => currentYear - i)

  // Helper: change_rate에 따라 trend 계산
  const getTrend = (changeRate: number): 'up' | 'down' | 'neutral' => {
    if (changeRate > 1) return 'up'
    if (changeRate < -1) return 'down'
    return 'neutral'
  }

  return (
    <Box sx={{ p: 3 }}>
      {/* 헤더 */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          대시보드
        </Typography>
        <Typography variant="body1" color="text.secondary">
          대학교 실적, 논문, 학생, 예산 현황을 한눈에 확인하세요
        </Typography>
      </Box>

      {/* 필터 */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>연도</InputLabel>
              <Select value={year} label="연도" onChange={handleYearChange}>
                {years.map((y) => (
                  <MenuItem key={y} value={y}>
                    {y}년
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>부서</InputLabel>
              <Select value={department} label="부서" onChange={handleDepartmentChange}>
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="컴퓨터공학과">컴퓨터공학과</MenuItem>
                <MenuItem value="전자공학과">전자공학과</MenuItem>
                <MenuItem value="기계공학과">기계공학과</MenuItem>
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* KPI 카드 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="전임교원 수"
            value={data.kpi_metrics?.full_time_faculty?.value || 0}
            unit="명"
            changeRate={data.kpi_metrics?.full_time_faculty?.change_rate || 0}
            trend={getTrend(data.kpi_metrics?.full_time_faculty?.change_rate || 0)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="논문 수"
            value={data.kpi_metrics?.total_papers?.value || 0}
            unit="편"
            changeRate={data.kpi_metrics?.total_papers?.change_rate || 0}
            trend={getTrend(data.kpi_metrics?.total_papers?.change_rate || 0)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="학생 수"
            value={data.kpi_metrics?.total_students?.value || 0}
            unit="명"
            changeRate={data.kpi_metrics?.total_students?.change_rate || 0}
            trend={getTrend(data.kpi_metrics?.total_students?.change_rate || 0)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <KPICard
            title="예산 집행률"
            value={data.kpi_metrics?.budget_execution_rate?.value || 0}
            unit="%"
            changeRate={data.kpi_metrics?.budget_execution_rate?.change_rate || 0}
            trend={getTrend(data.kpi_metrics?.budget_execution_rate?.change_rate || 0)}
          />
        </Grid>
      </Grid>

      {/* 차트 */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={6}>
          <PerformanceTrendChart data={data.charts?.faculty_trend || []} />
        </Grid>
        <Grid item xs={12} lg={6}>
          <PaperDistributionChart data={data.charts?.paper_distribution || []} />
        </Grid>
        <Grid item xs={12} lg={6}>
          <BudgetRatioChart data={data.charts?.budget_by_item || []} />
        </Grid>
        <Grid item xs={12} lg={6}>
          <StudentCountChart data={data.charts?.students_by_program || []} />
        </Grid>
      </Grid>
    </Box>
  )
}
