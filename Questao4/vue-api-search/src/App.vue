<template>
  <div>
    <h1>Buscar Operadoras</h1>
    <input v-model="query" placeholder="Digite o termo de busca" @keyup.enter="search">
    <button @click="search">Buscar</button>

    <div v-if="error" class="error">{{ error }}</div>
    
    <div v-if="results.length">
      <ul>
        <li v-for="(item, index) in results" :key="index">
          <strong>{{ item.Nome_Fantasia }}</strong> - {{ item.Registro_ANS }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const query = ref('')
const results = ref([])
const error = ref('')
''
const search = async () => {
  if (!query.value) {
    error.value = "O campo de busca não pode estar vazio!";
    return;
  }

  try {
    console.log("Buscando:", query.value);
    const response = await fetch(`http://127.0.0.1:5000/api/search?query=${encodeURIComponent(query.value)}&limit=20`, {
      headers: { "Accept": "application/json" }
    });

    const data = await response.json();
    console.log("Resposta da API:", data);

    if (response.ok) {
      results.value = data;
      error.value = "";
    } else {
      error.value = "Nenhum resultado encontrado.";
    }
  } catch (err) {
    console.error("Erro ao conectar com a API:", err);
    error.value = "Erro ao conectar com a API.";
  }
}

</script>

<style>
.error {
  color: red;
}
</style>
