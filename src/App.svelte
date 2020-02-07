<script>
	
	import { onMount } from 'svelte';
	import { beforeUpdate, afterUpdate } from 'svelte';

	let name  ;
	let currentuser = name;
	let div;
	let autoscroll;
	let input;


	import io from 'socket.io-client';
	const socket = io('http://127.0.0.1:5000/');

	
	beforeUpdate(() => {
		autoscroll = div && (div.offsetHeight + div.scrollTop) > (div.scrollHeight - 20);
	});

	afterUpdate(() => {
		if (autoscroll) div.scrollTo(0, div.scrollHeight);
	});

	function dateformat(){
		let now = new Date();
		const offsetMs = now.getTimezoneOffset() * 60 * 1000;
		const dateLocal = new Date(now.getTime() - offsetMs);
		let str =dateLocal.toISOString().slice(0, 19).replace(/-/g, "/").replace("T", " ");
		return str;
	};

	function handleKeydown() {

		if (event.which === 13 || event.type === "click") {

			const text = input.value;
			if (!text) return;
			
			socket.emit('chat message', {
				"author": name, 
				"commend": text, 
				"time": dateformat(),
			});
			
			console.log(comments);
			input.value = '';
		};
	};
	
	

	
	var formdata = new FormData();
	var requestOptions = {
		method: 'GET',
		redirect: 'follow'
		};
	let comments=[];
	onMount(async() => { 
		const res = await fetch("http://127.0.0.1:5000/api/chat", requestOptions);
		let results = await res.json();
		await results.reverse().forEach(result => {
			comments = comments.concat({
					author: result.author,
					text: result.commend,
					time: result.time

				});

		});

	});
	
	
	
	socket.on('chat message', function (json) {
		json = JSON.parse(json);
		console.log(typeof(json));
        comments = comments.concat({
				author: json.author,
				text: json.commend,
				time: json.time
			});
		

      });


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
				<article class="{comment.author=== name? "user":"other"}">
					<span>{#if comment.author != name}{comment.author}:<n></n>{/if} {comment.text}</span>
					<input id="nothing" type="text">
					<div id="commentdate">
						{comment.time}
					</div>
				</article>
				
				 
			{/if}
		{:else}

			<!-- this block renders when photos.length === 0 -->
			<center><p>Comments are loading...</p></center>
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

	article {
		margin: 0.5em 0;
		position: relative;
	
		
	}
	#commentdate{
		display: none;
		transition: all 5s ease-out;
		-webkit-transition: all 5s ease-in-out;

	}
	input#nothing{
		opacity: 0;
		top:0;
		left:0;
		position: absolute;
		cursor: pointer;
		transition: all 5s ease-out; 
		-webkit-transition: all 5s ease-in-out;
	}
	
	input#nothing:focus + div#commentdate{
		display:block;
		color: dimgrey;

	
		
	}

	.user {
		text-align: right;

	}

	span {
		padding: 0.5em 1em;
		display: inline-block;
	
	}

	.other span {
		background-color: #eee;
		border-radius: 1em 1em 1em 0;
		max-width: 250px;
		word-wrap: break-word;
		
	}

	.user span {
		background-color: #0074D9;
		color: white;
		border-radius: 1em 1em 0 1em;
		text-align: left;
		max-width: 250px;
		word-wrap: break-word;
	}
	.user input#nothing{
		opacity: 0;
		top:0;
		right:0;
		width: 100%;
		float:right;
		position: absolute;
		cursor: pointer;
		
	}
	

	@media only screen and (max-width: 400px) {
		.headdiv{
			max-height: 100px;
		}
	}
</style>

