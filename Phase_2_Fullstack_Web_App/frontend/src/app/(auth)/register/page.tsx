import Link from 'next/link'
import RegisterForm from '@/components/auth/RegisterForm'
import Card from '@/components/ui/Card'

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4">
      <Card className="w-full max-w-md">
        <div className="text-center mb-6">
          <h1 className="text-2xl font-bold text-gray-900">Create Account</h1>
          <p className="text-gray-600 mt-1">Start managing your tasks today</p>
        </div>

        <RegisterForm />

        <div className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link href="/login" className="text-primary-600 hover:underline">
            Sign in here
          </Link>
        </div>
      </Card>
    </div>
  )
}
