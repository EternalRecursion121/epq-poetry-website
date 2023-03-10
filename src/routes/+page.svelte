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
  let currentPoem = {};
  let selectedPoemId: string;
  const modes = ["planning", "reading", "writing", "editing"];
  let poems: Record<string, Object> = {};
  let editordiv:HTMLPreElement;

  $: console.log(poems);

  function savePoem() {
    if (editordiv) {
      currentPoem.body = editordiv.innerHTML;
    }

    if (newPoem) {
      fetch('http://127.0.0.1:8000/poems', {
          method: 'POST',
          headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          },
          body: JSON.stringify(currentPoem)
      }).then(res => res.json()).then(data => {
        
          poems[data.poem_id] = data.poem;
          selectedPoemId = data.poem_id;
      });
      newPoem = false;
    } else {
        fetch('http://127.0.0.1:8000/poems/' + selectedPoemId, {
            method: 'PUT',
            headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            },
            body: JSON.stringify(currentPoem)
        }).then(res => res.json()).then(data => {
            poems[selectedPoemId] = data.poem;
        });
    }
    poems = poems;
  }

  
  
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


  onMount(() => {
    document.addEventListener('keydown', onKeyPress);

    fetch('http://127.0.0.1:8000/poems',
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      }).then(res => res.json()).then(data => {
        poems = data;
    });
  });


  function createPoem() {
    newPoem = true;
    currentPoem.name = 'New Poem';
    currentPoem.body = '';
  }

  $: if (newPoem) {
    createPoem()
  }
</script>

<div>
  <PrimarySidebar bind:open={pSidebarOpen} bind:mode bind:newPoem {poems} {createPoem} bind:selectedPoemId {savePoem} bind:currentPoem/>
  <div class="main-section" class:sidebar-open={pSidebarOpen}>
    <Editor bind:mode bind:currentPoem bind:editordiv={editordiv}/>
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
  