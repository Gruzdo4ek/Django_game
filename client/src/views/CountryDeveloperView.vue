<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import _ from 'lodash';

const loading = ref(false);
const countryDeveloperToAdd = ref({});
const countryDeveloperToEdit = ref({});
const countryDeveloper = ref([]);
const flagPictureRef = ref();
const flagAddImageUrl = ref();
const selectedImageUrl = ref('');
const editFlagPictureRef = ref();
const flagEditImageUrl = ref();
const countryStats = ref({});

async function fetchStats() {
    try {
        const response = await axios.get("/api/country_developer/stats/");
        countryStats.value = response.data;
        console.log(countryStats.value); // Verify the data
    } catch (error) {
        console.error("Error fetching statistics:", error);
    }
}

async function fetchCountryDeveloper() {
    loading.value = true;
    const r = await axios.get("/api/country_developer/");
    console.log(r.data)
    countryDeveloper.value = r.data;
    loading.value = false;
}

async function flagAddPictureChange() {
    if (flagPictureRef.value && flagPictureRef.value.files && flagPictureRef.value.files[0]) {
        flagAddImageUrl.value = URL.createObjectURL(flagPictureRef.value.files[0]);
    } else {
        console.error("No picture file selected.");
    }
}

async function flagEditPictureChange() {
    if (editFlagPictureRef.value && editFlagPictureRef.value.files && editFlagPictureRef.value.files[0]) {
        flagEditImageUrl.value = URL.createObjectURL(editFlagPictureRef.value.files[0]);
    } else {
        console.error("No picture file selected.");
    }
}

async function onCountryDeveloperAdd() {
    const formData = new FormData();
    formData.set('name', countryDeveloperToAdd.value.name);
    if (flagPictureRef.value && flagPictureRef.value.files[0]) {
        formData.append('picture', flagPictureRef.value.files[0]);
    } else {
        console.error("No picture selected");
    }
    await axios.post("/api/country_developer/", formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    });
    await fetchCountryDeveloper();

}

async function openImageModal(imageUrl) {
    selectedImageUrl.value = imageUrl;
    const imageModal = new bootstrap.Modal(document.getElementById('imageModal'));
    imageModal.show();
}

async function onRemoveClick(countryDeveloper) {
    console.log(countryDeveloper);
    await axios.delete(`/api/country_developer/${countryDeveloper.id}/`);
    await fetchCountryDeveloper();
}

async function onEditClick(countryDeveloper) {

    countryDeveloperToEdit.value = { ...countryDeveloper };
    flagEditImageUrl.value = countryDeveloper.picture || ''

}

async function onUpdateCountryDeveloper() {
    const formData = new FormData();
    formData.set('name', countryDeveloperToEdit.value.name);

    if (editFlagPictureRef.value && editFlagPictureRef.value.files[0]) {
        formData.append('picture', editFlagPictureRef.value.files[0]);
    }

    try {
        await axios.put(`/api/country_developer/${countryDeveloperToEdit.value.id}/`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        fetchCountryDeveloper();
    } catch (error) {
        console.error("Error updating game:", error.response.data);
    }
}

onBeforeMount(async () => {
    await fetchStats();
    await fetchCountryDeveloper();
})

</script>
<template>
    <div class="container-fluid">
        <form @submit.prevent.stop="onCountryDeveloperAdd">
            <div class="p-2">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="countryDeveloperToAdd.name" required />
                            <label for="floatingInput">Страна</label>
                        </div>
                    </div>
                    <div class="col-auto" style="align-content: center; align-items: center;">
                        <input class="form-control" type="file" ref="flagPictureRef" @change="flagAddPictureChange">
                    </div>
                    <div class="col-auto">
                        <img :src="flagAddImageUrl" style="max-height: 60px;" alt="">
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </div>
        </form>
        <div class="stats-section" v-if="countryStats">
            <h3>Country Statistics</h3>
            <div>
                <p><strong>Количество записей:</strong> {{ countryStats.count }}</p>
            </div>
        </div>
        <div>
            <div v-for="item in countryDeveloper" class="countryDeveloper-item">
                <div>{{ item.name }}</div>
                <div v-show="item.picture">
                    <img :src="item.picture" style="max-height: 60px;" alt="Flag image" data-bs-toggle="modal"
                        data-bs-target="#imageModal" @click="openImageModal(item.picture)">
                </div>
                <div>
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editCountryDeveloperModal"
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

            <div class="modal fade" id="imageModal" tabindex="-1" aria-labelledby="imageModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h5 class="modal-title" id="imageModalLabel">Изображение игры</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <img :src="selectedImageUrl" class="img-fluid" alt="Game image">
                        </div>
                    </div>
                </div>
            </div>

            <div class="modal fade" id="editCountryDeveloperModal" tabindex="-1">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <h1 class="modal-title fs-5" id="exampleModalLabel">
                                редактировать
                            </h1>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <div class="row">
                                <div class="col-flex">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="countryDeveloperToEdit.name" />
                                        <label for="floatingInput">Страна</label>
                                    </div>
                                </div>
                                <div class="row p-2">
                                    <div class="col-auto">
                                        <input class="form-control" type="file" ref="editFlagPictureRef"
                                            @change="flagEditPictureChange">
                                    </div>
                                    <div class="col-auto">
                                        <img :src="flagEditImageUrl" style="max-height: 60px;" alt="Preview">
                                    </div>
                                </div>

                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Закрыть
                            </button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdateCountryDeveloper">
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
.countryDeveloper-item {
    padding: 0.5rem;
    margin: 0.5rem 0;
    border: 1px solid silver;
    border-radius: 8px;
    display: grid;
    grid-template-columns: 1fr 1fr auto auto;
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
