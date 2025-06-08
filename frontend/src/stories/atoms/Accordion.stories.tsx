import type { Meta, StoryObj } from '@storybook/react';
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/atoms/accordion';

const meta = {
  title: 'Atoms/Accordion',
  component: Accordion,
} satisfies Meta<typeof Accordion>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    type: 'single',
    children: (
      <AccordionItem value="item-1">
        <AccordionTrigger>Accordion Trigger</AccordionTrigger>
        <AccordionContent>Accordion Content</AccordionContent>
      </AccordionItem>
    ),
  },
}; 