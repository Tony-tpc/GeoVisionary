<script setup>
// 删除所有与 API_KEY 相关的代码
// 修改发送逻辑为调用后端接口
import { ref, reactive } from 'vue'

const messages = reactive([])
const isLoading = ref(false)

const sendMessage = async () => {
  if (!inputText.value.trim() || isLoading.value) return
  
  isLoading.value = true
  messages.push({ role: 'user', content: inputText.value })
  
  try {
    const response = await fetch('http://localhost:8000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message: inputText.value,
        history: messages.slice(-5) // 发送最近5条历史记录
      })
    })
    
    const reader = response.body.getReader()
    const decoder = new TextDecoder()
    let assistantMessage = { role: 'assistant', content: '' }
    
    messages.push(assistantMessage)
    
    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value)
      const data = JSON.parse(chunk)
      
      if (!data.completed) {
        assistantMessage.content += data.content
      } else {
        // 处理坐标数据
        if (data.coordinates?.length > 0) {
          coordinates.value = data.coordinates
        }
      }
    }
  } catch (error) {
    console.error('请求失败:', error)
  } finally {
    isLoading.value = false
  }
  
  inputText.value = ''
}
</script>
