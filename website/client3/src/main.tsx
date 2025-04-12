import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.scss'
import App from './App.tsx'
import { Provider } from "./components/ui/provider"

createRoot(document.getElementById('root')!).render(
    <StrictMode>
         <Provider>
            <App />
        </Provider>
    </StrictMode>
)
