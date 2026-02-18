/**
 * HTTP Status Codes
 * 
 * Standard HTTP status codes used across the application
 */

export const HTTP_STATUS = {
  // Success
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  
  // Client Errors
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  CONFLICT: 409,
  UNPROCESSABLE_ENTITY: 422,
  
  // Server Errors
  INTERNAL_SERVER_ERROR: 500,
  SERVICE_UNAVAILABLE: 503,
} as const;

export const STATUS_MESSAGES = {
  [HTTP_STATUS.OK]: 'Success',
  [HTTP_STATUS.CREATED]: 'Resource created successfully',
  [HTTP_STATUS.BAD_REQUEST]: 'Bad request',
  [HTTP_STATUS.UNAUTHORIZED]: 'Authentication required',
  [HTTP_STATUS.FORBIDDEN]: 'Access forbidden',
  [HTTP_STATUS.NOT_FOUND]: 'Resource not found',
  [HTTP_STATUS.CONFLICT]: 'Resource conflict',
  [HTTP_STATUS.INTERNAL_SERVER_ERROR]: 'Internal server error',
};
