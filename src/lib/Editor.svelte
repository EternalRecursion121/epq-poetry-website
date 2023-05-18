<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editordiv: null|HTMLDivElement = null;
    export let selectedWordIndex: number|null = null;

    let loaded = false;

    import { onMount, createEventDispatcher } from 'svelte';

    const dispatch = createEventDispatcher();

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

        spanElements.forEach((span, index) => {
            span.addEventListener('click', (e) => {
                spanElements.forEach((span) => span.classList.remove('selected')); // Remove the class from all words
                span.classList.add('selected'); // Add the class to the selected word
                selectedWordIndex = index;
                dispatch('wordSelected', { index });
            });
        });
    }

    $: if (editordiv) {
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
        @apply border border-gray-700 px-2 my-1 bg-black bg-opacity-0 cursor-pointer;
    }

    .editordiv :global(.word:not(.selected)) {
        @apply hover:hover:bg-opacity-10;
    }
    .editordiv :global(.selected) {
        @apply bg-gray-600 text-white;
    }
</style>
