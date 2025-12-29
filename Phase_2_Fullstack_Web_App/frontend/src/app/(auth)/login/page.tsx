import Link from 'next/link'
import LoginForm from '@/components/auth/LoginForm'
import Card from '@/components/ui/Card'

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Welcome Back</h1>
          <p className="text-gray-600 mt-1">Sign in to your account</p>
        </div>

        <LoginForm />

        <div className="mt-6 text-center text-sm text-gray-600">
          Don&apos;t have an account?{' '}
          <Link href="/register" className="text-primary-600 hover:underline">
            Register here
          </Link>
        </div>
      </Card>
    </div>
  )
}
