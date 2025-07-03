import { render, screen, fireEvent } from '@testing-library/react'
import '@testing-library/jest-dom'
import { ToastProvider, useToast } from '../toast'

const TestComponent: React.FC = () => {
  const toast = useToast()

  return (
    <div>
      <button onClick={() => toast.success('Success', 'This is a success message')}>
        Show Success Toast
      </button>
    </div>
  )
}

describe('ToastProvider', () => {
  it('should render toast messages', () => {
    render(
      <ToastProvider>
        <TestComponent />
      </ToastProvider>
    )

    // Trigger toast
    fireEvent.click(screen.getByText('Show Success Toast'))

    // Check if toast is rendered
    expect(screen.getByText('This is a success message')).toBeInTheDocument()
    expect(screen.getByText('Success')).toBeInTheDocument()
  })
})
