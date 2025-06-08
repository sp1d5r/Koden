import type { Meta, StoryObj } from '@storybook/react'
import { Hero } from '@/components/molecules/hero'

const meta: Meta<typeof Hero> = {
  title: 'Molecules/Hero',
  component: Hero,
  parameters: {
    layout: 'fullscreen',
  },
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof Hero>

export const Default: Story = {} 