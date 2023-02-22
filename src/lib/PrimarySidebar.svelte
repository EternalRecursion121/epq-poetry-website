<script lang="ts">
    export let open: boolean;
    export let savedFiles:Array<Record<string, string>> = [];
    export let mode: number;
    export let poems: Array<Object> = [];
</script>

<svelte:head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@48,400,0,0" />
</svelte:head>

<div class="sidebar" class:open>
    <div class="flex flex-col border-r items-center border-gray-400 w-[65px] h-full fixed">
        <span class:-scale-x-100={!open} class="transition-transform duration-300 ease-in-out justify-start material-symbols-sharp hover:cursor-pointer w-10 h-10 rounded-full mt-5" style="font-size:40px" on:click={()=>{open=!open}}>chevron_left</span>

        
        <div class:bg-[#FFE08D]="{mode === 1}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center mt-auto" on:click={()=>{mode=1}}>
            <span class="material-symbols-sharp" style="font-size:33px">lightbulb</span>
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
    <div class="ml-[65px] py-7">
        <div class="flex flex-col">
            <div class="flex flex-row justify-between items-center">
                <span class="material-symbols-sharp text-2xl ml-2" style="font-size:30px">folder</span>
                <span class="material-symbols-sharp text-2xl mr-2" style="font-size:30px">add</span>
            </div>
            <div class="flex flex-col">
                {#each poems as poem}
                    <div class="flex flex-row justify-between items-center">
                        <span class="material-symbols-sharp text-2xl ml-2" style="font-size:30px">insert_drive_file</span>
                        <span class="material-symbols-sharp text-2xl mr-2" style="font-size:30px">more_vert</span>
                    </div>
                {/each}
            </div>
            
            <div class="flex flex-row justify-between items-center">
                <span class="material-symbols-sharp text-2xl ml-2" style="font-size:30px">save</span>
                <span class="material-symbols-sharp text-2xl mr-2" style="font-size:30px">more_vert</span>
            </div> 
        </div> 
    </div>
    {/if}

</div>

<style lang="postcss">
    .sidebar {
        @apply border-r border-gray-400;
        position: fixed;
        width: 65px;
        height: 100%;
        transition: all 0.5s;
    }

    .sidebar.open {
        width: 250px;
    }
</style>