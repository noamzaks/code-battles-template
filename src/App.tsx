import { CodeBattles } from "code-battles"
import "code-battles/styles.css"
import config from "./firebase.json"

const App = () => {
  return (
    <CodeBattles
      configuration={{
        firebase: config,
        maps: ["NYC"],
      }}
      routes={{}}
    />
  )
}

export default App
