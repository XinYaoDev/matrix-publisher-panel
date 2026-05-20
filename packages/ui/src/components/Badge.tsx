import React from 'react'

interface BadgeProps {
  label: string
  variant?: 'default' | 'ok' | 'warn'
}

const colors: Record<string, React.CSSProperties> = {
  default: { background: '#eef2f7', color: '#334155' },
  ok: { background: '#dcfce7', color: '#166534' },
  warn: { background: '#fef3c7', color: '#b45309' }
}

export const Badge: React.FC<BadgeProps> = ({ label, variant = 'default' }) => {
  const style: React.CSSProperties = {
    display: 'inline-flex',
    alignItems: 'center',
    height: 24,
    borderRadius: 999,
    padding: '0 8px',
    fontSize: 12,
    ...colors[variant]
  }

  return <span style={style}>{label}</span>
}
