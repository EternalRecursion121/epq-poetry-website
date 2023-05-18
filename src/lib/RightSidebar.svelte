<script lang="ts">
    import { onDestroy, createEventDispatcher } from 'svelte';
    import { commandStore } from './store.js';

    export let pSidebarOpen: boolean;

    const dispatch = createEventDispatcher();
    
    let suggestions = [];
    let selectedWord: string|null = null;
    let command: string|null = null;
    let numTokens = 1;

    let unsubscribe = commandStore.subscribe(value => {
        command = value.command;
        selectedWord = value.selectedWord;
        if (Array.isArray(value.suggestions)) {
            suggestions = value.suggestions;
        } else {
            console.error('Invalid suggestions:', value.suggestions);
            suggestions = [];
        }
    });


    onDestroy(() => {
        unsubscribe();
    });

    $: commandStore.set({ ...$commandStore, numTokens: numTokens });
</script>

<div class="right-sidebar" class:open={pSidebarOpen && command}>
    {#if command === "generating"}
        <h2 class="font-bold text-lg">Generating...</h2>
    {:else if command === "error"}
        <h2 class="font-bold text-lg">Error</h2>
        <p>{selectedWord}</p>
    {:else if command === "suggestions"}
        <h2 class="font-bold text-lg">Word Suggestions</h2>
        <p class="selected-word">Selected Word: <span>{selectedWord}</span></p>
        <label>
            Number of tokens to generate:<br>
            <input class="mb-3 bg-gray-50" type="number" min="1" bind:value={numTokens}>
        </label>
        <div class="suggestions-list">
            {#each suggestions as [suggestion, probability]}
                <button class="suggestion-item" on:click={() => dispatch("replaceWord", {word:suggestion})}>
                    <p>Suggested Word: <span>{suggestion}</span></p>
                    <p>Probability: <span>{probability.toFixed(2)}</span></p>
                </button>
            {/each}
        </div>
        <button class="revert-button" on:click={() => dispatch("replaceWord", {word:selectedWord})}>Revert</button>
    {/if}
</div>

<style lang="postcss">
    .right-sidebar {
        @apply border-l border-gray-400 bg-gray-100 text-gray-700;
        position: fixed;
        right: 0;
        top: 0;
        width: 350px;
        height: 100%;
        padding: 20px;
        overflow-y: auto;
        transform: translateX(100%);
        transition: all 0.4s ease;
    }

    .right-sidebar.open {
        @apply transform-none;
    }

    .selected-word {
        @apply font-medium mb-3;
    }

    .selected-word span {
        @apply font-bold text-blue-600;
    }

    .suggestions-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .suggestion-item {
        @apply bg-white shadow-sm rounded-md p-3 cursor-pointer;
        transition: all 0.3s ease;
    }

    .suggestion-item:hover {
        @apply shadow-lg transform bg-gray-200;
    }

    .suggestion-item p {
        @apply mb-1;
    }

    .suggestion-item p:last-child {
        @apply mb-0;
    }

    .suggestion-item span {
        @apply font-semibold;
    }

    .revert-button {
        @apply bg-blue-500 text-white px-3 py-1 rounded my-4 cursor-pointer;
        transition: all 0.3s ease;
    }

    .revert-button:hover {
        @apply bg-blue-600;
    }
</style>
