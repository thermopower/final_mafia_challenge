/**
 * 포맷팅 유틸리티
 *
 * 날짜, 숫자, 퍼센트 포맷팅 함수를 제공합니다.
 */

export const formatters = {
  formatDate(dateStr: string): string {
    // "2024-11-01" → "2024년 11월 1일"
    const date = new Date(dateStr)
    return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일`
  },

  formatCurrency(amount: number): string {
    // 1000000 → "1,000,000원"
    return `${amount.toLocaleString('ko-KR')}원`
  },

  formatPercent(value: number): string {
    // 15.5 → "15.5%"
    return `${value.toFixed(1)}%`
  },

  formatCompactNumber(value: number): string {
    // 1200000 → "1.2M"
    if (value >= 1e9) return `${(value / 1e9).toFixed(1)}B`
    if (value >= 1e6) return `${(value / 1e6).toFixed(1)}M`
    if (value >= 1e3) return `${(value / 1e3).toFixed(1)}K`
    return value.toString()
  },
}
