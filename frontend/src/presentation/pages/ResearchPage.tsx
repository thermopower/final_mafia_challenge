/**
 * ResearchPage - 연구 성과 대시보드
 *
 * 책임:
 * - 논문 게재 현황 시각화
 * - 연구 과제 진행 현황
 * - 기술이전 수입 추이
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
  SelectChangeEvent
} from '@mui/material'
import { Loading } from '@/presentation/components/common/Loading'
import { ErrorMessage } from '@/presentation/components/common/ErrorMessage'
import apiClient from '@/services/api/client'

interface Publication {
  id: number
  paper_id: string
  publication_date: string
  college: string
  department: string
  paper_title: string
  lead_author: string
  co_authors: string | null
  journal_name: string
  journal_grade: 'SCIE' | 'KCI'
  impact_factor: number | null
  project_linked: 'Y' | 'N'
}

interface ResearchProject {
  id: number
  execution_id: string
  project_number: string
  project_name: string
  principal_investigator: string
  department: string
  funding_agency: string
  total_budget: number
  execution_date: string
  execution_item: string
  execution_amount: number
  status: '집행완료' | '처리중'
  remarks: string | null
}

export const ResearchPage: React.FC = () => {
  const [publications, setPublications] = useState<Publication[]>([])
  const [projects, setProjects] = useState<ResearchProject[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [dataType, setDataType] = useState<'publications' | 'projects'>('publications')
  const currentYear = new Date().getFullYear()
  const [year, setYear] = useState<number>(currentYear)

  const fetchData = async () => {
    setIsLoading(true)
    setError(null)

    try {
      if (dataType === 'publications') {
        const response = await apiClient.get('/data/', {
          params: {
            type: 'publication',
            year: year,
            page_size: 100
          }
        })
        // UnifiedDataItem 응답을 Publication 인터페이스로 변환
        const transformedData = (response.data.results || []).map((item: any) => ({
          id: item.id,
          paper_id: item.extra_fields?.paper_id || '',
          publication_date: item.date,
          college: item.extra_fields?.college || '',
          department: item.category || '',
          paper_title: item.title,
          lead_author: item.extra_fields?.lead_author || '',
          co_authors: item.extra_fields?.co_authors || null,
          journal_name: item.extra_fields?.journal_name || '',
          journal_grade: item.extra_fields?.journal_grade || 'KCI',
          impact_factor: item.extra_fields?.impact_factor || null,
          project_linked: item.extra_fields?.project_linked || 'N',
        }))
        setPublications(transformedData)
      } else {
        const response = await apiClient.get('/data/', {
          params: {
            type: 'research_project',
            year: year,
            page_size: 100
          }
        })
        // UnifiedDataItem 응답을 ResearchProject 인터페이스로 변환
        const transformedData = (response.data.results || []).map((item: any) => ({
          id: item.id,
          execution_id: item.extra_fields?.execution_id || '',
          project_number: item.extra_fields?.project_number || '',
          project_name: item.title,
          principal_investigator: item.extra_fields?.principal_investigator || '',
          department: item.category || '',
          funding_agency: item.extra_fields?.funding_agency || '',
          total_budget: item.extra_fields?.total_budget || 0,
          execution_date: item.date,
          execution_item: item.extra_fields?.execution_item || '',
          execution_amount: item.extra_fields?.execution_amount || 0,
          status: item.extra_fields?.status || '처리중',
          remarks: item.description || null,
        }))
        setProjects(transformedData)
      }
    } catch (err: any) {
      console.error('데이터 조회 실패:', err)
      setError(err.response?.data?.error || '데이터를 불러오는 중 오류가 발생했습니다')
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [dataType, year])

  const handleDataTypeChange = (event: SelectChangeEvent<string>) => {
    setDataType(event.target.value as 'publications' | 'projects')
  }

  const handleYearChange = (event: SelectChangeEvent<number>) => {
    setYear(Number(event.target.value))
  }

  const years = Array.from({ length: 6 }, (_, i) => currentYear - i)

  if (isLoading) {
    return <Loading message="연구 성과 데이터를 불러오는 중..." />
  }

  if (error) {
    return <ErrorMessage message={error} onRetry={fetchData} />
  }

  // 통계 계산
  const totalPublications = publications.length
  const scieCount = publications.filter(p => p.journal_grade === 'SCIE').length
  const kciCount = publications.filter(p => p.journal_grade === 'KCI').length
  const avgImpactFactor = publications
    .filter(p => p.impact_factor !== null)
    .reduce((sum, p) => sum + (p.impact_factor || 0), 0) / (scieCount || 1)
  const projectLinkedCount = publications.filter(p => p.project_linked === 'Y').length
  const projectLinkedRatio = totalPublications > 0 ? (projectLinkedCount / totalPublications * 100) : 0

  const totalBudget = projects.reduce((sum, p) => sum + p.total_budget, 0)
  const totalExecution = projects
    .filter(p => p.status === '집행완료')
    .reduce((sum, p) => sum + p.execution_amount, 0)
  const executionRate = totalBudget > 0 ? (totalExecution / totalBudget * 100) : 0

  return (
    <Box sx={{ p: 3 }}>
      {/* 헤더 */}
      <Box mb={4}>
        <Typography variant="h4" gutterBottom>
          연구 성과 대시보드
        </Typography>
        <Typography variant="body1" color="text.secondary">
          논문 게재 현황 및 연구 과제 진행 현황을 확인하세요
        </Typography>
      </Box>

      {/* 필터 */}
      <Paper elevation={1} sx={{ p: 2, mb: 3 }}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth size="small">
              <InputLabel>데이터 유형</InputLabel>
              <Select value={dataType} label="데이터 유형" onChange={handleDataTypeChange}>
                <MenuItem value="publications">논문 목록</MenuItem>
                <MenuItem value="projects">연구 과제</MenuItem>
              </Select>
            </FormControl>
          </Grid>
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
        </Grid>
      </Paper>

      {/* 통계 카드 */}
      {dataType === 'publications' && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{totalPublications}</Typography>
              <Typography variant="body2" color="text.secondary">총 논문 수</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{scieCount}</Typography>
              <Typography variant="body2" color="text.secondary">SCIE 논문</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{avgImpactFactor.toFixed(2)}</Typography>
              <Typography variant="body2" color="text.secondary">평균 IF</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{projectLinkedRatio.toFixed(1)}%</Typography>
              <Typography variant="body2" color="text.secondary">과제 연계율</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {dataType === 'projects' && (
        <Grid container spacing={3} mb={3}>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{projects.length}</Typography>
              <Typography variant="body2" color="text.secondary">총 연구 과제</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{(totalBudget / 100000000).toFixed(1)}억</Typography>
              <Typography variant="body2" color="text.secondary">총 연구비</Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} sm={6} md={4}>
            <Paper sx={{ p: 2, textAlign: 'center' }}>
              <Typography variant="h4" color="primary">{executionRate.toFixed(1)}%</Typography>
              <Typography variant="body2" color="text.secondary">집행률</Typography>
            </Paper>
          </Grid>
        </Grid>
      )}

      {/* 데이터 테이블 */}
      <Paper elevation={2}>
        <TableContainer sx={{ maxHeight: 600 }}>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                {dataType === 'publications' ? (
                  <>
                    <TableCell>논문ID</TableCell>
                    <TableCell>게재일</TableCell>
                    <TableCell>학과</TableCell>
                    <TableCell>논문제목</TableCell>
                    <TableCell>주저자</TableCell>
                    <TableCell>학술지명</TableCell>
                    <TableCell>등급</TableCell>
                    <TableCell>IF</TableCell>
                    <TableCell>과제연계</TableCell>
                  </>
                ) : (
                  <>
                    <TableCell>집행ID</TableCell>
                    <TableCell>과제번호</TableCell>
                    <TableCell>과제명</TableCell>
                    <TableCell>연구책임자</TableCell>
                    <TableCell>소속학과</TableCell>
                    <TableCell>지원기관</TableCell>
                    <TableCell>총 연구비</TableCell>
                    <TableCell>집행금액</TableCell>
                    <TableCell>상태</TableCell>
                  </>
                )}
              </TableRow>
            </TableHead>
            <TableBody>
              {dataType === 'publications' ? (
                publications.map((pub) => (
                  <TableRow key={pub.id} hover>
                    <TableCell>{pub.paper_id}</TableCell>
                    <TableCell>{pub.publication_date}</TableCell>
                    <TableCell>{pub.department}</TableCell>
                    <TableCell sx={{ maxWidth: 300 }}>{pub.paper_title}</TableCell>
                    <TableCell>{pub.lead_author}</TableCell>
                    <TableCell>{pub.journal_name}</TableCell>
                    <TableCell>
                      <Chip
                        label={pub.journal_grade}
                        color={pub.journal_grade === 'SCIE' ? 'primary' : 'default'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{pub.impact_factor?.toFixed(2) || '-'}</TableCell>
                    <TableCell>
                      <Chip
                        label={pub.project_linked === 'Y' ? '연계' : '미연계'}
                        color={pub.project_linked === 'Y' ? 'success' : 'default'}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              ) : (
                projects.map((proj) => (
                  <TableRow key={proj.id} hover>
                    <TableCell>{proj.execution_id}</TableCell>
                    <TableCell>{proj.project_number}</TableCell>
                    <TableCell sx={{ maxWidth: 250 }}>{proj.project_name}</TableCell>
                    <TableCell>{proj.principal_investigator}</TableCell>
                    <TableCell>{proj.department}</TableCell>
                    <TableCell>{proj.funding_agency}</TableCell>
                    <TableCell>{(proj.total_budget / 100000000).toFixed(2)}억</TableCell>
                    <TableCell>{(proj.execution_amount / 100000000).toFixed(2)}억</TableCell>
                    <TableCell>
                      <Chip
                        label={proj.status}
                        color={proj.status === '집행완료' ? 'success' : 'warning'}
                        size="small"
                      />
                    </TableCell>
                  </TableRow>
                ))
              )}
              {(dataType === 'publications' && publications.length === 0) && (
                <TableRow>
                  <TableCell colSpan={9} align="center">
                    데이터가 없습니다
                  </TableCell>
                </TableRow>
              )}
              {(dataType === 'projects' && projects.length === 0) && (
                <TableRow>
                  <TableCell colSpan={9} align="center">
                    데이터가 없습니다
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
