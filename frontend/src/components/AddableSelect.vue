<template>
  <a-select
    :disabled="disabled"
    :value="modelValue"
    :options="displayedOptions"
    :labelInValue="labelInValue"
    :mode="mode"
    :placeholder="placeholder"
    :loading="loading"
    :filter-option="filterOption"
    :allowClear="allowClear"
    :fieldNames="fieldNames"
    @search="handleSearch"
    @change="handleChange"
    @select="handleSelect"
    @deselect="handleDeselect"
    style="width: 100%"
  >
    <!-- Customize option rendering -->
    <template #option="{ option }">
      <div :class="['custom-option', { 'add-option': option.isAddOption }]">
        {{ option.label }}
      </div>
    </template>
  </a-select>
</template>


<script>
import { ref, computed, watch } from 'vue';
import { Select } from 'ant-design-vue';

export default {
  name: 'AddableSelect',
  components: {
    'a-select': Select,
  },
  props: {
    modelValue: {
      type: [String, Number, Array, Object],
      default: null,
    },
    options: {
      type: Array,
      default: () => [],
    },
    labelInValue: {
      type: Boolean,
      default: false,
    },
    mode: {
      type: String,
      default: undefined,
    },
    placeholder: {
      type: String,
      default: 'Please select',
    },
    disabled: {
      type: Boolean,
      default: false,
    },
    loading: {
      type: Boolean,
      default: false,
    },
    filterOption: {
      type: [Boolean, Function],
      default: true,
    },
    allowClear: {
      type: Boolean,
      default: false,
    },
    fieldNames: {
      type: Object,
      default: () => ({}),
    },
    // Add more props as needed to pass through to <a-select>
  },
  emits: [
    'update:modelValue',
    'select',
    'deselect',
    'search',
    'add',
    'change',
    // Add more emits as needed
  ],
  setup(props, { emit }) {
    const searchValue = ref('');
    const internalOptions = ref([...props.options]);

    // Watch for changes in the options prop to keep internalOptions in sync
    watch(
      () => props.options,
      (newOptions) => {
        internalOptions.value = [...newOptions];
      },
      { deep: true }
    );

    // Computed property to include "Add" option if necessary
    const displayedOptions = computed(() => {
      const filteredOptions = internalOptions.value.filter(option =>
        option.label.toLowerCase().includes(searchValue.value.toLowerCase())
      );

      const isExisting = internalOptions.value.some(
        option => option.label.toLowerCase() === searchValue.value.toLowerCase()
      );

      // If not exists and there's a search input, add the "Add" option
      if (searchValue.value && !isExisting) {
        filteredOptions.push({
          label: `Add "${searchValue.value}"`,
          value: `__add__${searchValue.value}`, // Unique identifier for "Add" option
          isAddOption: true, // Custom flag to identify in rendering
        });
      }

      return filteredOptions;
    });

    // Debounce search input to avoid excessive processing
    let searchTimeout = null;
    const handleSearch = (value) => {
      searchValue.value = value;
      emit('search', value);

      if (searchTimeout) {
        clearTimeout(searchTimeout);
      }

      searchTimeout = setTimeout(() => {
        // Additional debounced actions can be added here if needed
      }, 300);
    };

    // Handle change event
    const handleChange = (value, options) => {
      // value can be a single value or an array, depending on mode
      // options is an array of selected option objects

      // Check if any of the selected options is an "Add" option
      const addedOptions = options.filter(option => option.value.startsWith('__add__'));

      addedOptions.forEach(option => {
        const newOptionLabel = option.label.replace(/^Add\s*"|"$/g, '');
        const newOptionValue = newOptionLabel.toLowerCase().replace(/\s+/g, '_');

        emit('add', { label: newOptionLabel, value: newOptionValue });

        // Remove the "Add" option from the selected values
        // Assuming modelValue is an array or object
        // Need to adjust based on labelInValue and mode

        if (props.mode === 'multiple' || props.mode === 'tags') {
          const updatedValue = options.filter(opt => !opt.isAddOption).map(opt => opt.value);
          emit('update:modelValue', updatedValue);
        } else {
          emit('update:modelValue', null);
        }
      });

      emit('change', value, options);
    };

    // Handle selection of an option
    const handleSelect = (value, option) => {
      if (option.isAddOption) {
        const newOptionLabel = option.label.replace(/^Add\s*"|"$/g, '');
        const newOptionValue = newOptionLabel.toLowerCase().replace(/\s+/g, '_');
        emit('add', { label: newOptionLabel, value: newOptionValue });
      } else {
        emit('select', value, option);
      }

      // Update the modelValue if not "add" option
      if (!option.isAddOption) {
        emit('update:modelValue', props.modelValue);
      }
    };

    // Handle deselection of an option
    const handleDeselect = (value, option) => {
      emit('deselect', value, option);
      emit('update:modelValue', props.modelValue);
    };

    return {
      displayedOptions,
      handleSearch,
      handleSelect,
      handleDeselect,
      searchValue,
    };
  },
};
</script>


<style scoped>
.custom-option {
  padding: 8px 12px;
}

.add-option {
  background-color: #e6f7ff; /* Light blue background */
  font-weight: bold; /* Bold text */
  color: #1890ff; /* Ant Design's primary color */
}
</style>
