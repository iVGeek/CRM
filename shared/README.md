# Shared

This directory contains code shared between the frontend and backend.

## Purpose

By sharing code between frontend and backend, we:
- Reduce code duplication
- Ensure consistency in data types and validation
- Maintain a single source of truth for business logic
- Simplify maintenance and updates

## Structure

### `/types`
Shared TypeScript type definitions and interfaces:
- User types
- Contact types
- Ticket types
- API request/response types
- Enum definitions

### `/constants`
Shared constants and enums:
- User roles and permissions
- Status codes
- Error messages
- Configuration values

### `/utils`
Shared utility functions:
- Validation functions
- Data formatters
- Date/time utilities
- Common business logic

## Usage

### In Backend
```typescript
import { UserRole } from '../../../shared/types/user';
import { validateEmail } from '../../../shared/utils/validation';
```

### In Frontend
```typescript
import { UserRole } from '../../../shared/types/user';
import { validateEmail } from '../../../shared/utils/validation';
```

## Guidelines

- Only include code that is truly needed by both frontend and backend
- Keep shared code framework-agnostic (no React or Express-specific code)
- Write comprehensive tests for shared utilities
- Document all exported functions and types
