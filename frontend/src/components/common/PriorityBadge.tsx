'use client'

import { getPriorityColor, getPriorityLabel, getPriorityIcon } from '@/lib/utils/priority'

interface PriorityBadgeProps {
  priority?: string
  size?: 'sm' | 'md' | 'lg'
  showIcon?: boolean
  showText?: boolean
}

export function PriorityBadge({
  priority,
  size = 'md',
  showIcon = true,
  showText = true,
}: PriorityBadgeProps) {
  const color = getPriorityColor(priority)
  const label = getPriorityLabel(priority)
  const icon = getPriorityIcon(priority)

  const sizeClasses = {
    sm: 'px-2 py-1 text-xs',
    md: 'px-3 py-1 text-sm',
    lg: 'px-4 py-2 text-base',
  }

  return (
    <div
      className={`inline-flex items-center gap-1.5 rounded font-medium text-white ${sizeClasses[size]}`}
      style={{ backgroundColor: color }}
      title={label}
      role="badge"
      aria-label={`Priority: ${label}`}
    >
      {showIcon && <span>{icon}</span>}
      {showText && <span>{label}</span>}
    </div>
  )
}
