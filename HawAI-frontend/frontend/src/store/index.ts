import { createStore } from 'vuex'
import * as api from '../services/api'

export interface Message {
  text: string
  from: 'user' | 'bot'
  tags?: string[]
  sources?: { title: string; url: string }[]
}

export interface RootState {
  messages: Message[]
  isLoading: boolean
  rateLimited: boolean
  health: { reachable: boolean | null }
}

export default createStore<RootState>({
  state: {
    messages: [],
    isLoading: false,
    rateLimited: false,
    health: { reachable: null }
  },
  mutations: {
    addMessage(state, msg: Message) {
      state.messages.push(msg)
    },
    clearMessages(state) {
      state.messages = []
    },
    setLoading(state, val: boolean) {
      state.isLoading = val
    },
    setRateLimited(state, val: boolean) {
      state.rateLimited = val
    },
    setHealth(state, reachable: boolean | null) {
      state.health.reachable = reachable
    }
  },
  actions: {
    async sendMessage({ commit }, text: string) {
      if (!text || !text.trim()) return
      commit('setLoading', true)
      commit('setRateLimited', false)
      commit('addMessage', { text, from: 'user' } as Message)
      try {
        const res = await api.chat(text)
        if (!res.ok) {
          if (res.rateLimited) {
            commit('setRateLimited', true)
          }
          throw new Error(res.error || 'İstek başarısız')
        }
        commit('addMessage', { text: res.data.reply, from: 'bot', tags: res.data.sdg_tags, sources: res.data.sources })
      } catch (e) {
        console.error(e)
      } finally {
        commit('setLoading', false)
      }
    },
    async fetchHealth({ commit }) {
      try {
        const res = await api.health()
        commit('setHealth', res.ok ? !!res.data?.ollama?.reachable : null)
      } catch (e) {
        commit('setHealth', null)
      }
    }
  },
  modules: {}
})
