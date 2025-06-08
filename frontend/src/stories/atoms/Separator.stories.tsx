import type { Meta, StoryObj } from '@storybook/react';
import { Separator } from '@/components/atoms/separator';

const meta = {
  title: 'Atoms/Separator',
  component: Separator,
} satisfies Meta<typeof Separator>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {},
}; 