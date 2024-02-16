<template>
  <v-file-input show-size :rules="rules" accept="application/pdf" placeholder="Pick a PDF file or drag and drop it here"
    prepend-icon="mdi-document" label="PDF input" density="compact"></v-file-input>
</template>

<script>
export default {
  name: "FileUploadCard",
  data: () => ({
    rules: [
      value => {
        return !value || !value.length || value[0].size < 5000000 || 'PDF size should be less than 5 MB!'
      },
    ],
  }),
}
</script>
