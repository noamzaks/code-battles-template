import { CodeBattles } from "code-battles-components"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        maps: ["NYC"],
      }}
    />
  )
}

export default App
