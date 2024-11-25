<template>
  <a-select
  ref="autocomplete"
  v-model:value="value"
  :options="options.data"
  show-search
  allowClear
  class="w-full"
  :class="props.class"
  :style="props.style"
  :mode="props.mode"
  :disabled="props.disabled"
  max-tag-count="responsive"
  :size="attrs.size || 'default'"
  :filterOption="false"
  @search="reload"
  @change="setValue"
  >
    <template #option="{ value, description }">
      <strong>{{ value }}</strong><br><span class="small">{{ description }}</span>
    </template>
  </a-select>
</template>

<script setup>
import { watchDebounced } from '@vueuse/core'
import { createResource } from 'frappe-ui'
import { useAttrs, computed, ref } from 'vue'

const props = defineProps({
  doctype: {
    type: String,
    required: true,
  },
  modelValue: {
    type: String,
    default: '',
  },
  hideMe: {
    type: Boolean,
    default: false,
  },
  mode: {
    type: String,
    default: undefined,
  },
  query: {
    type: String,
    default: undefined,
  },
  filters: {
    type: Object,
    default: undefined,
  },
  class: {
    type: String,
    default: '',
  },
  style: {
    type: Object,
    default: undefined
  },
  disabled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const attrs = useAttrs()

const valuePropPassed = computed(() => 'value' in attrs)

const value = computed({
  get: () => (valuePropPassed.value ? attrs.value : props.modelValue),
  set: (val) => {
    return (
      val?.value &&
      emit(valuePropPassed.value ? 'change' : 'update:modelValue', val?.value)
    )
  },
})

const autocomplete = ref(null)
const text = ref('')

watchDebounced(
  () => autocomplete.value,
  (val) => {
    val = val || ''
    if (text.value === val) return
    text.value = val
    reload(val)
  },
  { debounce: 300, immediate: true }
)

watchDebounced(
  () => props.doctype,
  () => reload(''),
  { debounce: 300, immediate: true }
)

const options = createResource({
  url: 'frappe.desk.search.search_link',
  cache: [props.doctype, text.value, props.hideMe],
  method: 'POST',
  params: {
    txt: text.value || '',
    doctype: props.doctype,
    // ...(props.query ? {query: props.query} : {}),
    ...(props.filters ? {filters: props.filters} : {}),
  },
  transform: (data) => {
    let allData = data.map((option) => {
      return {
        label: option.value,
        value: option.value,
      }
    })
    if (!props.hideMe && props.doctype == 'User') {
      allData.unshift({
        label: '@me',
        value: '@me',
      })
    }
    return allData
  },
})

function reload(val) {
  if (
    options.data?.length &&
    val === options.params?.txt &&
    props.doctype === options.params?.doctype
  )
    return
  
  if (typeof val !== 'string') return

  options.update({
    params: {
      txt: val || '',
      doctype: props.doctype,
      // ...(props.query ? {query: props.query} : {}),
      ...(props.filters ? {filters: props.filters} : {}),
    },
  })
  options.reload()
}

function setValue(val) {
  emit(valuePropPassed.value ? 'change' : 'update:modelValue', val)
}

function clearValue(close) {
  emit(valuePropPassed.value ? 'change' : 'update:modelValue', '')
  close()
}

</script>