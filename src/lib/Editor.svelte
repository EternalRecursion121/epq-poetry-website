<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
</script>

<div class="h-screen p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode===2}>
    <textarea class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden" bind:value={currentPoem.body} readonly={mode===2}></textarea>
</div> 
