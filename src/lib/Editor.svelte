<script lang="ts">
    export let mode: number;
    export let currentPoem: Object;
    export let editorpre: null|HTMLPreElement = null;

    import { onMount } from "svelte";

    let selectionStart: number;
    let selectionEnd: number;
    let selectionTimer: null | number = null;

    let lastRange: Range;

    onMount(() => {
        document.addEventListener('selectionchange', handleSelectionChange);
    })

    $: if (editorpre){
        editorpre.innerHTML = currentPoem.body;
    }

    function highlight(range: Range) {

        // console.log("RUN")
        // // Remove any existing mark elements
        // const existingMarks = document.querySelectorAll('mark[data-highlighted]');
        // existingMarks.forEach(mark => {
        //     mark.outerHTML = mark.innerHTML;
        // });

        // // Create a new mark element to wrap the selection
        // const mark = document.createElement('mark');
        // mark.setAttribute('data-highlighted', 'true');

        // // Clone the range to avoid modifying the original selection
        // const clonedRange = range.cloneRange();

        // // Get the start and end container elements for the selection
        // const startContainer = range.startContainer;
        // const endContainer = range.endContainer;

        // // If the start and end container elements are the same, just wrap the selection with the new mark element
        // if (startContainer === endContainer) {
        //     clonedRange.surroundContents(mark);
        // } else {
        //     // If the start and end container elements are different, create a new range for each line of text
        //     const startLineRange = document.createRange();
        //     startLineRange.setStart(startContainer, range.startOffset);
        //     startLineRange.setEndAfter(startContainer);

        //     const endLineRange = document.createRange();
        //     endLineRange.setStartBefore(endContainer);
        //     endLineRange.setEnd(endContainer, range.endOffset);

        //     // Wrap the start line with the new mark element
        //     const startLineMark = mark.cloneNode();
        //     startLineMark.appendChild(startLineRange.extractContents());
        //     startLineRange.insertNode(startLineMark);

        //     // Wrap each middle line with a new mark element
        //     let currentNode = startContainer.nextSibling;
        //     while (currentNode && currentNode !== endContainer) {
        //         const lineMark = mark.cloneNode();
        //         lineMark.appendChild(currentNode.cloneNode(true));
        //         currentNode.parentNode.replaceChild(lineMark, currentNode);
        //         currentNode = startContainer.nextSibling;
        //     }

        //     // Wrap the end line with the new mark element
        //     const endLineMark = mark.cloneNode();
        //     endLineMark.appendChild(endLineRange.extractContents());
        //     endLineRange.insertNode(endLineMark);
        // }
        console.log(mark)
        mark.unmark();
        mark.markRanges([range]);
    }

    function handleSelectionChange(e) {
        console.log("SLEECTION CHANGE")
        if (e.target.activeElement !== editorpre) return;

        const selection = window.getSelection();

        if (selection && !selection.isCollapsed) {
            const range = selection.getRangeAt(0);

            if (selectionStart !== range.startOffset || selectionEnd !== range.endOffset) {
                highlight(range);

                selectionStart = range.startOffset;
                selectionEnd = range.endOffset;
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