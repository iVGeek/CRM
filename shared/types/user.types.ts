/**
 * User Types
 * 
 * Shared user type definitions
 */

export enum UserRole {
  ADMIN = 'admin',
  SALES = 'sales',
  SUPPORT = 'support',
}

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: UserRole;
  createdAt: Date;
  updatedAt: Date;
}

export interface CreateUserDto {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: UserRole;
}

export interface UpdateUserDto {
  email?: string;
  firstName?: string;
  lastName?: string;
  role?: UserRole;
}
