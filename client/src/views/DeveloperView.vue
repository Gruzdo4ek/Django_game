<script setup>
import axios from 'axios';
import { storeToRefs } from 'pinia';
import { computed, ref, onBeforeMount, watch } from 'vue'
import _ from 'lodash';
import useUserProfileStore from '@/stores/userProfileStore';

const userProfileStore = useUserProfileStore();
const {
  isAuthorized,
  isSuperUser,
  username
} = storeToRefs(userProfileStore)
const users = ref([]);
const loading = ref(false);
const developerToAdd = ref({});
const developerToEdit = ref({});
const developer = ref([]);
const country = ref([])
const countryById = computed(() => {
  return _.keyBy(country.value, x => x.id)
})
const developerStats = ref({});
const selectedUserId = ref()
const alert403 = ref(false);

async function fetchStats() {
  try {
    const response = await axios.get("/api/developer/stats/");
    developerStats.value = response.data;
    console.log(developerStats.value); // Verify the data
  } catch (error) {
    console.error("Error fetching statistics:", error);
  }
}

async function fetchUsers() {
  const r = await axios.get("/api/user/");
  users.value = r.data
  console.log(users.value)
}

async function fetchCountry() {
  const r = await axios.get("/api/country_developer/");
  console.log(r.data)
  country.value = r.data;
}

async function fetchDeveloper(selectedUserId) {
  loading.value = true;
  const r = await axios.get("/api/developer/");
  console.log(r.data)
  developer.value = r.data;
  loading.value = false;

  if (selectedUserId.value != null) {
    console.log(r.data.filter(it => it.user === selectedUserId.value))
    developer.value = r.data.filter(it => it.user === selectedUserId.value)
  }
  else
    developer.value = r.data

  console.log(selectedUserId.value)
  console.log(developer.value)
}

async function onDeveloperAdd() {
  await axios.post("/api/developer/", {
    ...developerToAdd.value
  });
  await fetchDeveloper(selectedUserId);
}

async function onRemoveClick(developer) {
  console.log(developer);
  await axios.delete(`/api/developer/${developer.id}/`);
  await fetchDeveloper(selectedUserId);
}

async function onEditClick(developer) {
  developerToEdit.value = { ...developer };
}

async function onUpdateDeveloper() {
  await axios.put(`/api/developer/${developerToEdit.value.id}/`, {
    ...developerToEdit.value,
  });
  await fetchDeveloper(selectedUserId);
}

async function handleUserChange() {
  await fetchDeveloper(selectedUserId)
}

onBeforeMount(async () => {
  await fetchStats();
  await fetchDeveloper(selectedUserId);
  await fetchCountry();
})

watch(isSuperUser, () => {
  if (isSuperUser.value) {
    console.log(isSuperUser.value)
    fetchUsers()
  }
}, {
  immediate: true
})

</script>
<template>
  <div class="container-fluid">
    <form @submit.prevent.stop="onDeveloperAdd">
      <div class="p-2">
        <div class="row">
          <div class="col-7">
            <div class="form-floating">
              <input type="text" class="form-control" v-model="developerToAdd.name" required />
              <label for="floatingInput">Имя разработчика</label>
            </div>
          </div>
          <div class="col">
            <div class="form-floating">
              <select name="" id="" class="form-select" v-model="developerToAdd.country_fk" required>
                <option :value="g.id" v-for="g in country">{{ g.name }}</option>
              </select>
              <label for="floatingInput">Страна разработчика</label>
            </div>
          </div>
          <div class="col-auto">
            <button class="btn btn-primary">Добавить</button>
          </div>
        </div>
      </div>
    </form>
    <div class="form-floating" v-if="isSuperUser === true">
      <select name="" id="" class="form-select" v-model="selectedUserId" @change="handleUserChange">
        <option :key="u.id" :value="u.id" v-for="u in users">{{ u.username }}</option>
      </select>
      <label for="floatingInput">Выберете пользователя</label>
    </div>
    <div class="stats-section" v-if="developerStats">
      <h3>Developer Statistics</h3>
      <div>
        <p><strong>Количество записей:</strong> {{ developerStats.count }}</p>
      </div>
    </div>
    <div>
      <div v-for="item in developer" class="developer-item">
        <div>{{ item.name }}</div>
        <div>{{ countryById[item.country_fk]?.name }}</div>
        <div>
          <button class="btn btn-success" data-bs-toggle="modal" data-bs-target="#editDeveloperModal"
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

      <div class="modal fade" id="editDeveloperModal" tabindex="-1">
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
                <div class="col-6">
                  <div class="form-floating">
                    <input type="text" class="form-control" v-model="developerToEdit.name" />
                    <label for="floatingInput">Имя разработчика</label>
                  </div>
                </div>
                <div class="col-6">
                  <div class="form-floating">
                    <select name="" id="" class="form-select" v-model="developerToEdit.country_fk">
                      <option :value="g.id" v-for="g in country">{{ g.name }}</option>
                    </select>
                    <label for="floatingInput">Страна разработчика</label>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              Закрыть
            </button>
            <button data-bs-dismiss="modal" type="button" class="btn btn-primary" @click="onUpdateDeveloper">
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
.developer-item {
  padding: 0.5rem;
  margin: 0.5rem 0;
  border: 1px solid silver;
  border-radius: 8px;
  display: grid;
  grid-template-columns: 1fr auto auto auto ;
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
