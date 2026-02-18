/**
 * Kanban Board Component
 * 
 * Sales pipeline visualization
 */

// Example component for sales pipeline Kanban board

interface KanbanBoardProps {
  stages: Stage[];
  deals: Deal[];
  onDealMove: (dealId: string, newStage: string) => void;
}

// Features:
// - Drag and drop deals between stages
// - Visual pipeline representation
// - Deal cards with key information
// - Stage totals and metrics
