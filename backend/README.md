# Backend

This directory contains the backend API server for the CRM system.

## Structure

### `/src`
- **config/**: Configuration files for database, environment variables, and app settings
- **controllers/**: HTTP request handlers that process requests and return responses
- **models/**: Database schemas and models (for MongoDB, PostgreSQL, etc.)
- **routes/**: API endpoint definitions and routing logic
- **services/**: Business logic layer that handles data processing and external API calls
- **middleware/**: Custom middleware for authentication, authorization, validation, and error handling
- **utils/**: Utility functions, formatters, validators, and helper functions
- **types/**: TypeScript type definitions and interfaces

### `/tests`
- **unit/**: Unit tests for individual functions and modules
- **integration/**: Integration tests for API endpoints and database operations
- **fixtures/**: Test data and mock objects

### `/scripts`
- Build scripts, database migration scripts, and deployment utilities

## Getting Started

1. Install dependencies:
   ```bash
   npm install
   ```

2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Run tests:
   ```bash
   npm test
   ```

## Tech Stack

- **Runtime**: Node.js
- **Framework**: Express.js / Fastify / NestJS (to be decided)
- **Database**: PostgreSQL / MongoDB (to be decided)
- **ORM**: TypeORM / Prisma / Mongoose (to be decided)
- **Authentication**: JWT / OAuth2
- **Testing**: Jest / Mocha + Chai

## API Endpoints

API documentation will be available at `/api/docs` when the server is running.
