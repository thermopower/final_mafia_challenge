/**
 * 인증 서비스
 *
 * Supabase Auth를 사용한 로그인/로그아웃 기능을 제공합니다.
 */
import { supabase } from './supabase'

export const authService = {
  async signIn(email: string, password: string): Promise<{ data: any; error: any }> {
    const { data, error } = await supabase.auth.signInWithPassword({ email, password })
    return { data, error }
  },

  async signUp(email: string, password: string, fullName?: string): Promise<{ data: any; error: any }> {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: {
          full_name: fullName || '',
          role: 'user',
        },
      },
    })
    return { data, error }
  },

  async signOut(): Promise<{ error: any }> {
    const { error } = await supabase.auth.signOut()
    return { error }
  },

  async getCurrentUser(): Promise<any> {
    const {
      data: { user },
    } = await supabase.auth.getUser()
    return user
  },

  async getAccessToken(): Promise<string | null> {
    const {
      data: { session },
    } = await supabase.auth.getSession()
    return session?.access_token || null
  },

  async refreshSession(): Promise<any> {
    const {
      data: { session },
      error,
    } = await supabase.auth.refreshSession()
    if (error) {
      console.error('세션 갱신 실패:', error)
      return null
    }
    return session
  },

  async updatePassword(newPassword: string): Promise<{ error: any }> {
    const { error } = await supabase.auth.updateUser({
      password: newPassword,
    })
    if (error) {
      throw new Error(error.message)
    }
    return { error }
  },
}
