-- Migration: Create research_project_execution table
-- Description: Stores research project execution data from research_project_data.csv

CREATE TABLE IF NOT EXISTS research_project_execution (
    id BIGSERIAL PRIMARY KEY,
    execution_id VARCHAR(50) NOT NULL UNIQUE,
    project_number VARCHAR(100) NOT NULL,
    project_name VARCHAR(200) NOT NULL,
    principal_investigator VARCHAR(100) NOT NULL,
    department VARCHAR(100) NOT NULL,
    funding_agency VARCHAR(100) NOT NULL,
    total_budget BIGINT NOT NULL,
    execution_date DATE NOT NULL,
    execution_item VARCHAR(200) NOT NULL,
    execution_amount BIGINT NOT NULL,
    status VARCHAR(20) NOT NULL,
    remarks TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add check constraints
ALTER TABLE research_project_execution
ADD CONSTRAINT chk_total_budget_positive CHECK (total_budget > 0);

ALTER TABLE research_project_execution
ADD CONSTRAINT chk_execution_amount_positive CHECK (execution_amount > 0);

ALTER TABLE research_project_execution
ADD CONSTRAINT chk_status_value CHECK (status IN ('집행완료', '처리중'));

-- Create indexes
CREATE INDEX idx_research_project_number ON research_project_execution(project_number);
CREATE INDEX idx_research_execution_date ON research_project_execution(execution_date);
CREATE INDEX idx_research_status ON research_project_execution(status);
CREATE INDEX idx_research_pi ON research_project_execution(principal_investigator);
CREATE INDEX idx_research_funding_agency ON research_project_execution(funding_agency);
CREATE INDEX idx_research_department ON research_project_execution(department);

-- Create trigger for updated_at
CREATE TRIGGER update_research_project_execution_updated_at
BEFORE UPDATE ON research_project_execution
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- Comment
COMMENT ON TABLE research_project_execution IS 'Stores research project budget execution data including funding agencies, budgets, and execution items';
