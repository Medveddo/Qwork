<script>
    import {fade} from "svelte/transition";
    export let is_correspond;
    export let temperature;
    export let systole_pressure;
    export let diastole_pressure;
</script>
<p class="text-center" transition:fade>
    Соответствует клиническим рекомендациям: {is_correspond}<br>
    Температура: {temperature}<br> 
    Систолическое давление: {systole_pressure}<br> 
    Диастолическое давление: {diastole_pressure}<br> 
</p>