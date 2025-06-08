import type { Meta, StoryObj } from '@storybook/react';
import { Sidebar } from '@/components/atoms/sidebar';

const meta = {
  title: 'Atoms/Sidebar',
  component: Sidebar,
} satisfies Meta<typeof Sidebar>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <div className="flex h-full w-full flex-col gap-4 p-4">
        <div className="flex items-center gap-2">
          <div className="h-8 w-8 rounded-full bg-primary" />
          <div className="flex flex-col">
            <span className="text-sm font-medium">Sidebar</span>
            <span className="text-xs text-muted-foreground">Navigation</span>
          </div>
        </div>
        <nav className="flex flex-col gap-2">
          <a href="#" className="flex items-center gap-2 rounded-md px-3 py-2 hover:bg-accent">
            <span>Home</span>
          </a>
          <a href="#" className="flex items-center gap-2 rounded-md px-3 py-2 hover:bg-accent">
            <span>Settings</span>
          </a>
          <a href="#" className="flex items-center gap-2 rounded-md px-3 py-2 hover:bg-accent">
            <span>Profile</span>
          </a>
        </nav>
      </div>
    ),
  },
}; 