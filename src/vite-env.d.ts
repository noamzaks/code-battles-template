/// <reference types="vite/client" />
import React from "react"

declare global {
  namespace JSX {
    interface IntrinsicElements {
      "py-script": React.DetailedHTMLProps<
        React.HTMLAttributes<HTMLElement>,
        HTMLElement
      >
    }
  }
}
