/**
 * User 도메인 모델
 */
export interface User {
  id: string
  email: string
  full_name: string
  department: string | null
  role: 'admin' | 'user'
  created_at: string
  updated_at: string
}
