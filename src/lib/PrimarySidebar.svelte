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

    import { commandStore } from './store.js';


    function openPoem(id: string) {
        newPoem = false;
        currentPoem = poems[id];
        selectedPoemId = id;
    }

    function deletePoem(id: string) {
        fetch('http://127.0.0.1:8000/poems/' + id , {
            method: 'DELETE',
            headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
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
            let poem_str = `Date Published: 2022|Title:${currentPoem.name}|</s>`;
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
            console.log(commandStore.numTokens)
            if ($commandStore.numTokens && $commandStore.numTokens > 1) {
                response = await fetch(`http://127.0.0.1:8000/suggest_replacement_multi`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
                    },
                    body: JSON.stringify({poem_str}),
                });
            } else {
                response = await fetch(`http://127.0.0.1:8000/suggest_replacement`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Access-Control-Allow-Origin': '*',
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
        console.log("CALLED")
        commandStore.update(store => {
            store.command = 'loading';
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
                let req_url = `http://127.0.0.1:8000/synonyms?word=${selectedWord}`;
                if (lc) {
                    req_url += `&lc=${lc}`
                }
                if (rc) {
                    req_url += `&rc=${rc}`
                }
                let response = await fetch(req_url);
                if (response.ok) {
                    const data = await response.json();
                    console.log(data);
                    commandStore.set({ command: 'synonyms', selectedWord, synonyms: data });
                }
            } 
        }
    }

    let prev = 0;

    $: if ($commandStore.command === 'suggestions' && selectedWordIndex !== prev) {
        suggestReplacement();
        prev = selectedWordIndex;
    } else if ($commandStore.command === 'synonyms' && selectedWordIndex !== prev) {
        getSynonyms();
        prev = selectedWordIndex;
    }

</script>

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
                <span on:click={() => {selectedPoemId=null; createPoem}} class:bg-gray-200={sidebarMode === 'add'} class="material-symbols-sharp text-2xl mr-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:30px">add</span>
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
                {#if mode === 4}
                    <button class="flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={suggestReplacement}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 35px;">compare_arrows</span>
                        <span class="ml-2">Suggest Replacement</span>
                    </button>
                    <button class="flex items-center justify-center px-4 py-2 text-sm font-medium rounded-md hover:bg-gray-300 focus:outline-none transition duration-150 ease-in-out" on:click={getSynonyms}>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size: 28px;">autorenew</span>
                        <span class="ml-2">Get Synonyms</span>
                    </button>
                {/if}


  
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
        width: 250px;
    }
</style>