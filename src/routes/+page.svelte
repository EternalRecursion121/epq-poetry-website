<script lang="ts">
  import "../app.css";
  import PrimarySidebar from "$lib/PrimarySidebar.svelte";
  import Editor from "$lib/Editor.svelte";
  import RightSidebar from "$lib/RightSidebar.svelte";
  import { env } from '$env/dynamic/public';

  import { onMount } from "svelte";

  let pSidebarOpen = true;
  let mode = 1;
  let newPoem = true;
  let currentPoem = {};
  let selectedPoemId: string;
  const modes = ["planning", "reading", "writing", "editing"];
  let poems: Record<string, Object> = {};
  let editordiv:HTMLDivElement;
  let selectedWordIndex:number|null = null;
  let replaceWord: () => void;

  $: console.log(poems);

  function savePoem() {
    if (editordiv) {
      currentPoem.body = editordiv.innerText;
    }

    if (newPoem) {
      fetch(`${env.PUBLIC_SERVER_URL}/poems`, {
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
        fetch(`${env.PUBLIC_SERVER_URL}/poems/` + selectedPoemId, {
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
    poems = { ...poems };
    
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

    fetch(`${env.PUBLIC_SERVER_URL}/poems`)
      .then(res => res.json())
      .then(data => {
          poems = data;
      });
  });


  function createPoem() {
    console.log("CREATING NEW POEM")
    newPoem = true;
    currentPoem.name = 'New Poem';
    currentPoem.body = '';
    currentPoem.year = 2022;
    currentPoem.themes = [];
    currentPoem.form = '';
    currentPoem.poet = '';
  }

  $: if (newPoem) {
    createPoem()
  }
</script>

<svelte:head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Sharp:opsz,wght,FILL,GRAD@48,400,0,0" />
</svelte:head>

<div>
  <PrimarySidebar bind:open={pSidebarOpen} bind:mode bind:newPoem {poems} {createPoem} bind:selectedPoemId {savePoem} bind:currentPoem {selectedWordIndex}/>
  <div class="main-section" class:sidebar-open={pSidebarOpen}>
    <Editor bind:mode bind:currentPoem bind:editordiv bind:selectedWordIndex bind:replaceWord/>
  </div>
  <RightSidebar {pSidebarOpen} on:replaceWord={(e) => replaceWord(e.detail.word)}/>
</div>

<style lang="postcss">
  :global(html) {
    background-color: theme(colors.gray.100);
  }

  .main-section{
    position: relative;
    min-height: 100vh;
    top: 0;
    left: 65px;
    width: calc(100% - 65px - 350px);
    transition: all 0.5s ease;
    z-index: 2;
  }

  .main-section.sidebar-open{
    left: 300px;
    width: calc(100% - 300px - 350px);
  }
</style>
  