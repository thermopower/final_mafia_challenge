/**
 * Dashboard 도메인 모델
 */

export interface PerformanceSummary {
  total_amount: number
  growth_rate: number
  category_breakdown: CategoryBreakdown[]
}

export interface CategoryBreakdown {
  category: string
  amount: number
}

export interface PaperSummary {
  total_count: number
  scie_count: number
  field_breakdown: FieldBreakdown[]
}

export interface FieldBreakdown {
  field: string
  count: number
}

export interface StudentSummary {
  total_count: number
  active_count: number
  department_breakdown: DepartmentBreakdown[]
}

export interface DepartmentBreakdown {
  department: string
  count: number
}

export interface BudgetSummary {
  total_amount: number
  category_breakdown: CategoryBreakdown[]
}

export interface DashboardSummary {
  performance: PerformanceSummary
  papers: PaperSummary
  students: StudentSummary
  budget: BudgetSummary
}
