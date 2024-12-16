<script setup>
import axios from 'axios';
import { computed, onBeforeMount, ref } from 'vue';
import _ from 'lodash';

const loading = ref(false);
const platformToAdd = ref({});
const platformToEdit = ref({});
const platform = ref([]);
const platformStats = ref({});

async function fetchStats() {
    try {
        const response = await axios.get("/api/platform/stats/");
        platformStats.value = response.data;
        console.log(platformStats.value); // Verify the data
    } catch (error) {
        console.error("Error fetching statistics:", error);
    }
}

async function fetchPlatform() {
    loading.value = true;
    const r = await axios.get("/api/platform/");
    console.log(r.data)
    platform.value = r.data;
    loading.value = false;
}

async function onPlatformAdd() {
    await axios.post("/api/platform/", {
        ...platformToAdd.value
    });
    await fetchPlatform();
}

async function onRemoveClick(platform) {
    console.log(platform);
    await axios.delete(`/api/platform/${platform.id}/`);
    await fetchPlatform();
}

async function onEditClick(platform) {
    platformToEdit.value = { ...platform };
}

async function onUpdatePlatform() {
    await axios.put(`/api/platform/${platformToEdit.value.id}/`, {
        ...platformToEdit.value,
    });
    await fetchPlatform();
}

onBeforeMount(async () => {
    await fetchStats();
    await fetchPlatform();
})

</script>
<template>
    <div class="container-fluid">
        <form @submit.prevent.stop="onPlatformAdd">
            <div class="p-2">
                <div class="row">
                    <div class="col">
                        <div class="form-floating">
                            <input type="text" class="form-control" v-model="platformToAdd.name" required />
                            <label for="floatingInput">Название платформы</label>
                        </div>
                    </div>
                    <div class="col-auto">
                        <button class="btn btn-primary">Добавить</button>
                    </div>
                </div>
            </div>
        </form>
        <div class="stats-section" v-if="platformStats">
            <h3>Platform Statistics</h3>
            <div>
                <p><strong>Количество записей:</strong> {{ platformStats.count }}</p>
            </div>
        </div>

        <div>
            <div v-for="item in platform" class="platform-item">
                <div>{{ item.name }}</div>
                <div>
                    <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editPlatformModal"
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

            <div class="modal fade" id="editPlatformModal" tabindex="-1">
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
                                <div class="col">
                                    <div class="form-floating">
                                        <input type="text" class="form-control" v-model="platformToEdit.name" />
                                        <label for="floatingInput">Название платформы</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                Закрыть
                            </button>
                            <button data-bs-dismiss="modal" type="button" class="btn btn-primary"
                                @click="onUpdatePlatform">
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
.platform-item {
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
