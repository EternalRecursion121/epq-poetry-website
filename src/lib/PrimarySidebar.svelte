<script lang="ts">
    export let open: boolean;
    export let mode: number;
    export let selectedPoemId: string;
    export let poems: Record<string, Object>;
    export let sidebarMode = 'files';
    export let createPoem: Function;
    export let savePoem: Function;
    export let newPoem: boolean;
    export let currentPoem: Object;

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
                poems = poems;
                selectedPoemId = '';
            }
        });
    }

</script>

<svelte:head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@48,400,0,0" />
</svelte:head>

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
                <span on:click={createPoem} class:bg-gray-200={sidebarMode === 'add'} class="material-symbols-sharp text-2xl mr-2 px-2 py-1 rounded-md hover:bg-gray-300 hover:cursor-pointer" style="font-size:30px">add</span>
            </div>
            {#if sidebarMode === 'files'}
            <div class="flex flex-col my-2">
                {#each Object.entries(poems) as [id, poem]}
                    <button class:bg-gray-200={id === selectedPoemId} class="flex flex-row justify-between items-center py-1 hover:bg-gray-200" on:click={()=>{openPoem(id)}}>
                        <span class="material-symbols-sharp text-2xl ml-2" style="font-size:30px">insert_drive_file</span>
                        <span class="text-lg">{poem.name}</span>
                        <span id="deleteButton" class="material-symbols-sharp text-2xl mr-2 " style="font-size:24px" on:click|stopPropagation={()=>{deletePoem(id)}}>delete</span>
                    </button>
                {/each}
            </div>
            {:else if sidebarMode === 'command'}
  
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