import type { Meta, StoryObj } from '@storybook/react';
import { ScrollArea } from '@/components/atoms/scroll-area';

const meta = {
  title: 'Atoms/ScrollArea',
  component: ScrollArea,
} satisfies Meta<typeof ScrollArea>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    className: "h-[200px] w-[350px] rounded-md border p-4",
    children: (
      <div className="space-y-4">
        <h4 className="text-sm font-medium leading-none">Scroll Area</h4>
        {Array.from({ length: 20 }).map((_, i) => (
          <div key={i} className="text-sm">
            Item {i + 1}
          </div>
        ))}
      </div>
    ),
  },
}; 