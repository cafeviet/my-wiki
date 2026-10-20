import DefaultTheme from 'vitepress/theme'
import './custom.css'
import ChatInterface from './components/ChatInterface.vue'
import MermaidViewer from './components/MermaidViewer.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ChatInterface', ChatInterface)
    app.component('Mermaid', MermaidViewer)
  }
}
