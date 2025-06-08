import type { Meta, StoryObj } from '@storybook/react';
import { NavigationMenu, NavigationMenuContent, NavigationMenuItem, NavigationMenuLink, NavigationMenuList, NavigationMenuTrigger } from '@/components/atoms/navigation-menu';

const meta = {
  title: 'Atoms/NavigationMenu',
  component: NavigationMenu,
} satisfies Meta<typeof NavigationMenu>;

export default meta;
type Story = StoryObj<typeof meta>;

export const Default: Story = {
  args: {
    children: (
      <NavigationMenuList>
        <NavigationMenuItem>
          <NavigationMenuTrigger>Getting Started</NavigationMenuTrigger>
          <NavigationMenuContent>
            <NavigationMenuLink>Documentation</NavigationMenuLink>
            <NavigationMenuLink>Components</NavigationMenuLink>
            <NavigationMenuLink>Examples</NavigationMenuLink>
          </NavigationMenuContent>
        </NavigationMenuItem>
      </NavigationMenuList>
    ),
  },
}; 