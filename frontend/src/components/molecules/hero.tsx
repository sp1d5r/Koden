"use client"

import { Button } from "@/components/atoms/button"
import { VisualPreviewCard } from "@/components/molecules/visual-preview-card"
import { useAuth } from "@/hooks/useAuth"
import { useRouter } from "next/navigation"

export function Hero() {
  const { user } = useAuth()
  const router = useRouter()

  const handleGetStarted = (e: React.MouseEvent) => {
    e.preventDefault()
    router.push(user ? "/app" : "/login")
  }

  return (
    <section className="container mx-auto px-4 sm:px-6 lg:px-8 flex flex-col lg:flex-row items-center justify-between gap-12 py-20 min-h-[70vh]">
      {/* Left: Text Content */}
      <div className="flex-1 flex flex-col items-start gap-8 max-w-2xl">
        {/* Badge */}
        <span className="inline-flex items-center rounded-full bg-primary/10 px-4 py-1 text-sm font-medium text-primary mb-2">
          <span className="w-2 h-2 rounded-full bg-primary mr-2"></span>
          Structural Codebase Analyzer
        </span>
        {/* Headline */}
        <h1 className="text-4xl md:text-6xl font-bold leading-tight tracking-tight text-foreground">
          <span className="font-sans">Understand your codebase </span>
          <span className="italic font-serif text-primary">like never before.</span>
        </h1>
        {/* Subtext */}
        <p className="text-lg md:text-xl text-muted-foreground max-w-xl">
          Visualize, analyze, and master your code's structure. Koden gives you instant insight into dependencies, hotspots, and architecture health.
        </p>
        {/* Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 w-full sm:w-auto">
          <Button size="lg" className="w-full sm:w-auto" onClick={handleGetStarted}>Get Started</Button>
          <Button size="lg" variant="outline" className="w-full sm:w-auto" onClick={() => router.push('/examples')}>View Examples</Button>
        </div>
        {/* Feature Highlights */}
        <div className="flex flex-wrap gap-6 mt-4 text-base">
          <div className="flex items-center gap-2 text-foreground">
            <span className="text-primary">🔍</span> Visualize structure
          </div>
          <div className="flex items-center gap-2 text-foreground">
            <span className="text-primary">🧠</span> Spot hotspots
          </div>
          <div className="flex items-center gap-2 text-foreground">
            <span className="text-primary">🛠</span> Build with confidence
          </div>
          <div className="flex items-center gap-2 text-foreground">
            <span className="text-primary">⚙️</span> GitHub integration
          </div>
        </div>
      </div>
      {/* Right: Visual Preview Card */}
      <div className="flex-1 flex items-center justify-center w-full max-w-xl">
        <VisualPreviewCard />
      </div>
    </section>
  )
} 