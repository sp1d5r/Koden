"use client"

import { Card } from "@/components/atoms/card"
import { useEffect, useState } from "react"

const steps = [
  { id: 1, label: "Analyze structure" },
  { id: 2, label: "Track dependencies" },
  { id: 3, label: "Spot hotspots" },
  { id: 4, label: "Export insights" },
]

export function VisualPreviewCard() {
  const [activeStep, setActiveStep] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setActiveStep((prev) => (prev + 1) % steps.length)
    }, 1200)
    return () => clearInterval(interval)
  }, [])

  return (
    <Card className="w-full max-w-md bg-background/80 border border-primary/20 shadow-xl p-8 flex flex-col gap-4 transition-all duration-500">
      {/* Animated gradient bar */}
      <div className="h-6 w-32 rounded-full bg-gradient-to-r from-primary via-accent to-secondary mb-4 animate-pulse" />
      {/* Animated steps */}
      {steps.map((step, idx) => (
        <div
          key={step.id}
          className={`h-6 w-full rounded transition-all duration-500 mb-2 flex items-center px-4 text-sm font-medium ${
            activeStep === idx
              ? "bg-primary/30 text-primary shadow-lg scale-105"
              : "bg-muted text-muted-foreground opacity-60"
          }`}
        >
          {step.label}
        </div>
      ))}
      {/* Simulated action buttons */}
      <div className="flex gap-2 mt-4">
        <div className="h-8 w-1/2 rounded bg-primary/20 animate-pulse" />
        <div className="h-8 w-1/2 rounded bg-muted" />
      </div>
    </Card>
  )
} 