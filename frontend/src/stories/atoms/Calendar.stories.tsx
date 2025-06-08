import type { Meta, StoryObj } from '@storybook/react';
import { Calendar } from '@/components/atoms/calendar';

const meta = {
  title: 'Atoms/Calendar',
  component: Calendar,
} satisfies Meta<typeof Calendar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
}; 