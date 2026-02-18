/**
 * Button Component
 * 
 * Reusable button component with variants
 */

// Example React component structure

interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  onClick?: () => void;
  disabled?: boolean;
  children: React.ReactNode;
}

// Implementation would go here
