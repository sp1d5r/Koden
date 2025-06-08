import type { Meta, StoryObj } from '@storybook/react'
import { VisualPreviewCard } from '@/components/molecules/visual-preview-card'

const meta: Meta<typeof VisualPreviewCard> = {
  title: 'Molecules/VisualPreviewCard',
  component: VisualPreviewCard,
  parameters: {
    layout: 'centered',
  },
  tags: ['autodocs'],
}

export default meta

type Story = StoryObj<typeof VisualPreviewCard>

export const Default: Story = {} 