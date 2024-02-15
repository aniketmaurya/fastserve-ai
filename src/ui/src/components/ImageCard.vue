<template>
    <div class="flex justify-center items-center h-screen">
        <div class="w-auto h-auto rounded-md border">
            <img :src="imagePath" alt="Generated Image" class="h-full w-full rounded-t-md object-cover" />
            <div class="p-4">
                <div class="w-full">
                    <input v-model="inputPrompt"
                        class="flex h-10 w-full rounded-md border border-black/30 bg-transparent px-3 py-2 text-sm placeholder:text-gray-600 focus:outline-none focus:ring-1 focus:ring-black/30 focus:ring-offset-1 disabled:cursor-not-allowed disabled:opacity-50"
                        type="text" placeholder="Image prompt"/>
                </div>

                <button type="button" @click="generateImage()"
                    class="mt-4 w-full rounded-sm bg-black px-2 py-1.5 text-sm font-semibold text-white shadow-sm hover:bg-black/80 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-black">
                    Generate
                </button>
            </div>
        </div>
    </div>
</template>

<script>
import sampleImageSrc from '../assets/sdxl-turbo.jpeg';


export default {
    name: "ImageCard",
    data() {
        return {
            imagePath: sampleImageSrc,
            inputPrompt: "dog in a frosty background, puppy eyes, cute, full of lights, 8K"
        }
    },
    methods: {
        generateImage() {
            if (this.inputPrompt.length > 1) {
                this.postRequest(this.inputPrompt);
            }
        },
        async postRequest(newPrompt) {
            try {
                const response = await fetch('http://127.0.0.1:8000/endpoint', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        // Add any additional headers if needed
                    },
                    body: JSON.stringify({
                        // Your request payload goes here
                        prompt: newPrompt,
                        negative_prompt: 'ugly, blurry, poor quality',
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                // Assuming the response is an image, convert it to a data URL
                const responseDataUrl = await response.blob().then((blob) =>
                    URL.createObjectURL(blob)
                );

                this.imagePath = responseDataUrl;
                return responseDataUrl
            } catch (error) {
                console.error('Error fetching data:', error);
                // Handle error appropriately (e.g., show an error message to the user)
            }
        }
    }
}
</script>
