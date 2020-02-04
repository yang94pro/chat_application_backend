<script>
	let name  ;
	let currentuser = name;
	
	let input;
	import io from 'socket.io-client';
	const socket = io('https://polar-eyrie-04595.herokuapp.com');

	import { beforeUpdate, afterUpdate } from 'svelte';

	let div;
	let autoscroll;

	beforeUpdate(() => {
		autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
	});

	afterUpdate(() => {
		if (autoscroll) div.scrollTo(0, div.scrollHeight);
	});

	
	let comments = [
		{ author: 'eliza', text:"how are you", active:false}
	];
	socket.on('chat message', function (json) {
        comments = comments.concat({
				author: json.author,
				text: json.commend,
				time: json.time,
				active: json.active,
			});
      });


	function handleKeydown() {

		if (event.which === 13 || event.type === "click") {

			const text = input.value;
			if (!text) return;
			
			socket.emit('chat message', {
				"author": name, 
				"commend": text, 
				"time": Date(),
				"active":false,
				
			});
			
			console.log(comments);
			input.value = '';
		};
	};


</script>

<main>
<div class="title"> <h1>Hello {name}!</h1></div>
<div class="headdiv">
	<label>Name:  </label>
	<input type="text" bind:value={name} class="user" />
</div>

<div class="chat">

	<div class="scrollable" bind:this={div}>
		{#each comments as comment}
			{#if comment.author==="system"}
				<span class="systemsg">{comment.text}</span>
			{:else}
				
				<div>
					<article class="{comment.author=== name? "user":"other"}">
						<input type=checkbox id={comment} bind:checked={comment.active} >
						<label for={comment}>{#if comment.author != name}{comment.author}:<n></n>{/if} {comment.text} </label>
			
					</article>
					{#if comment.active}
					<div class="receivedate">
						{comment.time}
					</div>
					{/if}
				</div>
				
			{/if}
		{/each}
	</div>

	<input bind:this={input} on:keydown={handleKeydown}/> <button  type="submit" on:click={handleKeydown}>Send</button>

</div>
	
	

</main>

<style>

	main{
		display: grid;
		justify-content: center;
		height: 95vh;
		width: 95vw;
		box-sizing: border-box;		

	}
	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 3em;
		font-weight: bold;

		word-wrap: break-word;
		
	}
	.title{
		width: 50vw;
	}
    * {
     
	  font: 20px Helvetica, Arial;
    }
	.default{
		opacity: 0;
	}

		
	.systemsg{
		text-align: center;
		display: flex;
		flex-direction: column;
		margin: 0;
		padding: 0;
		font-size: 20px;
		color: rgb(151, 151, 151);
	}
	.headdiv{

		display: flex;
		justify-content: space-around;
		height: 50px;
		margin: auto;
		max-width: 100px;
	
		
	}


	.chat {
		position: relative;
		display: flex;
		flex-direction: column;
		height: 50vh;
		max-height: 600px;
		max-width: 640px;
		justify-content: center;
		word-wrap: break-word;
		
		
		
	}

	.scrollable {
		flex: 1 1 auto;
		border-top: 1px solid #eee;
		margin: 0 0 0.5em 0;
		overflow-y: auto;
		word-wrap: break-word;
		
	}
	div{
		position: relative;
	}

	input[type="checkbox"] {
		position: absolute;
		width: 100%;
		height: 100%;
		opacity: 0;
		}
	article {
		margin: 0.5em 0;
		
	}

	.user {
		text-align: right;

	}

	label {
		padding: 0.5em 1em;
		display: inline-block;
		cursor: pointer;
	
	}

	.other label {
		background-color: #eee;
		border-radius: 1em 1em 1em 0;
		max-width: 250px;
		word-wrap: break-word;
		
	}

	.user label {
		background-color: #0074D9;
		color: white;
		border-radius: 1em 1em 0 1em;
		text-align: left;
		max-width: 250px;
		word-wrap: break-word;
	}


	.receivedate{
		opacity: 1;
		text-align: center;
		font-size: 15px;
		color: rgb(138, 136, 136);
		margin:0;
		padding:0;
	}


	@media only screen and (max-width: 400px) {
		.headdiv{
			max-height: 100px;
		}
	}
</style>

