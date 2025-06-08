import type { Meta, StoryObj } from '@storybook/react';
import { Label } from '@/components/atoms/label';

const meta = {
  title: 'Atoms/Label',
  component: Label,
} satisfies Meta<typeof Label>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: 'Label',
  },
}; 