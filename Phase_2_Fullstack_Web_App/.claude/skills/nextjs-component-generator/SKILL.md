# Next.js Component Generator

## Auto-Generated
- **Trigger**: Creating React components for Next.js App Router
- **Created**: 2025-12-29
- **Phase**: Phase 2 - Fullstack Web App
- **Reuse Count**: 0

## Purpose
Generate consistent, type-safe React components following Next.js 15+ App Router conventions with TypeScript and Tailwind CSS.

## When to Use
- Creating new UI components in `frontend/src/components/`
- Creating new pages in `frontend/src/app/`
- Building form components with validation
- Creating reusable UI primitives

## Component Types

### 1. Server Components (Default)
```typescript
// frontend/src/components/[name]/[Name].tsx
import { ComponentProps } from "@/types/component";

interface [Name]Props {
  // Define props here
}

export default function [Name]({ ...props }: [Name]Props) {
  return (
    <div className="">
      {/* Component content */}
    </div>
  );
}
```

### 2. Client Components (Interactive)
```typescript
// frontend/src/components/[name]/[Name].tsx
"use client";

import { useState } from "react";

interface [Name]Props {
  // Define props here
}

export default function [Name]({ ...props }: [Name]Props) {
  const [state, setState] = useState<Type>(initialValue);

  return (
    <div className="">
      {/* Interactive content */}
    </div>
  );
}
```

### 3. Form Components
```typescript
// frontend/src/components/forms/[Name]Form.tsx
"use client";

import { useState, FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";

interface [Name]FormProps {
  onSubmit: (data: FormData) => Promise<void>;
  initialData?: Partial<FormData>;
}

interface FormData {
  // Form fields
}

export default function [Name]Form({ onSubmit, initialData }: [Name]FormProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);

    try {
      const formData = new FormData(e.currentTarget);
      const data: FormData = {
        // Extract form data
      };
      await onSubmit(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="text-red-500 text-sm">{error}</div>
      )}
      {/* Form fields */}
      <Button type="submit" disabled={isLoading}>
        {isLoading ? "Loading..." : "Submit"}
      </Button>
    </form>
  );
}
```

### 4. Page Components (App Router)
```typescript
// frontend/src/app/[route]/page.tsx
import { Metadata } from "next";

export const metadata: Metadata = {
  title: "[Page Title]",
  description: "[Page description]",
};

interface PageProps {
  params: { [key: string]: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function [Name]Page({ params, searchParams }: PageProps) {
  // Fetch data if needed (server component)

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">[Page Title]</h1>
      {/* Page content */}
    </main>
  );
}
```

### 5. Layout Components
```typescript
// frontend/src/app/[route]/layout.tsx
import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}

export default function [Name]Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen">
      {/* Layout structure */}
      {children}
    </div>
  );
}
```

## File Structure Convention

```
frontend/src/
├── app/
│   ├── (auth)/           # Route group for auth pages
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── dashboard/
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── layout.tsx        # Root layout
│   └── page.tsx          # Home page
├── components/
│   ├── auth/             # Auth-related components
│   │   ├── LoginForm.tsx
│   │   └── RegisterForm.tsx
│   ├── tasks/            # Task-related components
│   │   ├── TaskForm.tsx
│   │   ├── TaskItem.tsx
│   │   └── TaskList.tsx
│   └── ui/               # Reusable UI primitives
│       ├── Button.tsx
│       ├── Card.tsx
│       └── Input.tsx
├── lib/
│   ├── api.ts            # API client
│   └── auth.ts           # Auth configuration
└── types/
    └── task.ts           # Type definitions
```

## Tailwind CSS Patterns

### Common Classes
```
Layout: container, mx-auto, px-4, py-8, flex, grid, space-y-4
Typography: text-xl, font-bold, text-gray-600, text-red-500
Spacing: p-4, m-2, gap-4, space-x-2
Borders: rounded, border, shadow-md
States: hover:bg-gray-100, focus:ring-2, disabled:opacity-50
Responsive: sm:flex, md:grid-cols-2, lg:px-8
```

### Button Variants
```typescript
const variants = {
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  secondary: "bg-gray-200 text-gray-800 hover:bg-gray-300",
  danger: "bg-red-600 text-white hover:bg-red-700",
  ghost: "hover:bg-gray-100",
};
```

## Checklist Before Creating Component

- [ ] Determine if Server or Client Component
- [ ] Define TypeScript interface for props
- [ ] Plan state management (if client)
- [ ] Consider loading and error states
- [ ] Add proper accessibility attributes
- [ ] Use consistent Tailwind patterns
- [ ] Export from correct location

## Error Handling Pattern

```typescript
"use client";

import { useState } from "react";

export default function ComponentWithError() {
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  if (error) {
    return (
      <div className="p-4 bg-red-50 border border-red-200 rounded">
        <p className="text-red-600">{error}</p>
        <button
          onClick={() => setError(null)}
          className="text-sm text-red-500 underline mt-2"
        >
          Try again
        </button>
      </div>
    );
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="animate-spin h-8 w-8 border-4 border-blue-500 rounded-full border-t-transparent" />
      </div>
    );
  }

  return (/* Normal content */);
}
```

## Integration with API

```typescript
"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { Task } from "@/types/task";

export default function TaskList({ userId }: { userId: string }) {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const data = await api.tasks.list(userId);
        setTasks(data);
      } catch (err) {
        setError("Failed to load tasks");
      } finally {
        setIsLoading(false);
      }
    };
    fetchTasks();
  }, [userId]);

  // Render based on state
}
```

---

## Version
- **Version**: 1.0.0
- **Created**: 2025-12-29
- **Category**: Frontend Development
- **Reuse Potential**: High (all React/Next.js components)
