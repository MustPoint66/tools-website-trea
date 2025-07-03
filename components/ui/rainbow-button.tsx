"use client";

import * as React from "react"
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { ButtonProps } from "@/components/ui/button";

interface RainbowButtonProps extends ButtonProps {
    rainbowEnabled?: boolean;
}

const RainbowButton = React.forwardRef<HTMLButtonElement, RainbowButtonProps>(
    ({ className, rainbowEnabled = true, children, ...props }, ref) => {
        return (
            <Button
                ref={ref}
                className={cn(
                    rainbowEnabled &&
                        "relative overflow-hidden bg-gradient-to-r from-[var(--color-1)] via-[var(--color-2)] to-[var(--color-3)] hover:animate-rainbow transition-all duration-300",
                    className
                )}
                style={
                    rainbowEnabled
                        ? {
                              "--color-1": "#ff6b6b",
                              "--color-2": "#4ecdc4", 
                              "--color-3": "#45b7d1",
                              "--color-4": "#96ceb4",
                              "--color-5": "#feca57",
                              "--color-6": "#ff9ff3",
                              "--color-7": "#54a0ff",
                          } as React.CSSProperties
                        : undefined
                }
                {...props}
            >
                {children}
            </Button>
        );
    }
);

RainbowButton.displayName = "RainbowButton";

export { RainbowButton, type RainbowButtonProps };
