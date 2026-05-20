import React from 'react'

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger'
}

export const Button: React.FC<ButtonProps> = ({ variant = 'primary', children, ...props }) => {
  const baseStyle: React.CSSProperties = {
    padding: '8px 16px',
    border: '1px solid #d1d5db',
    borderRadius: 6,
    cursor: 'pointer',
    fontSize: 14,
    fontFamily: 'inherit',
    background: variant === 'primary' ? '#0f766e' : variant === 'danger' ? '#fff' : '#2563eb',
    color: variant === 'danger' ? '#b91c1c' : '#fff',
    borderColor: variant === 'danger' ? '#fecaca' : 'transparent'
  }

  return <button style={baseStyle} {...props}>{children}</button>
}
