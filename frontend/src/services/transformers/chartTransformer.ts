/**
 * 차트 데이터 변환기
 *
 * Backend API 응답을 Recharts 형식으로 변환합니다.
 */

function formatDate(dateStr: string): string {
  const date = new Date(dateStr)
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
}

export const chartTransformer = {
  /**
   * 막대 차트 데이터 변환
   * Backend: { category: string, value: number }[]
   * Recharts: { name: string, value: number }[]
   */
  transformBarChartData(data: any[]): any[] {
    return data.map((item) => ({
      name: item.category || item.name,
      value: item.value || item.amount,
    }))
  },

  /**
   * 라인 차트 데이터 변환 (시계열)
   * Backend: { date: string, value: number }[]
   * Recharts: { date: string, value: number }[]
   */
  transformLineChartData(data: any[]): any[] {
    return data.map((item) => ({
      date: formatDate(item.date),
      value: item.value,
    }))
  },

  /**
   * 파이 차트 데이터 변환
   * Backend: { name: string, value: number }[]
   * Recharts: { name: string, value: number }[]
   */
  transformPieChartData(data: any[]): any[] {
    return data
  },
}
