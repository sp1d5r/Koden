import type { Meta, StoryObj } from '@storybook/react';
import { Checkbox } from '@/components/atoms/checkbox';

const meta = {
  title: 'Atoms/Checkbox',
  component: Checkbox,
} satisfies Meta<typeof Checkbox>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
}; 