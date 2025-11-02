/**
 * StudentPage - 학생 현황 대시보드
 *
 * 책임:
 * - 학생 수 통계
 * - 학적 상태 분포
 * - 학과별 학생 분포
 * - 지도교수별 학생 현황
 */
import React, { useState, useEffect } from 'react'
import {
  Box,
  Grid,
  Typography,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Card,
  CardContent
} from '@mui/material'
import { Loading } from '@/presentation/components/common/Loading'
import { ErrorMessage } from '@/presentation/components/common/ErrorMessage'
import apiClient from '@/services/api/client'

interface Student {
  id: number
  student_id: string
  name: string
  college: string
  department: string
  grade: number
  program_type: '학사' | '석사' | '박사'
  enrollment_status: '재학' | '휴학' | '졸업'
  gender: '남' | '여'
  admission_year: number
  advisor: string | null
  email: string
}

export const StudentPage: React.FC = () => {
  const [students, setStudents] = useState<Student[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [filterStatus, setFilterStatus] = useState<string>('all')
  const [filterProgram, setFilterProgram] = useState<string>('all')
  const [filterDepartment, setFilterDepartment] = useState<string>('all')

  const fetchData = async () => {
    setIsLoading(true)
    setError(null)

    try {
      const response = await apiClient.get('/data/', {
        params: {
          type: 'student_roster',
          page_size: 500
        }
      })
      // UnifiedDataItem 응답을 Student 인터페이스로 변환
      const transformedData = (response.data.results || []).map((item: any) => ({
        id: item.id,
        student_id: item.extra_fields?.student_id || '',
        name: item.title,
        college: item.extra_fields?.college || '',
        department: item.category || '',
        grade: item.extra_fields?.grade || 0,
        program_type: item.extra_fields?.program_type || '학사',
        enrollment_status: item.extra_fields?.enrollment_status || '재학',
        gender: item.extra_fields?.gender || '남',
        admission_year: item.extra_fields?.admission_year || 2020,
        advisor: item.extra_fields?.advisor || null,
        email: item.extra_fields?.email || '',
      }))
      setStudents(transformedData)
    } catch (err: any) {
      console.error('학생 데이터 조회 실패:', err)
      setError(err.response?.data?.error || '데이터를 불러오는 중 오류가 발생했습니다')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleStatusChange = (event: SelectChangeEvent<string>) => {
    setFilterStatus(event.target.value)
  }

  const handleProgramChange = (event: SelectChangeEvent<string>) => {
    setFilterProgram(event.target.value)
  }

  const handleDepartmentChange = (event: SelectChangeEvent<string>) => {
    setFilterDepartment(event.target.value)
  }

  if (isLoading) {
    return <Loading message="학생 현황 데이터를 불러오는 중..." />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />
  }

  // 필터링된 학생 목록
  const filteredStudents = students.filter(student => {
    if (filterStatus !== 'all' && student.enrollment_status !== filterStatus) return false
    if (filterProgram !== 'all' && student.program_type !== filterProgram) return false
    if (filterDepartment !== 'all' && student.department !== filterDepartment) return false
    return true
  })

  // 통계 계산
  const totalStudents = filteredStudents.length
  const byProgram = {
    학사: filteredStudents.filter(s => s.program_type === '학사').length,
    석사: filteredStudents.filter(s => s.program_type === '석사').length,
    박사: filteredStudents.filter(s => s.program_type === '박사').length,
  }
  const byStatus = {
    재학: filteredStudents.filter(s => s.enrollment_status === '재학').length,
    휴학: filteredStudents.filter(s => s.enrollment_status === '휴학').length,
    졸업: filteredStudents.filter(s => s.enrollment_status === '졸업').length,
  }
  const byGender = {
    남: filteredStudents.filter(s => s.gender === '남').length,
    여: filteredStudents.filter(s => s.gender === '여').length,
  }

  // 고유 학과 목록
  const departments = Array.from(new Set(students.map(s => s.department))).sort()

  return (
    <Box sx={{ p: 3 }}>
      {/* 헤더 */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          학생 현황 대시보드
        </Typography>
        <Typography variant="body1" color="text.secondary">
          학생 수 통계 및 학적 상태 분포를 확인하세요
        </Typography>
      </Box>

      {/* 필터 */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>학적 상태</InputLabel>
              <Select value={filterStatus} label="학적 상태" onChange={handleStatusChange}>
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="재학">재학</MenuItem>
                <MenuItem value="휴학">휴학</MenuItem>
                <MenuItem value="졸업">졸업</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>과정 구분</InputLabel>
              <Select value={filterProgram} label="과정 구분" onChange={handleProgramChange}>
                <MenuItem value="all">전체</MenuItem>
                <MenuItem value="학사">학사</MenuItem>
                <MenuItem value="석사">석사</MenuItem>
                <MenuItem value="박사">박사</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>학과</InputLabel>
              <Select value={filterDepartment} label="학과" onChange={handleDepartmentChange}>
                <MenuItem value="all">전체</MenuItem>
                {departments.map(dept => (
                  <MenuItem key={dept} value={dept}>{dept}</MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
      </Paper>

      {/* 통계 카드 */}
      <Grid container spacing={3} mb={3}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent sx={{ textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{totalStudents}</Typography>
              <Typography variant="body2" color="text.secondary">총 학생 수</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>과정별 분포</Typography>
              <Typography variant="body2">학사: {byProgram.학사}명</Typography>
              <Typography variant="body2">석사: {byProgram.석사}명</Typography>
              <Typography variant="body2">박사: {byProgram.박사}명</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>학적 상태</Typography>
              <Typography variant="body2">재학: {byStatus.재학}명</Typography>
              <Typography variant="body2">휴학: {byStatus.휴학}명</Typography>
              <Typography variant="body2">졸업: {byStatus.졸업}명</Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" gutterBottom>성별 분포</Typography>
              <Typography variant="body2">남: {byGender.남}명 ({totalStudents > 0 ? (byGender.남 / totalStudents * 100).toFixed(1) : 0}%)</Typography>
              <Typography variant="body2">여: {byGender.여}명 ({totalStudents > 0 ? (byGender.여 / totalStudents * 100).toFixed(1) : 0}%)</Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* 학생 목록 테이블 */}
      <Paper elevation={2}>
        <TableContainer sx={{ maxHeight: 600 }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell>학번</TableCell>
                <TableCell>이름</TableCell>
                <TableCell>학과</TableCell>
                <TableCell>학년</TableCell>
                <TableCell>과정</TableCell>
                <TableCell>학적 상태</TableCell>
                <TableCell>성별</TableCell>
                <TableCell>입학년도</TableCell>
                <TableCell>지도교수</TableCell>
                <TableCell>이메일</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredStudents.map((student) => (
                <TableRow key={student.id} hover>
                  <TableCell>{student.student_id}</TableCell>
                  <TableCell>{student.name}</TableCell>
                  <TableCell>{student.department}</TableCell>
                  <TableCell>{student.grade}학년</TableCell>
                  <TableCell>
                    <Chip label={student.program_type} size="small" color="primary" variant="outlined" />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={student.enrollment_status}
                      size="small"
                      color={
                        student.enrollment_status === '재학' ? 'success' :
                        student.enrollment_status === '휴학' ? 'warning' :
                        'default'
                      }
                    />
                  </TableCell>
                  <TableCell>{student.gender}</TableCell>
                  <TableCell>{student.admission_year}</TableCell>
                  <TableCell>{student.advisor || '-'}</TableCell>
                  <TableCell>{student.email}</TableCell>
                </TableRow>
              ))}
              {filteredStudents.length === 0 && (
                <TableRow>
                  <TableCell colSpan={10} align="center">
                    조건에 맞는 학생이 없습니다
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  )
}
