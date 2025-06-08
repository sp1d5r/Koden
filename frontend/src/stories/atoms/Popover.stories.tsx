import type { Meta, StoryObj } from '@storybook/react';
import { Popover, PopoverContent, PopoverTrigger } from '@/components/atoms/popover';
import { Button } from '@/components/atoms/button';

const meta = {
  title: 'Atoms/Popover',
  component: Popover,
} satisfies Meta<typeof Popover>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <>
        <PopoverTrigger asChild>
          <Button>Open Popover</Button>
        </PopoverTrigger>
        <PopoverContent>
          <div className="p-4">
            <h4 className="font-medium">Popover Content</h4>
            <p className="text-sm text-muted-foreground">This is some content inside the popover.</p>
          </div>
        </PopoverContent>
      </>
    ),
  },
}; 