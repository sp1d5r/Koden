import type { Meta, StoryObj } from '@storybook/react';
import { Toaster } from '@/components/atoms/sonner';

const meta = {
  title: 'Atoms/Sonner',
  component: Toaster,
} satisfies Meta<typeof Toaster>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
}; 