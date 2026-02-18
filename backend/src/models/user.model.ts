/**
 * User Model
 * 
 * Represents a user in the CRM system
 */

export interface User {
  id: string;
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'sales' | 'support';
  createdAt: Date;
  updatedAt: Date;
}

// Example: This would be a Mongoose schema, Sequelize model, or TypeORM entity
// depending on your chosen ORM
