// ErrorMessage.tsx
import React from 'react';

interface ErrorMessageProps {
  message: string;
}

const ErrorMessage: React.FC<ErrorMessageProps> = ({ message }) => {
  return message ? (
    <div className="api-error">
      <p className="api-error-text">{message}</p>
    </div>
  ) : null;
};

export default ErrorMessage;
