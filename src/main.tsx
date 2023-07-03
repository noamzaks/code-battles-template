import React from "react"
import ReactDOM from "react-dom/client"
import App from "./App"

import { initialize } from "code-battles-components"

initialize()

ReactDOM.createRoot(document.getElementById("root") as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
)
