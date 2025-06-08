import { Navbar } from "@/components/molecules/navbar"
import { Hero } from "@/components/molecules/hero"
import { Footer } from "@/components/molecules/footer"

export default function Home() {
  return (
    <div className="relative min-h-screen flex flex-col">
      <Navbar />
      <main className="flex-1">
        <Hero />
      </main>
      <Footer />
    </div>
  )
}
