import type { Meta, StoryObj } from '@storybook/react';
import { AspectRatio } from '@/components/atoms/aspect-ratio';

const meta = {
  title: 'Atoms/AspectRatio',
  component: AspectRatio,
} satisfies Meta<typeof AspectRatio>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    ratio: 16 / 9,
    children: <div className="bg-gray-200 w-full h-full flex items-center justify-center">Aspect Ratio Content</div>,
  },
}; 