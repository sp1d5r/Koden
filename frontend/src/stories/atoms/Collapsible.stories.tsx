import type { Meta, StoryObj } from '@storybook/react';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/atoms/collapsible';

const meta = {
  title: 'Atoms/Collapsible',
  component: Collapsible,
} satisfies Meta<typeof Collapsible>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <>
        <CollapsibleTrigger>Collapsible Trigger</CollapsibleTrigger>
        <CollapsibleContent>Collapsible Content</CollapsibleContent>
      </>
    ),
  },
}; 