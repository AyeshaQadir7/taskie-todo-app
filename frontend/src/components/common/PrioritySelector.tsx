'use client'

import { PRIORITY_OPTIONS } from '@/lib/utils/priority'

interface PrioritySelectorProps {
  value?: string
  onChange: (value: string) => void
  label?: string
  required?: boolean
  disabled?: boolean
}

export function PrioritySelector({
  value = 'medium',
  onChange,
  label = 'Priority',
  required = false,
  disabled = false,
}: PrioritySelectorProps) {
  return (
    <div className="flex flex-col gap-2">
      <label htmlFor="priority-select" className="text-sm font-medium text-gray-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <select
        id="priority-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        className="px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
      >
        {PRIORITY_OPTIONS.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  )
}
