<script lang="ts">
    import { onDestroy, createEventDispatcher } from 'svelte';
    import { commandStore } from './store.ts';

    export let pSidebarOpen: boolean;

    const dispatch = createEventDispatcher();
    
    let suggestions = [];
    let synonyms = [];
    let rhymes = [];
    let selectedWord: string|null = null;
    let command: string|null = null;
    let numTokens = 1;

    let unsubscribe = commandStore.subscribe(value => {
        command = value.command;
        selectedWord = value.selectedWord;
        if (command === "suggestions") {
            if (Array.isArray(value.suggestions)) {
                suggestions = value.suggestions;
            } else {
                console.error('Invalid suggestions:', value.suggestions);
                suggestions = [];
            }
        } else if (command === "synonyms") {
            if (Array.isArray(value.synonyms)) {
                synonyms = value.synonyms;
            } else {
                console.error('Invalid synonyms:', value.synonyms);
                synonyms = [];
            }
        } else if (command === "rhymes") {
            if (Array.isArray(value.rhymes)) {
                rhymes = value.rhymes;
            } else {
                console.error('Invalid rhymes:', value.rhymes);
                rhymes = [];
            }
        }
    });

    function searchPoem(poem) {
        console.log(poem.author)
        const query = encodeURIComponent(`${poem.title.trim()} by ${poem.author.trim()}`);
        window.open(`https://www.google.com/search?q=${query}`, '_blank');
    }


    onDestroy(() => {
        unsubscribe();
    });

    $: {
        if (numTokens !== $commandStore.numTokens) {
            commandStore.update(store => ({...store, numTokens}));
            console.log("Updated")
            console.log($commandStore)
        }
    }
</script>

<div class="right-sidebar" class:open={pSidebarOpen && command}>
    {#if command === "generating" || (command === "rewriteLine" && !($commandStore.rewrites))}
        <h2 class="font-bold text-lg">Generating<span class="ellipsis-anim">.</span></h2>
        <h3 class="font-light">(may take a while)</h3>
    {:else if command === "error"}
        <h2 class="font-bold text-lg text-red-600">Error</h2>
    {:else if command === "suggestions"}
        <h2 class="font-bold text-lg">Word Suggestions</h2>
        <p class="selected-word">Selected Word: <span>{selectedWord}</span></p>
        <label>
            Number of tokens to generate (anything above 1 will only generate 1 suggestion):<br>
            <input class="mb-3 bg-gray-50" type="number" min="1" bind:value={numTokens}>
        </label>
        <div class="suggestions-list">
            {#if typeof suggestions[0] !== "string"}
                {#each suggestions as [suggestion, probability]}
                    <button class="suggestion-item" on:click={() => dispatch("replaceWord", {word:suggestion})}>
                        <p>Suggested Word: <span>{suggestion}</span></p>
                        <p>Probability: <span>{probability.toFixed(2)}</span></p>
                    </button>
                {/each}
            {:else}
                <p>Suggestion: {suggestions.join("")}</p>
            {/if}
        </div>
        <button class="revert-button" on:click={() => dispatch("replaceWord", {word:selectedWord})}>Revert</button>

    {:else if command === "synonyms"}
        <h2 class="font-bold text-lg">Synonyms</h2>
        <p class="selected-word">Selected Word: <span>{selectedWord}</span></p>
        <div class="suggestions-list">
            {#each synonyms as {word, score}}
                <button class="suggestion-item" on:click={() => dispatch("replaceWord", {word:word})}>
                    <p>Synonym: <span>{word}</span></p>
                    <p>Score: <span>{score}</span></p>
                </button>
            {/each}
        </div>
        <button class="revert-button" on:click={() => dispatch("replaceWord", {word:selectedWord})}>Revert</button>
    {:else if command === "rhymes"}
        <h2 class="font-bold text-lg">Rhymes</h2>
        <p class="selected-word">Selected Word: <span>{selectedWord}</span></p>
        <div class="suggestions-list">
            {#each rhymes as {word, score}}
                <button class="suggestion-item" on:click={() => dispatch("replaceWord", { word })}>
                    <p>Synonym: <span>{word}</span></p>
                    <p>Score: <span>{score}</span></p>
                </button>
            {/each}
        </div>
        <button class="revert-button" on:click={() => dispatch("replaceWord", {word:selectedWord})}>Revert</button>
    {:else if command === "feedback"}
        <h2 class="font-bold text-lg mb-2">Feedback</h2>
        <div class="bg-white shadow-sm text-sm rounded-md p-3 cursor-pointer">
            <p>{@html $commandStore.feedback.replace(/\n/g, '<br>')}</p>
        </div>
    {:else if command === "rewriteLine" && $commandStore.rewrites}
        <h2 class="font-bold text-lg mb-2">Rewrites</h2>
        <p class="selected-word">Original Line: <br><span>{$commandStore.line}</span></p>
        <div class="space-y-2">
            {#each $commandStore.rewrites as rewrite}
                <div class="bg-white shadow-sm text-sm rounded-md p-3">
                    <p class="font-bold mb-2">{rewrite}</p>
                </div>
            {/each}
        </div>
    {:else if command === "metaphor"}
        <h2 class="font-bold text-lg mb-2">Metaphor</h2>
        <p class="selected-word">Source: <span>{$commandStore.source}</span></p>
        <p class="selected-word">Target: <span>{$commandStore.target}</span></p>
        <h3 class="font-bold mb-2">Generated Metaphors:</h3>
        <div class="space-y-4">
            {#each $commandStore.metaphors as metaphor}
                <div class="bg-white shadow-sm font-medium text-sm rounded-md p-3">
                    <p>{metaphor}</p>
                </div>
            {/each}
        </div>
    {:else if command === "similarPoems"}
        <h2 class="font-bold text-lg mb-2">Similar Poems</h2>
        <div class="space-y-2">
            {#each $commandStore.similarPoems as poem, i}
                <div class="bg-white shadow-sm text-sm rounded-md p-3 cursor-pointer hover:bg-gray-100" on:click={() => searchPoem(poem)}>
                    <h3 class="font-bold mb-1">{poem.title}</h3>
                    <p class="text-gray-500 mb-2">By {poem.author}</p>
                    
                    <p class="text-gray-700 font-thin">
                    {#if poem.poem.length > 100}
                        {@html poem.poem.trim().substring(0, 100).replace(/\n/g, '<br>')}...
                        <br><span class="text-gray-400">Click to read more.</span>
                    {:else}
                        {@html poem.poem.replace(/\n/g, '<br>').trim()}
                    {/if}
                    </p>
                    <div class="flex justify-between">
                        <p class="selected-word">Score: <span>{Math.round($commandStore.scores[i]*10000)}</span></p>
                        <span class="material-symbols-sharp text-2xl mr-2 hover:scale-110 text-gray-600 hover:text-gray-700" style="font-size: 28px;">manage_search</span>
                    </div>
                </div>
            {/each}
        </div>
    {:else if command==="ideas"}
        <h2 class="font-bold text-lg mb-2">Idea Generation</h2>
        <div class="space-y-2">
            {#each $commandStore.ideas as idea}
                <div class="bg-white shadow-sm text-sm rounded-md p-3">
                    <p class="font-bold mb-2">{idea}</p>
                </div>
            {/each}
        </div>
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

    .ellipsis-anim:after {
        content: ".";
        animation: ellipsis 1s infinite;
    }

    @keyframes ellipsis {
        0%, 100% { content: ""; }
        33% { content: "."; }
        66% { content: ".."; }
    }

</style>
