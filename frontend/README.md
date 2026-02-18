# Frontend

This directory contains the frontend web application for the CRM system.

## Structure

### `/public`
- Static assets that are served directly (favicon, manifest, etc.)

### `/src`
- **components/**: Reusable UI components organized by feature
  - **common/**: Shared components (buttons, inputs, modals, etc.)
  - **contacts/**: Contact management components
  - **sales/**: Sales pipeline and Kanban board components
  - **marketing/**: Marketing and email campaign components
  - **support/**: Support ticketing system components
  - **analytics/**: Dashboard and analytics components
- **pages/**: Top-level page components (Dashboard, Contacts, Sales, etc.)
- **services/**: API client functions for communicating with the backend
- **hooks/**: Custom React hooks for reusable logic
- **context/**: React Context providers for global state management
- **utils/**: Utility functions, formatters, and validators
- **config/**: Frontend configuration (API URLs, feature flags, constants)
- **types/**: TypeScript type definitions and interfaces
- **styles/**: Global CSS, theme configuration, and style utilities
- **assets/**: Images, fonts, icons, and other static resources

### `/tests`
- **unit/**: Unit tests for components and functions
- **integration/**: Integration tests for user flows
- **e2e/**: End-to-end tests using Cypress or Playwright

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

5. Build for production:
   ```bash
   npm run build
   ```

## Tech Stack

- **Framework**: React / Next.js / Vue.js (to be decided)
- **Language**: TypeScript
- **State Management**: Redux / Zustand / Context API (to be decided)
- **Styling**: Tailwind CSS / Material-UI / Styled Components (to be decided)
- **Testing**: Jest + React Testing Library
- **E2E Testing**: Cypress / Playwright

## Features

- Contact Management
- Sales Pipeline (Kanban View)
- Marketing Email Campaigns
- Support Ticket System
- Role-Based Access Control (Admin, Sales, Support)
- Analytics Dashboard
- Real-time Notifications
