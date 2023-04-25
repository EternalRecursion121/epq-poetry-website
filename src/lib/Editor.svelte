<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editordiv: null|HTMLDivElement = null;
    
    import { onMount } from "svelte";

    onMount(() => {
        editordiv.innerHTML = currentPoem.body;
    });

    $: console.log(currentPoem.body)

    $: if (editordiv && mode === 4) {
        editordiv.innerHTML = editordiv.innerHTML.replace(/<\/?span[^>]*>/g, '');
        editordiv.innerHTML = editordiv.innerHTML.replace(/(^|>|[\s]+)([^<>\s]+)([\s]+|<|$)/g, '$1<span class="hi">$2</span>$3');
        editordiv.innerHTML = editordiv.innerHTML
    }

</script>

<div class="h-screen p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode === 2 || mode === 4}>
    <div class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden font-sans" bind:this={editordiv} contenteditable={mode!==2}></div>
</div>

<style lang="postcss">
    .hi {
        background-color: #961e1e;
        @apply border;
        border-radius: 4px;
        padding: 0 4px;
    }
</style>
