<template>
    <div>
        <form @submit.prevent="submitForm()">
            <div class="mb-3">
                <label for="title" class="form-label">Title</label>
                <input type="text" class="form-control" id="title" v-model="title">
            </div>
            <div class="mb-3">
                <label for="description" class="form-label">Description</label>
                <input type="text" class="form-control" id="description" v-model="description">
            </div>
            <button type="submit">Save</button>
        </form>
    </div>

</template>

<script>
import axios from 'axios';
export default{
    name: "Mapform",
    data(){
        return{
            title: "",
            description: "",
        }
    },
    methods: {
        async submitForm (event) {
            try
            {
                const response = await axios.post('http://127.0.0.1:5000/createmap', {
                userid:localStorage.getItem('userid'),
                title: this.title,
                description: this.description,
                });
                this.$emit('submit', { show: false });
                console.log(response.data.message);
            }
            catch (error) {
                console.log(error);
            }
        }
    }
}
</script>

<style>
form {
  display: flex;
  flex-direction: column;
}

button {
  background-color: #007bff;
  color: white;
  padding: 10px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
button:hover {
  background-color: #0056b3;
}

.form-floating label {
  color: #6c757d;
}

.form-floating input {
  border-radius: 10px;
  border: none;
  padding-left: 12px;
  box-shadow: none;
  background-color: #f2f2f2;
}

.form-check-input {
  border-radius: 10px;
}
</style>

