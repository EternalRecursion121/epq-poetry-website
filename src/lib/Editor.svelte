<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editordiv: null|HTMLDivElement = null;
    let loaded = false;

    import { onMount } from 'svelte';

    function setInnerHTML(newHTML: string) {
        editordiv.innerHTML = newHTML.replace(/\n/g, "<br>");
        if (mode === 4) {
            wrapWords();
        }
    }

    onMount(() => {
        loaded = true;
    });
    
    $: if (loaded) {
        setInnerHTML(currentPoem.body);
    }

    function wrapWords() {
        unwrapWords();
        editordiv.innerHTML = editordiv.innerHTML.replace(/(^|>|[\s]+)(([^<>\s&]|&(?!nbsp;))+)/g, '$1<span class="word">$2</span>');
        editordiv.innerHTML = editordiv.innerHTML;
        addEventListenersToSpans();
    }

    function unwrapWords() {
        editordiv.innerHTML = editordiv.innerHTML.replace(/<\/?span[^>]*>/g, '');
    }

    function addEventListenersToSpans() {
        const spanElements = editordiv.querySelectorAll('span');

        spanElements.forEach((span) => {
            span.addEventListener('click', (e) => {
                console.log('Clicked:', e.target);
                // Add your custom logic for when the span is clicked
            });
        });
    }

    $: if (editordiv) {
        console.log(mode)
        if (mode === 4) {
            wrapWords();
        } else {
            unwrapWords();
            console.log("unwrapped")
        }
    } 

</script>

<div class="h-screen p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode === 2}>
    <div class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden font-sans editordiv" bind:this={editordiv} contenteditable={mode!==2 && mode!==4}></div>
    
</div>

<style lang="postcss">
    .editordiv :global(.word) {
        @apply border px-1 border-gray-700 bg-black bg-opacity-0 hover:bg-opacity-10 cursor-pointer;
    }
</style>
