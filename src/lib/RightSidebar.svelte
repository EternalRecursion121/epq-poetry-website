<script lang="ts">
    export let command: string;

    import { onMount } from "svelte";

    let suggestions: Array<[string, number]> = [];
    let selectedWord: string|null = null;

    const updateSuggestions = (event) => {
        selectedWord = event.detail.selectedWord;
        suggestions = event.detail.suggestions;
    }

    onMount(() => {
        window.addEventListener('suggestions', updateSuggestions);
        return () => {
            window.removeEventListener('suggestions', updateSuggestions);
        }
    });
</script>

<div class="right-sidebar">
    <h2>Word Suggestions</h2>
    <p>Selected Word: {selectedWord}</p>
    <div class="suggestions-list">
        {#each suggestions as [suggestion, probability]}
            <div class="suggestion-item">
                <p>Suggested Word: {suggestion}</p>
                <p>Probability: {probability}</p>
            </div>
        {/each}
    </div>
</div>

<style lang="postcss">
    .right-sidebar {
        @apply border-l border-gray-400;
        position: fixed;
        right: 0;
        width: 250px;
        height: 100%;
        padding: 20px;
    }

    .suggestions-list {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }

    .suggestion-item {
        border: 1px solid gray;
        border-radius: 5px;
        padding: 10px;
    }
</style>