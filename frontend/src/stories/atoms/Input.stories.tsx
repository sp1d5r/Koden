import type { Meta, StoryObj } from '@storybook/react';
import { Input } from '@/components/atoms/input';

const meta = {
  title: 'Atoms/Input',
  component: Input,
} satisfies Meta<typeof Input>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    placeholder: 'Enter text here',
  },
}; 