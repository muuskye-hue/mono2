import { RuntimeProvider } from "./RuntimeProvider";
import { ChatThread } from "./components/ChatThread";
import { loadFrontendConfig } from "./config";
import "./App.css";

function App() {
  const { agentUrl } = loadFrontendConfig();

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="brand">mono2</p>
          <h1>Agent Chat</h1>
        </div>
        <p className="endpoint" title={agentUrl}>
          agent: {agentUrl}
        </p>
      </header>
      <main className="app-main">
        <RuntimeProvider>
          <ChatThread />
        </RuntimeProvider>
      </main>
    </div>
  );
}

export default App;
