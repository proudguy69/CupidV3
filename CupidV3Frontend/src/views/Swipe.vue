<template>
    <div class="container mx-auto">
        <v-card width="400">
            <v-img
                src="https://cdn.discordapp.com/banners/1267552151454875751/b8aeb5cee79f6728ab89f5521b891ad4.webp?size=512"
                cover
                class="text-white">

                <v-card-title>
                    <div class="card-title">
                        <img class="icon" src="https://cdn.discordapp.com/avatars/1267552151454875751/9bf9a1155e9640ba12a48a7df00131f7.png?size=512"></img>
                        <span class="name">Oliver</span>
                    </div>
                    <v-chip>20</v-chip>
                    <v-chip class="ml-3">Male</v-chip>
                    <v-chip class="ml-3">He/Him</v-chip>
                    <v-chip class="ml-3">Heterosexual</v-chip>
                    
                </v-card-title>
            </v-img>
            
            <v-card-text>
                orangegreencat
            </v-card-text>
            
            <v-card-text>
                I’m 20, going to the Air Force in February. No I do not believe in killing people or war, in fact I’m anti war, it’s just a way better place to be In terms of money (they litteraly pay for your home, like free housing? Hell yeah) I’ll be doing cyber sec
                <br> <br>
                I’m a programmer i love to code. Huge big time yapper btw. I love to call and talk to people. I’m not on discord much anymore tho.
                I’m currently a manager of a car wash. I love space and the galaxy as well as aviation. I love photography and I take LOTS of photos too.. so feel free to ask to see them
                saving this for later
            </v-card-text>
        <div class="buttons">
            <v-btn variant="tonal" class="bg-error"><- Reject</v-btn>
            <v-btn variant="tonal" class="bg-success">Match -></v-btn>
        </div>
        
        </v-card>
    </div>
    
</template>

<script setup>

</script>

<style scoped>

.buttons {
    display: flex;
    justify-content: space-between;
    padding: 1rem;
}

.icon {
    height: 48px;
    border-radius: 100px;
}

.card-title {
    display: flex;
    align-items: center;
    gap: 0.25rem;
    margin-bottom: 4px;
}

.container {
    margin-top: 8rem;
}

.v-chip {
  background-color: rgba(0, 0, 0, 0.85) !important; /* Less transparent */
  color: white !important;
}

.name {
    padding-left: 6px;
    padding-right: 6px;
    background-color: rgba(0, 0, 0, 0.65);
    border-radius: 10px;
}

</style>