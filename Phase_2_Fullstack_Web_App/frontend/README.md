# Phase 2 Frontend - Next.js Todo App

A modern, responsive Todo application built with Next.js, React 19, and Tailwind CSS.

## Tech Stack

- **Framework**: Next.js 15+ (App Router)
- **UI Library**: React 19
- **Language**: TypeScript 5
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth
- **HTTP Client**: Fetch API

## Project Structure

```
frontend/
├── src/
│   ├── app/                    # Next.js App Router pages
│   │   ├── layout.tsx          # Root layout
│   │   ├── page.tsx            # Home page (redirects to dashboard)
│   │   ├── login/              # Login page
│   │   ├── register/           # Registration page
│   │   └── dashboard/          # Main todo app (protected)
│   ├── components/             # React components
│   │   ├── auth/               # Authentication forms
│   │   │   ├── LoginForm.tsx
│   │   │   └── RegisterForm.tsx
│   │   ├── tasks/              # Task management
│   │   │   ├── TaskList.tsx    # Task list with sections
│   │   │   ├── TaskItem.tsx    # Individual task card
│   │   │   ├── TaskForm.tsx    # Add new task form
│   │   │   └── TaskEditModal.tsx # Edit task modal
│   │   └── ui/                 # Reusable UI components
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       └── Input.tsx
│   ├── lib/                    # Utilities and clients
│   │   ├── api.ts              # Backend API client
│   │   ├── auth.ts             # Better Auth configuration
│   │   ├── auth-client.ts      # Auth client instance
│   │   └── errors.ts           # Error message utilities
│   └── types/                  # TypeScript definitions
│       └── task.ts             # Task types
├── public/                     # Static assets
├── .env.local.example          # Environment template
├── tailwind.config.ts          # Tailwind configuration
├── tsconfig.json               # TypeScript configuration
└── package.json                # Dependencies
```

## Quick Start

### Prerequisites

- Node.js 18+ (LTS recommended)
- npm or yarn
- Backend server running (see [Backend README](../backend/README.md))

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment

```bash
# Copy the example environment file
cp .env.local.example .env.local

# Edit .env.local with your values
```

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000` |
| `BETTER_AUTH_SECRET` | JWT secret (must match backend) | `your-32-char-secret-key` |
| `BETTER_AUTH_URL` | Frontend URL for auth | `http://localhost:3000` |
| `NEXT_PUBLIC_BETTER_AUTH_URL` | Public auth URL | `http://localhost:3000` |

**Important**: `BETTER_AUTH_SECRET` must be identical to the backend's secret.

### 3. Run Development Server

```bash
npm run dev
```

### 4. Access the App

- Application: http://localhost:3000
- Login: http://localhost:3000/login
- Register: http://localhost:3000/register
- Dashboard: http://localhost:3000/dashboard

## Available Scripts

| Command | Description |
|---------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build production bundle |
| `npm run start` | Start production server |
| `npm run lint` | Run ESLint |

## Features

### Authentication
- User registration with email/password
- Login with session management
- JWT-based authentication
- Protected routes (automatic redirect to login)
- Logout functionality

### Task Management
- View all tasks (separated by completion status)
- Add new tasks with title and optional description
- Edit existing tasks via modal dialog
- Mark tasks complete/incomplete with checkbox
- Delete tasks with confirmation dialog

### User Experience
- Responsive design (320px+ mobile support)
- Loading spinners on all async operations
- User-friendly error messages
- Real-time form validation with character counters
- Success notifications
- Bottom sheet modals on mobile

## Component Overview

### TaskList (`components/tasks/TaskList.tsx`)
Displays tasks in two sections: Active and Completed. Handles task operations with optimistic updates and error handling.

### TaskItem (`components/tasks/TaskItem.tsx`)
Individual task card with:
- Checkbox for completion toggle
- Edit button (opens modal)
- Delete button (with confirmation)
- Visual distinction for completed tasks (strikethrough)
- Responsive layout (icon buttons on mobile)

### TaskForm (`components/tasks/TaskForm.tsx`)
Add new task form with:
- Title input (required, max 200 chars)
- Description textarea (optional, max 1000 chars)
- Character counters with warnings
- Loading state during submission
- Success toast notification

### TaskEditModal (`components/tasks/TaskEditModal.tsx`)
Edit task modal with:
- Pre-filled form fields
- Character counters
- Bottom sheet on mobile, centered modal on desktop
- Escape key to close
- Click outside to dismiss

## API Integration

The frontend communicates with the FastAPI backend via `lib/api.ts`:

```typescript
// Example usage
import * as api from '@/lib/api'

// Get all tasks
const tasks = await api.getTasks(userId)

// Create task
const newTask = await api.createTask(userId, { title: 'New task' })

// Toggle completion
const updated = await api.toggleComplete(userId, taskId)

// Update task
const edited = await api.updateTask(userId, taskId, { title: 'Updated' })

// Delete task
await api.deleteTask(userId, taskId)
```

## Error Handling

The app uses `lib/errors.ts` to convert technical errors to user-friendly messages:

| Technical Error | User Message |
|-----------------|--------------|
| `Failed to fetch` | "Unable to connect to server. Please check your internet connection." |
| `401` | "Your session has expired. Please log in again." |
| `403` | "You don't have permission to perform this action." |
| `404` | "The requested item was not found." |
| `422` | "Please check your input and try again." |
| `5xx` | "Something went wrong on our end. Please try again later." |

## Styling

The app uses Tailwind CSS with responsive breakpoints:

| Breakpoint | Width | Use Case |
|------------|-------|----------|
| Default | 0px+ | Mobile phones |
| `sm:` | 640px+ | Large phones, small tablets |
| `md:` | 768px+ | Tablets |
| `lg:` | 1024px+ | Laptops |
| `xl:` | 1280px+ | Desktops |

## Troubleshooting

### Common Issues

**"Unable to connect to server"**
- Ensure backend is running on the configured port
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend CORS allows frontend origin

**Login/Register not working**
- Verify `BETTER_AUTH_SECRET` matches backend exactly
- Check browser console for detailed errors
- Ensure `BETTER_AUTH_URL` is set correctly

**Tasks not loading**
- Verify you're logged in (check for session)
- Check browser network tab for API errors
- Ensure backend database is connected

**Build errors**
- Run `npm install` to ensure dependencies are installed
- Check for TypeScript errors: `npm run lint`
- Verify all environment variables are set

### Development Tips

1. **Hot Reload**: The dev server auto-reloads on file changes
2. **React DevTools**: Install the browser extension for debugging
3. **Network Tab**: Monitor API calls in browser developer tools
4. **Console Logs**: Check browser console for client-side errors

## Related

- [Backend README](../backend/README.md)
- [Main Project README](../README.md)
- [API Specification](../specs/spec.md)
