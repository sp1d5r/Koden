import type { Meta, StoryObj } from '@storybook/react';
import { Sheet, SheetContent, SheetDescription, SheetHeader, SheetTitle, SheetTrigger } from '@/components/atoms/sheet';
import { Button } from '@/components/atoms/button';

const meta = {
  title: 'Atoms/Sheet',
  component: Sheet,
} satisfies Meta<typeof Sheet>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <>
        <SheetTrigger asChild>
          <Button>Open Sheet</Button>
        </SheetTrigger>
        <SheetContent>
          <SheetHeader>
            <SheetTitle>Sheet Title</SheetTitle>
            <SheetDescription>
              This is a sheet component that slides in from the side.
            </SheetDescription>
          </SheetHeader>
          <div className="py-4">
            <p>Sheet content goes here.</p>
          </div>
        </SheetContent>
      </>
    ),
  },
}; 