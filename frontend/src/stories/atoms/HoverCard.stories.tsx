import type { Meta, StoryObj } from '@storybook/react';
import { HoverCard, HoverCardContent, HoverCardTrigger } from '@/components/atoms/hover-card';

const meta = {
  title: 'Atoms/HoverCard',
  component: HoverCard,
} satisfies Meta<typeof HoverCard>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <>
        <HoverCardTrigger>Hover me</HoverCardTrigger>
        <HoverCardContent>Hover Card Content</HoverCardContent>
      </>
    ),
  },
}; 