/**
 * Priority utility functions
 * Provides color, icon, and label mappings for task priorities
 */

export type PriorityLevel = 'low' | 'medium' | 'high'

export function getPriorityColor(priority?: string): string {
  switch (priority?.toLowerCase()) {
    case 'high':
      return '#ff6b6b' // Red
    case 'medium':
      return '#c68dff' // Violet
    case 'low':
      return '#3d444f' // Slate
    default:
      return '#c68dff' // Default to medium (violet)
  }
}

export function getPriorityLabel(priority?: string): string {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 'High'
    case 'medium':
      return 'Medium'
    case 'low':
      return 'Low'
    default:
      return 'Medium'
  }
}

export function getPriorityIcon(priority?: string): string {
  switch (priority?.toLowerCase()) {
    case 'high':
      return '!'
    case 'medium':
      return '–'
    case 'low':
      return '↓'
    default:
      return '–'
  }
}

export function getPriorityOrder(priority?: string): number {
  switch (priority?.toLowerCase()) {
    case 'high':
      return 3
    case 'medium':
      return 2
    case 'low':
      return 1
    default:
      return 2
  }
}

export const PRIORITY_OPTIONS: Array<{ value: string; label: string }> = [
  { value: 'low', label: 'Low' },
  { value: 'medium', label: 'Medium' },
  { value: 'high', label: 'High' },
]
