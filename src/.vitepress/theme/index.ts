import DefaultTheme from 'vitepress/theme'
import './custom.css'
import ChatInterface from './components/ChatInterface.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app }) {
    app.component('ChatInterface', ChatInterface)
  }
}
