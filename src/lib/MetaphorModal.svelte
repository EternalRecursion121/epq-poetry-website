<script>
  import { createEventDispatcher } from 'svelte';
  import { afterUpdate } from 'svelte';

  let userInput1 = "";
  let userInput2 = "";
  const dispatch = createEventDispatcher();
  let isButtonClickable = false;

  function submitMetaphor() {
    dispatch('metaphor', { "source": userInput1, "target": userInput2 });
  }

  function closeModal() {
    dispatch('close');
  }

  afterUpdate(() => {
    isButtonClickable = userInput1 !== "" && userInput2 !== "";
  });
</script>

<div class="modal z-50">
  <div class="modal-content" on:click={(event) => event.stopPropagation()}>
    <div class="modal-header pt-4">
      <h2 class="modal-title">Write a Metaphor</h2>
      <button class="close-button" on:click={closeModal}>
        <span class="-scale-x-100={!open} transition-transform duration-300 ease-in-out justify-start material-symbols-sharp hover:cursor-pointer w-10 h-10 rounded-full" style="font-size: 30px" on:click={()=>{open=!open}}>
          close
        </span>
      </button>
    </div>
    <div class="input-container">
      <label for="input1" class="input-label">Comparing</label>
      <input type="text" id="input1" bind:value={userInput1} class="input-field" placeholder="Enter the first term" />
    </div>
    <div class="input-container">
      <label for="input2" class="input-label">with</label>
      <input type="text" id="input2" bind:value={userInput2} class="input-field" placeholder="Enter the second term" />
    </div>
    <button class="submit-button" class:clickable={isButtonClickable} on:click={submitMetaphor}>Submit</button>
  </div>
</div>

<style>
  .modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(0, 0, 0, 0.5);
  }
  
  .modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 4px;
    max-width: 400px;
    width: 100%;
  }
  
  .modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 20px;
  }
  
  .modal-title {
    font-size: 24px;
  }
  
  .close-button {
    background: none;
    border: none;
    cursor: pointer;
  }
  
  .close-icon {
    width: 24px;
    height: 24px;
    fill: #000;
  }
  
  .input-container {
    margin-bottom: 15px;
  }
  
  .input-label {
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 5px;
  }
  
  .input-field {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 16px;
  }
  
  .submit-button {
    padding: 10px 20px;
    @apply bg-blue-400;
    color: #fff;
    font-size: 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .submit-button.clickable {
    @apply bg-blue-500;
    cursor: pointer;
  }
</style>
