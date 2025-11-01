/**
 * Supabase 클라이언트 초기화
 *
 * Supabase 클라이언트 싱글톤을 생성합니다.
 */
import { createClient, SupabaseClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  throw new Error('Missing Supabase environment variables')
}

export const supabase: SupabaseClient = createClient(supabaseUrl, supabaseAnonKey)
