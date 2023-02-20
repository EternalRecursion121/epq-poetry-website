<script lang="ts">
  import "../app.css";
  import PrimarySidebar from "$lib/PrimarySidebar.svelte";

  let open = true;
</script>

<div>
  <PrimarySidebar bind:open/>
  <div class="main-section" class:sidebar-open={open}>
    <slot />
  </div>
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
    width: calc(100% - 65px);
    transition: all 0.5s ease;
    z-index: 2;
  }

  .main-section.sidebar-open{
    left: 250px;
    width: calc(100% - 250px);
  }
</style>
  