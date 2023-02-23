<script lang="ts">
  import "../app.css";
  import PrimarySidebar from "$lib/PrimarySidebar.svelte";
  import Editor from "$lib/Editor.svelte";
  import RightSidebar from "$lib/RightSidebar.svelte";

  import { onMount } from "svelte";

  let pSidebarOpen = true;
  let mode = 1;
  let command = '';
  let newPoem = true;
  const modes = ["planning", "reading", "writing", "editing"];
  
  function onKeyPress(e: KeyboardEvent) {
    if (e.getModifierState('Alt')) {
      switch (e.key) {
        case '1': {
          mode = 1;
          break;
        }
        case '2': {
          mode = 2;
          break;
        }
        case '3': {
          mode = 3;
          break;
        }
        case '4': {
          mode = 4;
          break; 
        }
        default: {
          return;
        }
      }
      e.preventDefault();
    } else if (e.key === 'Tab') {
        if (e.getModifierState("Shift")) {
          mode = (mode + 2) % 4 + 1;
        } else {
          mode = (mode % 4) + 1;
        }
        e.preventDefault();
      }
  }

  let poems: Array<Object>;

  onMount(() => {
    document.addEventListener('keydown', onKeyPress);

    fetch('http://127.0.0.1:8000/api/poems').then(res => res.json()).then(data => {
      poems = data;
    });
  });

</script>

<div>
  <PrimarySidebar bind:open={pSidebarOpen} bind:mode {poems} {newPoem}/>
  <div class="main-section" class:sidebar-open={pSidebarOpen}>
    <Editor bind:mode/>
  </div>
  <RightSidebar {command}/>
</div>

<style lang="postcss">
  :global(html) {
    background-color: theme(colors.gray.100);
  }

  * {
    box-sizing: border-box;
  }

  .main-section{
    position: relative;
    min-height: 100vh;
    top: 0;
    left: 65px;
    width: calc(100% - 65px);
    transition: all 0.5s ease;
    z-index: 2;
  }

  .main-section.sidebar-open{
    left: 250px;
    width: calc(100% - 250px);
  }
</style>
  