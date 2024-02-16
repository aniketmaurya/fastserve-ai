<template>
  <v-card>
    <v-card-title>Chat with PDF</v-card-title>
    <v-card-text>
      <v-list lines="three">
        <v-list-item v-for="message in messages" :key="message.id" :value="message" rounded="xl">
          <v-list-item-content>
            <div>
              <v-chip>🙋‍♂️ {{ message.user }}</v-chip><br><br>
              <v-chip>🤖 {{ message.bot }}</v-chip>
            </div>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-text-field v-model="newMessage" label="Type a message" @keyup.enter="sendMessage"></v-text-field>
      <v-btn color="primary" @click="sendMessage">Send</v-btn>
      <FileUploadCard />
    </v-card-actions>
  </v-card>
</template>

<script>
import FileUploadCard from './FileUpload.vue';
export default {
  name: "ChatBot",
  components: {
    FileUploadCard
  },
  data() {
    return {
      messages: [],
      newMessage: "Hey there!"
    };
  },
  methods: {
    sendMessage() {
      if (this.newMessage) {
        this.messages.push({ user: this.newMessage, bot: "Generated chatbot msg" });
        this.newMessage = "";
      }
    }
  }
};
</script>

<style scoped>
/* Add your custom styles here */
</style>
