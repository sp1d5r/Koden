import type { Meta, StoryObj } from '@storybook/react';
import { Switch } from '@/components/atoms/switch';

const meta = {
  title: 'Atoms/Switch',
  component: Switch,
} satisfies Meta<typeof Switch>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
}; 