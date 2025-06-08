import type { Meta, StoryObj } from '@storybook/react';
import { ChartContainer } from '@/components/atoms/chart';

const meta = {
  title: 'Atoms/Chart',
  component: ChartContainer,
} satisfies Meta<typeof ChartContainer>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    config: {
      value: { label: 'Value', color: '#000' },
    },
    children: (
      <div>Chart Content</div>
    ),
  },
}; 