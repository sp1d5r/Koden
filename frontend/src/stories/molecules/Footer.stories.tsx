import type { Meta, StoryObj } from '@storybook/react'
import { Footer } from '@/components/molecules/footer'

const meta: Meta<typeof Footer> = {
  title: 'Molecules/Footer',
  component: Footer,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof Footer>

export const Default: Story = {} 