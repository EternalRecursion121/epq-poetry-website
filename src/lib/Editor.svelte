<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editordiv: null|HTMLDivElement = null;

    $: if(editordiv || mode === 4){
        editordiv.innerHTML = currentPoem.body;
        console.log("before: " + editordiv?.innerHTML);
        console.log(editordiv?.innerHTML.match(/\b(?<!<|span|\/)(?!>|<\/span>)(\w+)(?!<|<\/span|\/>)(?<!>|span)\b/g))
        console.log("<div>hi</div><div>hello</div><div>something<br></div>".match(/\b(?<!<|span|\/)(?!>|<\/span>)(\w+)(?!<|<\/span|\/>)(?<!>|span)\b/g))
        editordiv.innerHTML = editordiv.innerHTML.replace(/\b(?<!<|span>|\/)(?!>|<\/span>)(\w+)(?!<|<\/span>)(?<!>|span)\b/g, '<span>$1</span>');
        console.log(editordiv?.innerHTML)
    }

</script>

<div class="h-screen p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode===2 || mode===3}>
    <div class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden font-sans" bind:this={editordiv} contenteditable={mode!==2}></div>
</div> 

<style lang="postcss">
    span:hover {
        background-color: coral;
    }
</style>
