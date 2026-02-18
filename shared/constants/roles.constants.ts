/**
 * User Roles and Permissions
 * 
 * Constants for user roles and their permissions
 */

export const USER_ROLES = {
  ADMIN: 'admin',
  SALES: 'sales',
  SUPPORT: 'support',
} as const;

export const PERMISSIONS = {
  // Contact permissions
  CONTACTS_VIEW: 'contacts:view',
  CONTACTS_CREATE: 'contacts:create',
  CONTACTS_EDIT: 'contacts:edit',
  CONTACTS_DELETE: 'contacts:delete',
  
  // Sales permissions
  SALES_VIEW: 'sales:view',
  SALES_CREATE: 'sales:create',
  SALES_EDIT: 'sales:edit',
  SALES_DELETE: 'sales:delete',
  
  // Support permissions
  TICKETS_VIEW: 'tickets:view',
  TICKETS_CREATE: 'tickets:create',
  TICKETS_EDIT: 'tickets:edit',
  TICKETS_DELETE: 'tickets:delete',
  
  // Marketing permissions
  MARKETING_VIEW: 'marketing:view',
  MARKETING_CREATE: 'marketing:create',
  MARKETING_EDIT: 'marketing:edit',
  MARKETING_SEND: 'marketing:send',
  
  // Admin permissions
  USERS_MANAGE: 'users:manage',
  SETTINGS_MANAGE: 'settings:manage',
  ANALYTICS_VIEW: 'analytics:view',
} as const;

export const ROLE_PERMISSIONS = {
  [USER_ROLES.ADMIN]: Object.values(PERMISSIONS),
  [USER_ROLES.SALES]: [
    PERMISSIONS.CONTACTS_VIEW,
    PERMISSIONS.CONTACTS_CREATE,
    PERMISSIONS.CONTACTS_EDIT,
    PERMISSIONS.SALES_VIEW,
    PERMISSIONS.SALES_CREATE,
    PERMISSIONS.SALES_EDIT,
  ],
  [USER_ROLES.SUPPORT]: [
    PERMISSIONS.CONTACTS_VIEW,
    PERMISSIONS.TICKETS_VIEW,
    PERMISSIONS.TICKETS_CREATE,
    PERMISSIONS.TICKETS_EDIT,
  ],
};
