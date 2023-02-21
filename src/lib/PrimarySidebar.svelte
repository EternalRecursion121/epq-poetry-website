<script lang="ts">
    export let open: boolean;
    export let savedFiles:Array<Record<string, string>> = [];

    let mode = "writing";
    const modes = ["planning", "reading", "writing", "editing"];
</script>

<svelte:head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@48,400,0,0" />
</svelte:head>

<div class="sidebar" class:open>
    <div class="flex flex-col border-r items-center border-gray-400 w-[65px] h-full fixed">
        <span class="justify-start material-symbols-sharp hover:bg-black hover:bg-opacity-5 hover:cursor-pointer w-10 h-10 rounded-full mt-3" style="font-size:40px" on:click={()=>{open=!open}}>chevron_left</span>

        <div class:bg-[#FFE08D]="{mode === 'planning'}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center mt-auto" on:click={()=>{mode='planning'}}>
            <span class="material-symbols-sharp" style="font-size:33px">lightbulb</span>
        </div>
        
        <div class:bg-[#7FB2F0]="{mode === 'reading'}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center" on:click={()=>{mode='reading'}}>
            <span class="material-symbols-sharp" style="font-size:30px">visibility</span>
        </div>

        <div class:bg-[#B1D8B7]="{mode === 'writing'}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center" on:click={()=>{mode='writing'}}>
            <span class="material-symbols-sharp" style="font-size:33px">edit</span>
        </div>

        <div class:bg-[#F4A460]="{mode === 'editing'}" class="hover:cursor-pointer flex w-full h-[53px] justify-center items-center mb-10" on:click={()=>{mode='editing'}}>
            <span class="material-symbols-sharp mb-1" style="font-size:28px">edit_square</span>
        </div>
   </div>
    <div class="ml-[65px]">
        
    </div>

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