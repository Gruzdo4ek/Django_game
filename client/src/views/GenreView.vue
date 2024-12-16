<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import _ from 'lodash';

const loading = ref(false);
const genreToAdd = ref({});
const genreToEdit = ref({});
const genre = ref([]);
const genreStats = ref({});

async function fetchStats() {
    try {
        const response = await axios.get("/api/genre/stats/");
        genreStats.value = response.data;
        console.log(genreStats.value); // Verify the data
    } catch (error) {
        console.error("Error fetching statistics:", error);
    }
}

async function fetchGenre() {
    loading.value = true;
    const r = await axios.get("/api/genre/");
    console.log(r.data)
    genre.value = r.data;
    loading.value = false;
}

async function onGenreAdd() {
    await axios.post("/api/genre/", {
        ...genreToAdd.value
    });
    await fetchGenre();
}

async function onRemoveClick(genre) {
    console.log(genre);
    await axios.delete(`/api/genre/${genre.id}/`);
    await fetchGenre();
}

async function onEditClick(genre) {
    genreToEdit.value = { ...genre };
}

async function onUpdateGenre() {
    await axios.put(`/api/genre/${genreToEdit.value.id}/`, {
        ...genreToEdit.value,
    });
    await fetchGenre();
}

onBeforeMount(async () => {
    await fetchStats();
    await fetchGenre();
})

</script>
<template>
    <div class="container-fluid">
        <form @submit.prevent.stop="onGenreAdd">
            <div class="p-2">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="genreToAdd.name" required />
                            <label for="floatingInput">Название жанра</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </div>
        </form>
        <div class="stats-section" v-if="genreStats">
            <h3>Genre Statistics</h3>
            <div>
                <p><strong>Количество записей:</strong> {{ genreStats.count }}</p>
            </div>
        </div>
            <div>
                <div v-for="item in genre" class="genre-item">
                    <div>{{ item.name }}</div>
                    <div>
                        <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editGenreModal"
                            @click="onEditClick(item)">
                            <i class="bi bi-pencil"></i>
                        </button>
                    </div>
                    <div>
                        <button class="btn btn-danger" @click="onRemoveClick(item)">
                            <i class="bi bi-x"></i>
                        </button>
                    </div>
                </div>

                <div class="modal fade" id="editGenreModal" tabindex="-1">
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h1 class="modal-title fs-5" id="exampleModalLabel">
                                    редактировать
                                </h1>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col">
                                        <div class="form-floating">
                                            <input type="text" class="form-control" v-model="genreToEdit.name" />
                                            <label for="floatingInput">Название жанра</label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    Закрыть
                                </button>
                                <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                    @click="onUpdateGenre">
                                    Сохранить
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>
        </div>
</template>

<style lang="css" scoped>
.genre-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr auto auto;
    gap: 16px;
    align-content: center;
    align-items: center;

}
.stats-section {
  padding: 1rem;
  margin-bottom: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}
</style>
