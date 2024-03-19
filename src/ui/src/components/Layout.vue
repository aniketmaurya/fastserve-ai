<template>
    <v-layout>
      <v-app-bar density="default" prominent>
        <template v-slot:prepend>
          <v-app-bar-nav-icon variant="text" @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
        </template>

        <v-app-bar-title>FastServe</v-app-bar-title>
        <v-spacer></v-spacer>
      </v-app-bar>

      <v-navigation-drawer>
        <v-list-item link title="Applications" subtitle="Vuetify"></v-list-item>
        <v-divider></v-divider>
        <v-list-item link title="Image Generation" @click="handleNavItemSelect('Image Generation')"></v-list-item>
        <v-list-item link title="Chat with PDF" @click="handleNavItemSelect('Chat with PDF')"></v-list-item>
      </v-navigation-drawer>

      <v-main>
        <v-card fluid>
          <template v-if="selectedNavItem === 'Image Generation'">
            <ImageCard />
          </template>
          <template v-else-if="selectedNavItem === 'Chat with PDF'">
            <!-- Add your code for Chat with PDF component here -->
            <ChatBot />
          </template>
        </v-card>
      </v-main>
    </v-layout>
  </template>

<script>
    import ImageCard from './ImageCard.vue';
    import ChatBot from './ChatBot.vue';

    export default {
        name: "Layout",
        components: {
            ImageCard,
            ChatBot
        },
        data() {
            return {
                drawer: false,
                selectedNavItem: "Image Generation",
            };
        },
        methods: {
            handleNavItemSelect(item) {
                this.selectedNavItem = item;
            },
        },
    }
</script>