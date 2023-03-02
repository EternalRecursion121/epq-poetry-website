<script lang="ts">
	import { Node } from "postcss";

    export let mode: number;
    export let currentPoem: Object;
    export let editorpre: null|HTMLPreElement = null;

    import { onMount } from "svelte";

    let marks: Array<HTMLElement> = []; 
    let selectionStart: number;
    let selectionEnd: number;

    onMount(() => {
        document.addEventListener('selectionchange', handleSelectionChange);
    })

    $: if (editorpre){
        editorpre.innerHTML = currentPoem.body;
    }

    function highlight(range: Range) {
        console.log(range.extractContents())
        for (let mark of marks) {
            mark.parentNode?.replaceChild(mark.firstChild, mark);
        }

        range.extractContents().childNodes.forEach((childNode) => {
            if (childNode.nodeType === Node.TEXT_NODE) {
                const mark = document.createElement('mark');
                marks.push(mark);
                childNode.parentNode?.insertBefore(mark, childNode);
                mark.appendChild(childNode);
            }
        });
    }

    function handleSelectionChange(e) {
        if (e.target.activeElement !== editorpre) return;

        const selection = window.getSelection();
        console.log(selection)
        if (selection && !selection.isCollapsed) {
            const range = selection.getRangeAt(0);

            if (selectionStart !== range.startOffset || selectionEnd !== range.endOffset) {
                highlight(range);
            }
        }
    }

</script>

<div class="h-screen p-4">
    <input class="text-3xl font-bold w-full h-14 bg-transparent outline-none" bind:value={currentPoem.name} readonly={mode===2}>
    <pre class="block w-full h-full pl-1 py-4 bg-gray-100 text-gray-900 focus:outline-none focus:border-transparent overflow-y-hidden font-sans" bind:this={editorpre} contenteditable={mode!==2}></pre>
</div> 

<style lang="postcss">
    mark {
        background-color: #ff0;
        color: #000;
    }
</style>