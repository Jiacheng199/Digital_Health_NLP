<template>
    <div>
        <h1>Shark</h1>
        <p>{{ message }}</p>
    </div>
</template>
<script>
import axios from 'axios';
export default {
    name: 'Shark',
    data() {
        return {
            message: 'Shark'
        }
    },
    methods : {
        getShark() {
            axios.get('http://127.0.0.1:5000/shark')
            .then(response => {
                this.message = response.data;
            })
            .catch(error => {
                console.log(error);
            });
        }
    },
    created() {
        this.getShark();
    }
}
</script>