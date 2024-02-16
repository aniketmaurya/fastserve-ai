<template>
  <v-card>
    <v-card-title>ChatBot</v-card-title>
    <v-card-text>
      <v-list>
        <v-list-item v-for="message in messages" :key="message.id">
          <v-list-item-content>
            <v-list-item-title v-text="message.text"></v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-text-field v-model="newMessage" label="Type a message" @keyup.enter="sendMessage"></v-text-field>
      <v-btn color="primary" @click="sendMessage">Send</v-btn>
    </v-card-actions>
  </v-card>
</template>

<script>
import FileUploadCard from './FileUpload.vue';

export default {
  data() {
    return {
      messages: [],
      newMessage: ""
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage) {
        this.messages.push({ id: Date.now(), text: this.newMessage });
        this.newMessage = "";
      }
    }
  }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
