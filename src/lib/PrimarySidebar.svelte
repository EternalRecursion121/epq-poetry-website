<script lang="ts">
    export let open: boolean;
    export let mode: number;
    export let selectedPoemId: string|null;
    export let poems: Record<string, Object>;
    export let sidebarMode = 'files';
    export let createPoem: Function;
    export let savePoem: Function;
    export let newPoem: boolean;
    export let currentPoem: Object;
    export let selectedWordIndex: number|null;

    import { commandStore } from './store.ts';
    import { env } from '$env/dynamic/public';
    import params from './params.json';
    import { onMount, onDestroy } from 'svelte';
    import MetaphorModal from './MetaphorModal.svelte';

    let showModal = false;

    let search = '';
    let searchPoet = '';
    
    let visibleThemes = params.themes;
    params.poets.sort();

    let visiblePoets:Array<string> = [];
    let maxSuggestions = 10;

    onMount(() => {
        updateVisibleThemes();
        updateVisiblePoets();
    });

    function updateVisiblePoets() {
        if(searchPoet === '') {
            visiblePoets = [];
        } else {
            visiblePoets = params.poets.filter(poet => poet.toLowerCase().includes(searchPoet.toLowerCase())).slice(0, maxSuggestions);
        }
    }


    function updateVisibleThemes() {
        if(search === '') {
            visibleThemes = params.themes;
        } else {
            visibleThemes = params.themes.filter(theme => theme.includes(search));
        }
    }

    function toggleTheme(theme) {
        const index = currentPoem.themes.indexOf(theme);

        if(index >= 0) {
            currentPoem.themes.splice(index, 1);
        } else {
            currentPoem.themes.push(theme);
        }
    }


    function openPoem(id: string) {
        console.log("POEMS", poems)
        newPoem = false;
        currentPoem = { ...poems[id] };
        selectedPoemId = id;
        console.log(poems)
        console.log("openPoem", id, poems[id]);
    }

    function deletePoem(id: string) {
        fetch(`${env.PUBLIC_SERVER_URL}/poems/` + id , {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            "ngrok-skip-browser-warning": "true"
            }
        }).then(res => {
            if (res.ok) {
                delete poems[id];
                poems = { ...poems };
                selectedPoemId = '';
            }
        });
    }

    async function suggestReplacement() {
        commandStore.update(store => {
            store.command = 'loading';
            return store;
        });
        if (selectedPoemId) {
            // Create a RegExp to match any kind of whitespace or non-whitespace (words)
            let matches = currentPoem.body.match(/(\s+|\S+)/g);


            let selectedWord;
            let i = 0;
            let poem_str = `Date Published: ${currentPoem.year}`
            if (currentPoem.poet) {
                poem_str += `|Author:${currentPoem.poet}|`;
            }
            poem_str += `|Title:${currentPoem.name}`;
            if (currentPoem.form) {
                poem_str += `|Forms:${currentPoem.form}`;
            }
            if (currentPoem.themes) {
                poem_str += `|Themes:${currentPoem.themes.join(', ')}`;
            }
            poem_str += "|</s>";
            if (matches) {
                for (const match of matches) {
                    if (/\S/.test(match)) { // If the match is not whitespace (i.e., it's a word)
                        if (i === selectedWordIndex) {
                            selectedWord = match;
                            poem_str += '<mask>'.repeat($commandStore.numTokens||1);
                        } else {
                            poem_str += match;
                        }
                        i++;
                    } else { // If the match is whitespace
                        poem_str += match;
                    }
                }
            }

            if (!selectedWord) {
                poem_str += '<mask>'.repeat($commandStore.numTokens||1);
            }
            let response;
            if ($commandStore.numTokens && $commandStore.numTokens > 1) {
                response = await fetch(`${env.PUBLIC_SERVER_URL}/suggest_replacement_multi`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "ngrok-skip-browser-warning": "true",
                    },
                    body: JSON.stringify({poem_str}),
                });
            } else {
                response = await fetch(`${env.PUBLIC_SERVER_URL}/suggest_replacement`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "ngrok-skip-browser-warning": "true",
                    },
                    body: JSON.stringify({poem_str}),
                });
            }
            if (response.ok) {
                const data = await response.json();
                console.log(data);
                commandStore.set({ command: 'suggestions', selectedWord, suggestions:data.suggestions });
            }
        }
    }


    async function getSynonyms() {
        commandStore.update(store => {
            store.command = 'generating';
            return store;
        });
        if (selectedPoemId) {
            let matches = currentPoem.body.match(/(\s+|\S+)/g);
            let selectedWord;
            let lc;
            let rc;
            let i = 0;
            if (matches) {
                for (const match of matches) {
                    if (/\S/.test(match)) { // If the match is not whitespace (i.e., it's a word)
                        if (i === selectedWordIndex - 1) {
                            lc = match.replace(/[^a-zA-Z]/g, '');
                        } else if (i === selectedWordIndex) {
                            selectedWord = match.replace(/[^a-zA-Z]/g, '');
                        } else if (i === selectedWordIndex + 1) {
                            rc = match.replace(/[^a-zA-Z]/g, '');
                            break;
                        }
                        i++;
                    }
                }
            }
            console.log("SELECTED_WORD")

            if (selectedWord) {
                let req_url = `${env.PUBLIC_SERVER_URL}/synonyms?word=${selectedWord}`;
                if (lc) {
                    req_url += `&lc=${lc}`
                }
                if (rc) {
                    req_url += `&rc=${rc}`
                }
                let response = await fetch(req_url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "ngrok-skip-browser-warning": "true",
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    commandStore.set({ command: 'synonyms', selectedWord, synonyms: data });
                }
            } 
        }
    }

    async function getRhymes() {
        commandStore.update(store => {
            store.command = 'generating';
            return store;
        });
        if (selectedPoemId) {
            let matches = currentPoem.body.match(/(\s+|\S+)/g);
            let selectedWord;
            let lc;
            let rc;
            let i = 0;
            if (matches) {
                for (const match of matches) {
                    if (/\S/.test(match)) { // If the match is not whitespace (i.e., it's a word)
                        if (i === selectedWordIndex - 1) {
                            lc = match.replace(/[^a-zA-Z]/g, '');
                        } else if (i === selectedWordIndex) {
                            selectedWord = match.replace(/[^a-zA-Z]/g, '');
                        } else if (i === selectedWordIndex + 1) {
                            rc = match.replace(/[^a-zA-Z]/g, '');
                            break;
                        }
                        i++;
                    }
                }
            }

            if (selectedWord) {
                let req_url = `${env.PUBLIC_SERVER_URL}/rhymes?word=${selectedWord}`;
                if (lc) {
                    req_url += `&lc=${lc}`
                }
                if (rc) {
                    req_url += `&rc=${rc}`
                }
                let response = await fetch(req_url, {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "ngrok-skip-browser-warning": "true",
                    },
                });
                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    commandStore.set({ command: 'rhymes', selectedWord, rhymes: data });
                }
            } 
        }
    }

    async function getFeedback() {
        console.log("GETTING FEEDBACK");
        commandStore.update(store => {
            store.command = 'generating';
            return store;
        });

        let response = await fetch(`${env.PUBLIC_SERVER_URL}/feedback`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "ngrok-skip-browser-warning": "true",
            },
            body: JSON.stringify(currentPoem),
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            commandStore.set({ command: 'feedback', feedback: data.feedback });
        }
    }

    async function metaphor(e) {
        showModal = false;
        const source = e.detail.source;
        const target = e.detail.target;
        commandStore.update(store => {
            store.command = 'generating';
            return store;
        });

        let response = await fetch(`${env.PUBLIC_SERVER_URL}/metaphors`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                "ngrok-skip-browser-warning": "true",
            },
            body: JSON.stringify({ "poem": currentPoem, source, target }),
        });

        if (response.ok) {
            const data = await response.json();
            console.log(data);
            commandStore.set({ command: 'metaphor', source, target, ...data });
        }
    }

    let prev = 0;

    $: if (selectedWordIndex !== prev) {
        if ($commandStore.command === 'suggestions') {
            suggestReplacement();
        } else if ($commandStore.command === 'synonyms') {
            getSynonyms();
        } else if ($commandStore.command === 'rhymes') {
            getRhymes();
        }
        prev = selectedWordIndex;
    }

    function getLineRewrite() {
        commandStore.update(store => {
            store.command = 'rewriteLine';
            return store;
        });
        const unsubscribe = commandStore.subscribe(async value => {
            if (value.line) {
                console.log({poem: currentPoem, line: value.line});
                let response = await fetch(`${env.PUBLIC_SERVER_URL}/rewrite_line`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                        "ngrok-skip-browser-warning": "true"
                    },
                    body: JSON.stringify({poem: currentPoem, line: value.line}),
                });
                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    commandStore.set({ command: 'rewriteLine', line: value.line, rewrites: data.rewrite });
                }
                unsubscribe();
            }
        });
    }



</script>

{#if showModal}
    <MetaphorModal on:close={() => showModal = false} on:metaphor={metaphor}/>
{/if}

<div class="sidebar" class:open>
    <div class="flex flex-col border-r items-center border-gray-400 w-[65px] h-full fixed">
        <span class:-scale-x-100={!open} class="transition-transform duration-300 ease-in-out justify-start material-symbols-sharp hover:cursor-pointer w-10 h-10 rounded-full mt-5" style="font-size:40px" on:click={()=>{open=!open}}>chevron_left</span>
        
        <div class:bg-[#FFE08D]="{mode === 1}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center mt-auto" on:click={()=>{mode=1}}>
            <span class='material-symbols-sharp' style="font-size:33px">lightbulb</span>
        </div>
        
        <div class:bg-[#7FB2F0]="{mode === 2}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center" on:click={()=>{mode=2}}>
            <span class="material-symbols-sharp" style="font-size:30px">visibility</span>
        </div>

        <div class:bg-[#B1D8B7]="{mode === 3}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center" on:click={()=>{mode=3}}>
            <span class="material-symbols-sharp" style="font-size:33px">edit</span>
        </div>

        <div class:bg-[#ED8C9C]="{mode === 4}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center mb-10" on:click={()=>{mode=4}}>
            <span class="material-symbols-sharp mb-1" style="font-size:28px">edit_square</span>
        </div>
   </div>
   {#if open}
   <div class="ml-[65px] h-full py-7 flex flex-col justify-between">
        <div class="flex flex-col">
            <div class="flex flex-row justify-between items-center">
                <span on:click={() => {sidebarMode = 'files'}} class:bg-gray-200={sidebarMode === 'files'} class="material-symbols-sharp text-2xl ml-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:30px">folder</span>
                <span on:click={() => {sidebarMode = 'command'}} class:bg-gray-200={sidebarMode === 'command'} class="material-symbols-sharp text-2xl ml-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:29px">keyboard_command_key</span>
                <span on:click={() => {sidebarMode = 'params'}} class:bg-gray-200={sidebarMode === 'poemParams'} class="material-symbols-sharp text-2xl ml-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:30px">tune</span>
                <span on:click={() => {selectedPoemId=null; createPoem()}} class:bg-gray-200={sidebarMode === 'add'} class="material-symbols-sharp text-2xl mr-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:30px">add</span>
            </div>
            {#if sidebarMode === 'files'}
                <div class="flex flex-col my-2">
                    {#each Object.entries(poems) as [id, poem]}
                        <button class:bg-gray-200={id === selectedPoemId} class="flex flex-row justify-between items-center py-1 hover:bg-gray-200" on:click={()=>{openPoem(id)}}>
                            <span class="material-symbols-sharp text-2xl ml-2" style="font-size:30px">insert_drive_file</span>
                            <span>{poem.name}</span>
                            <span id="deleteButton" class="material-symbols-sharp text-2xl mr-2 " style="font-size:24px" on:click|stopPropagation={()=>{deletePoem(id)}}>delete</span>
                        </button>
                    {/each}
                </div>
            {:else if sidebarMode === 'command'}
                {#if mode === 1}
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getFeedback}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 28px;">manage_search</span>
                        <span class="ml-2">Similar Poems</span>
                    </button>
                {:else if mode === 2}
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getFeedback}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 28px;">assistant</span>
                        <span class="ml-2">Get Feedback</span>
                    </button>
                {:else if mode == 3}
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={() => {showModal=true}}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 27px;">hub</span>
                        <span class="ml-2">Metaphor</span>
                    </button>
                {:else if mode === 4}
                    <button class="flex items-center px-4 text-md py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={suggestReplacement}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 35px;">compare_arrows</span>
                        <span class="ml-2">Get Replacement</span>
                    </button>
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getSynonyms}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 28px;">autorenew</span>
                        <span class="ml-2">Get Synonyms</span>
                    </button>
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getRhymes}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 28px;">music_note</span>
                        <span class="ml-2">Get Rhymes</span>
                    </button>
                    <button class="flex items-center px-4 py-2 font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getLineRewrite}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 25px;">edit_note</span>
                        <span class="ml-2">Rewrite Line</span>
                    </button>
                {/if}
            {:else if sidebarMode === 'params'}
                <div class="space-y-4 mx-3">
                    <div>
                        <label for="year" class="block text-sm font-medium text-gray-700">Year: </label>
                        <input id="year" type="number" bind:value={currentPoem.year} min="1" max="9999" class="mt-1 block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                    </div>
                    <div>
                        <label for="themes" class="block text-sm font-medium text-gray-700">Themes: </label>
                        <input class="mt-1 block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" type="text" bind:value={search} on:input={updateVisibleThemes} placeholder="Search themes..." />
                    
                        <div class="dropdown mt-2 px-2 rounded-sm">
                            {#each visibleThemes as theme (theme)}
                                <div>
                                    <input type="checkbox" id={theme} checked={currentPoem.themes.includes(theme)} on:change={() => toggleTheme(theme)}>
                                    <label for={theme} class="ml-2">{theme}</label>
                                </div>
                            {/each}
                        </div>
                    </div>
                    <div>
                        <label for="form" class="block text-sm font-medium text-gray-700">Form (Optional): </label>
                        <select id="form" bind:value={currentPoem.form} class="mt-1 block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm">
                            <option value="">-- Select a form --</option>
                            {#each params.forms as form}
                                <option value={form}>{form}</option>
                            {/each}
                        </select>
                    </div>
                    <div>
                        <label for="poet" class="block text-sm font-medium text-gray-700">Poet (Optional): </label>
                        <input class="mt-1 block w-full py-1 px-2 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm" type="text" bind:value={searchPoet} on:input={updateVisiblePoets} placeholder="Search poets..." />

                        {#each visiblePoets as poet (poet)}
                            <div>
                                <input class="border-1 border max-h-[200px] overflow-y-auto" type="radio" id={poet} bind:group={currentPoem.poet} value={poet}>
                                <label for={poet}>{poet}</label>
                            </div>
                        {/each}
                    </div>
                </div>
            {/if}
        </div>

        <button class="flex flex-row justify-between px-5 py-3 hover:bg-gray-200 rounded" on:click={savePoem}>
            <span class="text-lg">Save</span>
            <span class="material-symbols-sharp text-2xl" style="font-size:32px">save</span>
        </button>
    </div>

    {/if}

</div>

<style lang="postcss">
    .sidebar {
        @apply border-r border-gray-400;
        position: fixed;
        width: 65px;
        height: 100%;
        transition: all 0.5s; }

    .sidebar.open {
        width: 300px;
    }

    .dropdown {
        border: 1px solid #ccc;
        max-height: 200px;
        overflow-y: auto;
    }
</style>