<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editordiv: null|HTMLDivElement = null;
    export let selectedWordIndex: number|null = null;

    let loaded = false;
    let selectedLine:string;

    import { onMount } from 'svelte';
    import { commandStore } from './store';

    export const replaceWord = (word) => {
        console.log(selectedWordIndex);
        if (selectedWordIndex !== null) {
            const spanElements = editordiv.querySelectorAll('span');
            const selectedWord = spanElements[selectedWordIndex];
            console.log(selectedWord.innerHTML);
            selectedWord.innerHTML = word;
        }
    }

    function setInnerHTML(newHTML: string) {
        editordiv.innerHTML = newHTML.replace(/\n/g, "<br>");
        if (mode === 4) {
            wrapWords();
        }
    }

    onMount(() => {
        loaded = true;
    });
    
    let prevBody = "";
    $: if (loaded) {
        console.log(currentPoem.body)
        if (currentPoem.body !== prevBody) {
            console.log(currentPoem.body)
            setInnerHTML(currentPoem.body);
            prevBody = currentPoem.body;
        }
    }

    function wrapWords() {
        unwrapWords();
        if ($commandStore.command === "rewriteLine") {
            // Match the entire line until a line break or the end of the string
            editordiv.innerHTML = editordiv.innerHTML.replace(/(.+?)(<br>|$)/g, '<span class="line">$1</span><br>');
        } else {
            // If it's not line mode, fall back to word mode
            editordiv.innerHTML = editordiv.innerHTML.replace(/(^|>|[\s]|&nbsp;)(([^<>\s&]|&(?!nbsp;))+)/g, '$1<span class="word">$2</span>');
        }
        currentPoem.body = editordiv?.innerText;
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
                if ($commandStore.command === "rewriteLine") {
                    commandStore.update(store => {
                        store.line = span.innerText;;
                        return store;
                    });
                } else {
                    selectedWordIndex = index;
                }
            });

            span.addEventListener('dblclick', (e) => {
                e.target.contentEditable = 'true';
                e.target.focus();
                e.target.classList.add('editing');
            });
            
            span.addEventListener('blur', (e) => {
                e.target.contentEditable = 'false';
                e.target.classList.remove('editing');
                replaceWord(e.target.innerHTML);
            });
        });
    }

    $: if (editordiv) {
        if ($commandStore.command === "rewriteLine" && mode === 4) {
            wrapWords();
        } else if (mode === 4) {
            wrapWords();
        } else {
            unwrapWords();
        }
    } 

</script>

<div class="p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode === 2}>
    <div class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden font-sans editordiv min-h-400" bind:this={editordiv} contenteditable={mode!==2 && mode!==4} ></div>
</div>

<style lang="postcss">
    .editordiv :global(.word), .editordiv :global(.line) {
        @apply border border-gray-700 px-2 my-1 bg-black bg-opacity-0 cursor-pointer;
    }

    .editordiv :global(.word:not(.selected)), .editordiv :global(.line:not(.selected)) {
        @apply hover:hover:bg-opacity-10;
    }

    .editordiv :global(.word) {
        @apply border border-gray-700 px-2 my-1 bg-black bg-opacity-0 cursor-pointer;
    }
    .editordiv :global(.div) {
        @apply border border-gray-700 px-2 my-1 bg-black bg-opacity-0 cursor-pointer;
    }

    .editordiv :global(.word:not(.selected)) {
        @apply hover:hover:bg-opacity-10;
    }
    .editordiv :global(.selected) {
        @apply bg-gray-600 text-white;
    }

    .editordiv :global(.editing) {
        @apply bg-gray-200 text-black border-none;
    }
</style>
