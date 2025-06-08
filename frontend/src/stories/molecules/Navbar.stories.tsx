import type { Meta, StoryObj } from '@storybook/react'
import { Navbar } from '@/components/molecules/navbar'
import { ThemeProvider } from '@/components/providers/theme-provider'

const meta: Meta<typeof Navbar> = {
  title: 'Molecules/Navbar',
  component: Navbar,
  parameters: {
    layout: 'fullscreen',
  },
  decorators: [
    (Story) => (
      <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
        <Story />
      </ThemeProvider>
    ),
  ],
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof Navbar>

export const Default: Story = {} 