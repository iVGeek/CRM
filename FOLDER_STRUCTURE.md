# Full-Stack CRM Folder Structure

## Proposed Tree Structure

```
CRM/
├── backend/
│   ├── src/
│   │   ├── config/          # Configuration files (database, environment, etc.)
│   │   ├── controllers/     # Request handlers
│   │   ├── models/          # Database models/schemas
│   │   ├── routes/          # API route definitions
│   │   ├── services/        # Business logic layer
│   │   ├── middleware/      # Custom middleware (auth, validation, etc.)
│   │   ├── utils/           # Utility functions and helpers
│   │   └── types/           # TypeScript types/interfaces
│   ├── tests/               # Backend tests
│   │   ├── unit/            # Unit tests
│   │   ├── integration/     # Integration tests
│   │   └── fixtures/        # Test data
│   └── scripts/             # Build and deployment scripts
│
├── frontend/
│   ├── public/              # Static assets
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   │   ├── common/      # Common/shared components
│   │   │   ├── contacts/    # Contact management components
│   │   │   ├── sales/       # Sales pipeline components
│   │   │   ├── marketing/   # Marketing components
│   │   │   ├── support/     # Support ticketing components
│   │   │   └── analytics/   # Analytics dashboard components
│   │   ├── pages/           # Page-level components
│   │   ├── services/        # API client services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── context/         # React context providers
│   │   ├── utils/           # Utility functions
│   │   ├── config/          # Frontend configuration
│   │   ├── types/           # TypeScript types
│   │   ├── styles/          # Global styles
│   │   └── assets/          # Images, fonts, etc.
│   └── tests/               # Frontend tests
│       ├── unit/            # Unit tests
│       ├── integration/     # Integration tests
│       └── e2e/             # End-to-end tests
│
├── shared/                  # Shared code between frontend and backend
│   ├── types/               # Shared TypeScript types
│   ├── constants/           # Shared constants
│   └── utils/               # Shared utilities
│
└── docs/                    # Project documentation
    ├── api/                 # API documentation
    ├── architecture/        # Architecture diagrams and docs
    └── deployment/          # Deployment guides
```

## Folder Descriptions

### Backend Structure

- **config/**: Environment variables, database configuration, app settings
- **controllers/**: Handle HTTP requests, call services, return responses
- **models/**: Database schemas and models (Mongoose, Sequelize, TypeORM, etc.)
- **routes/**: Define API endpoints and map them to controllers
- **services/**: Business logic, data processing, external API calls
- **middleware/**: Authentication, authorization, validation, error handling
- **utils/**: Helper functions, formatters, validators
- **types/**: TypeScript interfaces and types
- **tests/**: Test suites for backend code

### Frontend Structure

- **components/**: Reusable UI components organized by feature
- **pages/**: Top-level page components
- **services/**: API client functions for backend communication
- **hooks/**: Custom React hooks for shared logic
- **context/**: Global state management using Context API
- **utils/**: Helper functions, formatters, validators
- **config/**: Frontend configuration (API URLs, feature flags)
- **types/**: TypeScript interfaces and types
- **styles/**: Global CSS, theme configuration
- **tests/**: Test suites for frontend code

### Shared Structure

- **shared/**: Code that can be used by both frontend and backend
  - Reduces duplication
  - Ensures consistency in types and constants
  - Useful for validation schemas, DTOs, enums

### Documentation

- **docs/**: Comprehensive project documentation
  - API specifications
  - Architecture decisions
  - Deployment procedures
