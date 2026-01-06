import { useEffect, useRef } from 'react'
import { useTheme } from '../context/ThemeContext'

const NeuralBackground = () => {
  const canvasRef = useRef(null)
  const { isDark } = useTheme()
  const animationFrameId = useRef(null)
  const nodesRef = useRef([])
  const mouseRef = useRef({ x: 0, y: 0 })

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas) return

    const ctx = canvas.getContext('2d')
    let width = window.innerWidth
    let height = window.innerHeight

    canvas.width = width
    canvas.height = height

    // Neural node class
    class Node {
      constructor() {
        this.reset()
      }

      reset() {
        this.x = Math.random() * width
        this.y = Math.random() * height
        this.vx = (Math.random() - 0.5) * 0.5
        this.vy = (Math.random() - 0.5) * 0.5
        this.radius = Math.random() * 3.5 + 2.5
        this.pulsePhase = Math.random() * Math.PI * 2
        this.pulseSpeed = 0.03 + Math.random() * 0.05
      }

      update() {
        this.x += this.vx
        this.y += this.vy

        // Bounce off edges
        if (this.x < 0 || this.x > width) {
          this.vx *= -1
          this.x = Math.max(0, Math.min(width, this.x))
        }
        if (this.y < 0 || this.y > height) {
          this.vy *= -1
          this.y = Math.max(0, Math.min(height, this.y))
        }

        // Update pulse
        this.pulsePhase += this.pulseSpeed
      }

      draw() {
        const pulse = Math.sin(this.pulsePhase) * 0.3 + 0.7
        const dynamicRadius = this.radius * pulse

        // Outer glow
        const gradient = ctx.createRadialGradient(
          this.x, this.y, 0,
          this.x, this.y, dynamicRadius * 2
        )
        
        if (isDark) {
          gradient.addColorStop(0, 'rgba(255, 215, 100, 1)')
          gradient.addColorStop(0.3, 'rgba(240, 240, 240, 0.9)')
          gradient.addColorStop(0.6, 'rgba(220, 200, 150, 0.5)')
          gradient.addColorStop(1, 'rgba(200, 200, 200, 0)')
        } else {
          gradient.addColorStop(0, 'rgba(200, 150, 50, 0.9)')
          gradient.addColorStop(0.5, 'rgba(100, 100, 100, 0.5)')
          gradient.addColorStop(1, 'rgba(120, 120, 120, 0)')
        }

        ctx.beginPath()
        ctx.arc(this.x, this.y, dynamicRadius * 2, 0, Math.PI * 2)
        ctx.fillStyle = gradient
        ctx.fill()

        // Core
        ctx.beginPath()
        ctx.arc(this.x, this.y, dynamicRadius, 0, Math.PI * 2)
        ctx.fillStyle = isDark ? 'rgba(255, 223, 150, 1)' : 'rgba(180, 130, 40, 0.95)'
        ctx.fill()
      }
    }

    // Initialize nodes
    const nodeCount = Math.min(150, Math.floor((width * height) / 8000))
    nodesRef.current = Array.from({ length: nodeCount }, () => new Node())

    // Mouse interaction
    const handleMouseMove = (e) => {
      mouseRef.current = { x: e.clientX, y: e.clientY }
    }
    window.addEventListener('mousemove', handleMouseMove)

    // Animation loop
    let lastTime = 0
    const targetFPS = 30
    const frameDelay = 1000 / targetFPS

    const animate = (currentTime) => {
      const elapsed = currentTime - lastTime

      if (elapsed > frameDelay) {
        lastTime = currentTime - (elapsed % frameDelay)

        // Clear with fade effect
        ctx.fillStyle = isDark ? 'rgba(0, 0, 0, 0.15)' : 'rgba(250, 250, 250, 0.15)'
        ctx.fillRect(0, 0, width, height)

        // Update and draw nodes
        nodesRef.current.forEach(node => {
          node.update()
          node.draw()
        })

        // Draw dynamic connections
        const maxDistance = 200
        const mouseInfluence = 120
        
        for (let i = 0; i < nodesRef.current.length; i++) {
          const node1 = nodesRef.current[i]
          
          // Connect to nearby nodes
          for (let j = i + 1; j < Math.min(i + 20, nodesRef.current.length); j++) {
            const node2 = nodesRef.current[j]
            const dx = node1.x - node2.x
            const dy = node1.y - node2.y
            const distance = Math.sqrt(dx * dx + dy * dy)

            if (distance < maxDistance) {
              // Check mouse proximity for enhanced connections
              const dmx = (node1.x + node2.x) / 2 - mouseRef.current.x
              const dmy = (node1.y + node2.y) / 2 - mouseRef.current.y
              const mouseDist = Math.sqrt(dmx * dmx + dmy * dmy)
              const mouseEffect = mouseDist < mouseInfluence ? (1 - mouseDist / mouseInfluence) : 0

              ctx.beginPath()
              ctx.moveTo(node1.x, node1.y)
              ctx.lineTo(node2.x, node2.y)

              const baseOpacity = (1 - distance / maxDistance) * 0.6
              const totalOpacity = Math.min(baseOpacity + mouseEffect * 0.6, 1)
              const lineWidth = 1.2 + mouseEffect * 2

              ctx.strokeStyle = isDark
                ? `rgba(245, 220, 170, ${totalOpacity})`
                : `rgba(150, 110, 40, ${totalOpacity})`
              ctx.lineWidth = lineWidth
              ctx.stroke()

              // Draw data pulse effect on strong connections
              if (mouseEffect > 0.3) {
                const pulsePos = (Date.now() % 1000) / 1000
                const pulseX = node1.x + (node2.x - node1.x) * pulsePos
                const pulseY = node1.y + (node2.y - node1.y) * pulsePos

                ctx.beginPath()
                ctx.arc(pulseX, pulseY, 3, 0, Math.PI * 2)
                ctx.fillStyle = isDark
                  ? `rgba(255, 215, 100, ${mouseEffect})`
                  : `rgba(200, 140, 30, ${mouseEffect * 0.8})`
                ctx.fill()
                
                // Add glow to pulse
                ctx.beginPath()
                ctx.arc(pulseX, pulseY, 6, 0, Math.PI * 2)
                ctx.fillStyle = isDark
                  ? `rgba(255, 230, 150, ${mouseEffect * 0.3})`
                  : `rgba(180, 130, 40, ${mouseEffect * 0.2})`
                ctx.fill()
              }
            }
          }
        }
      }

      animationFrameId.current = requestAnimationFrame(animate)
    }

    animate(0)

    // Handle resize
    let resizeTimeout
    const handleResize = () => {
      clearTimeout(resizeTimeout)
      resizeTimeout = setTimeout(() => {
        width = window.innerWidth
        height = window.innerHeight
        canvas.width = width
        canvas.height = height
        
        const newNodeCount = Math.min(150, Math.floor((width * height) / 8000))
        nodesRef.current = Array.from({ length: newNodeCount }, () => new Node())
      }, 300)
    }

    window.addEventListener('resize', handleResize)

    // Cleanup
    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current)
      }
      window.removeEventListener('mousemove', handleMouseMove)
      window.removeEventListener('resize', handleResize)
      clearTimeout(resizeTimeout)
    }
  }, [isDark])

  return (
    <canvas
      ref={canvasRef}
      className="fixed top-0 left-0 w-full h-full pointer-events-none"
      style={{ 
        opacity: isDark ? 0.55 : 0.45,
        zIndex: 0,
        mixBlendMode: isDark ? 'screen' : 'multiply'
      }}
    />
  )
}

export default NeuralBackground
