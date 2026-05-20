import React from 'react'

interface CardProps {
  title?: string
  children: React.ReactNode
}

export const Card: React.FC<CardProps> = ({ title, children }) => {
  const style: React.CSSProperties = {
    background: '#fff',
    border: '1px solid #e5e7eb',
    borderRadius: 8,
    padding: 16
  }

  return (
    <div style={style}>
      {title && <h2 style={{ margin: '0 0 12px', fontSize: 16 }}>{title}</h2>}
      {children}
    </div>
  )
}
