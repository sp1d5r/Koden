import { AppSidebar } from "@/components/molecules/sidebar"
import { SidebarProvider, SidebarInset } from "@/components/atoms/sidebar"

export default function DashboardLayout({ children, onConnectRepo }: { children?: React.ReactNode, onConnectRepo?: () => void }) {
  return (
    <SidebarProvider
      style={{
        "--sidebar-width": "calc(var(--spacing) * 72)",
        "--header-height": "calc(var(--spacing) * 12)",
      } as React.CSSProperties}
    >
      <AppSidebar variant="inset" onConnectRepo={onConnectRepo} />
      <SidebarInset>
        {/* Main dashboard content goes here */}
        <div className="flex flex-1 flex-col p-6">
          {children || <div className="text-muted-foreground">Dashboard content placeholder</div>}
        </div>
      </SidebarInset>
    </SidebarProvider>
  )
} 