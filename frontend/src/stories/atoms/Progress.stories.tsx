import type { Meta, StoryObj } from '@storybook/react';
import { Progress } from '@/components/atoms/progress';

const meta = {
  title: 'Atoms/Progress',
  component: Progress,
} satisfies Meta<typeof Progress>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    value: 33,
  },
}; 